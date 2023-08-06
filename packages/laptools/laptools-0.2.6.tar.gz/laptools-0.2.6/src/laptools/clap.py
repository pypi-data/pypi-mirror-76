import numpy as np

from py_lapjv import lapjv

from . import lap
from ._util import one_hot


def costs(cost_matrix):
    """Solve a constrained linear sum assignment problem for each entry.

    The output of this function is equivalent to, but significantly more
    efficient than,

    >>> def costs(cost_matrix):
    ...     total_costs = np.empty_like(cost_matrix)
    ...     num_rows, num_cols = cost_matrix.shape
    ...     for i in range(num_rows):
    ...         for j in range(num_cols):
    ...             total_costs[i, j] = clap.cost(i, j, cost_matrix)
    ...     return total_costs

    Parameters
    ----------
    cost_matrix : 2darray
        A matrix of costs.

    Returns
    -------
    2darray
        A matrix of total constrained lsap costs. The i, j entry of the matrix
        corresponds to the total lsap cost under the constraint that row i is
        assigned to column j.
    """
    cost_matrix = np.array(cost_matrix, dtype=np.double)

    n_rows, n_cols = cost_matrix.shape
    if n_rows > n_cols:
        return costs(cost_matrix.T).T

    # Find the best lsap assignment from rows to columns without constrains.
    # Since there are at least as many columns as rows, row_idxs should
    # be identical to np.arange(n_rows). We depend on this.
    row_idxs = np.arange(n_rows)
    try:
        col4row, row4col, v = lapjv(cost_matrix)
    except ValueError as e:
        if str(e) == "cost matrix is infeasible":
            return np.full((n_rows, n_cols), np.inf)
        else:
            raise e

    # Column vector of costs of each assignment in the lsap solution.
    lsap_costs = cost_matrix[row_idxs, col4row]
    lsap_total_cost = lsap_costs.sum()

    # Find the two minimum-cost columns for each row
    best_col_idxs = np.argmin(cost_matrix, axis=1)
    best_col_vals = cost_matrix[row_idxs, best_col_idxs]
    cost_matrix[row_idxs, best_col_idxs] = np.inf
    second_best_col_idxs = np.argmin(cost_matrix, axis=1)
    second_best_col_vals = cost_matrix[row_idxs, second_best_col_idxs]
    cost_matrix[row_idxs, second_best_col_idxs] = np.inf
    third_best_col_idxs = np.argmin(cost_matrix, axis=1)
    cost_matrix[row_idxs, best_col_idxs] = best_col_vals
    cost_matrix[row_idxs, second_best_col_idxs] = second_best_col_vals

    # When a row has its column stolen by a constraint, these are the columns
    # that might come into play when we are forced to resolve the assignment.
    if n_rows < n_cols:
        # unused = col_idxs[~np.isin(col_idxs, col4row)]
        # unused = np.setdiff1d(np.arange(n_cols), col4row, assume_unique=True)
        # first_unused = np.argmin(cost_matrix[:, unused], axis=1)
        # potential_cols = np.union1d(col4row, unused[first_unused])
        used_cost_matrix = cost_matrix[:, col4row]
        cost_matrix[:, col4row] = np.inf
        first_unused = np.argmin(cost_matrix, axis=1)
        potential_cols = np.union1d(col4row, first_unused)
        cost_matrix[:, col4row] = used_cost_matrix
    else:
        potential_cols = np.arange(n_cols)

    # When we add the constraint assigning row i to column j, lsap_col_idxs[i]
    # is freed up. If lsap_col_idxs[i] cannot improve on the cost of one of the
    # other row assignments, it does not need to be reassigned to another row.
    # If additionally column j is not in lsap_col_idxs, it is not taken away
    # from any of the other row assignments. In this situation, the resulting
    # total assignment costs are:
    total_costs = lsap_total_cost - lsap_costs[:, None] + cost_matrix

    for i, freed_j in enumerate(col4row):
        # When row i is constrained to another column, can column j be
        # reassigned to improve the assignment cost of one of the other rows?
        # To deal with that, we solve the lsap with row i omitted. For the
        # majority of constraints on row i's assignment, this will not conflict
        # with the constraint. When it does conflict, we fix the issue later.

        sub_ind = ~one_hot(i, n_rows)

        freed_col_costs = cost_matrix[:, freed_j]
        # If the freed up column does not contribute to lowering the costs of any
        # other rows, simply use the current assignments.
        if np.any(freed_col_costs < lsap_costs):
            # Need to solve the subproblem in which one row is removed
            new_row4col, new_col4row, new_v = lap.solve_lsap_with_removed_row(
                cost_matrix, i, row4col, col4row, v, modify_val=False
            )

            sub_total_cost = cost_matrix[sub_ind, new_col4row[sub_ind]].sum()

            # This calculation will end up being wrong for the columns in
            # lsap_col_idxs[sub_col_ind]. This is because the constraint in
            # row i in these columns will conflict with the sub assignment.
            # These miscalculations are corrected later.
            total_costs[i, :] = cost_matrix[i, :] + sub_total_cost
        else:
            new_row4col, new_col4row, new_v = (
                row4col,
                col4row.copy(),
                v,
            )

        new_col4row[i] = -1  # Row i is having a constraint applied.

        # new_col4row now contains the optimal assignment columns ignoring row i.

        # TODO: np.setdiff1d is very expensive.
        # new_col4row[i] = np.setdiff1d(col4row, new_col4row, assume_unique=True)[0]
        new_col4row[i] = set(col4row).difference(set(new_col4row)).pop()
        total_costs[i, new_col4row[i]] = cost_matrix[row_idxs, new_col4row].sum()

        # A flag that indicates if solve_lsap_with_removed_col has been called.
        flag_removed_col = False

        for other_i, stolen_j in enumerate(new_col4row):
            if other_i == i:
                continue

            # if not np.isfinite(cost_matrix[i, stolen_j]):
            #     total_costs[i, stolen_j] = cost_matrix[i, stolen_j]
            #     continue

            # Row i steals column stolen_j from other_i because of constraint.
            new_col4row[i] = stolen_j

            # Row other_i must find a new column. What is its next best option?
            best_j, second_best_j, third_best_j = (
                best_col_idxs[other_i],
                second_best_col_idxs[other_i],
                third_best_col_idxs[other_i],
            )

            # Note: Problem might occur if we have two j's that are both next
            # best, but one is not in col_idxs and the other is in col_idxs.
            # In this case, choosing the one not in col_idxs does not necessarily
            # give us the optimal assignment.
            # TODO: make the following if-else prettier.

            if (
                best_j != stolen_j
                and best_j not in new_col4row
                and (
                    cost_matrix[other_i, best_j] != cost_matrix[other_i, second_best_j]
                    or second_best_j not in new_col4row
                )
            ):
                new_col4row[other_i] = best_j
                total_costs[i, stolen_j] = cost_matrix[row_idxs, new_col4row].sum()
            elif second_best_j not in new_col4row and (
                cost_matrix[other_i, second_best_j]
                != cost_matrix[other_i, third_best_j]
                or third_best_j not in new_col4row
            ):
                new_col4row[other_i] = second_best_j
                total_costs[i, stolen_j] = cost_matrix[row_idxs, new_col4row].sum()
            else:
                # If this is the first time solve_lsap_with_removed_col is called
                # we initialize a bunch of variables
                if not flag_removed_col:
                    # Otherwise, solve the lsap with stolen_j removed
                    sub_sub_cost_matrix = cost_matrix[sub_ind, :][:, potential_cols]

                    sub_j = list(potential_cols).index(stolen_j)

                    sub_new_col4row = new_col4row[sub_ind]
                    sub_new_col4row = np.where(
                        sub_new_col4row.reshape(sub_new_col4row.size, 1)
                        == potential_cols
                    )[1]

                    # When we solve the lsap with row i removed, we update row4col accordingly.
                    sub_row4col = new_row4col.copy()
                    sub_row4col[sub_row4col == i] = -1
                    sub_row4col[sub_row4col > i] -= 1
                    sub_sub_row4col = sub_row4col[potential_cols]

                    sub_new_v = new_v[potential_cols]

                    flag_removed_col = True
                else:
                    sub_j = list(potential_cols).index(stolen_j)

                try:
                    _, new_new_col4row, _ = lap.solve_lsap_with_removed_col(
                        sub_sub_cost_matrix,
                        sub_j,
                        sub_sub_row4col,
                        sub_new_col4row,
                        sub_new_v,  # dual variable associated with cols
                        modify_val=False,
                    )
                    total_costs[i, stolen_j] = (
                        cost_matrix[i, stolen_j]
                        + sub_sub_cost_matrix[
                            np.arange(n_rows - 1), new_new_col4row
                        ].sum()
                    )
                except ValueError:
                    total_costs[i, stolen_j] = np.inf

            # Give other_i its column back in preparation for the next round.
            new_col4row[other_i] = stolen_j
            new_col4row[i] = -1

    # For those constraints which are compatible with the unconstrained lsap:
    total_costs[row_idxs, col4row] = lsap_total_cost

    return total_costs
