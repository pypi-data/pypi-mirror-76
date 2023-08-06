import numpy as np
import pytest

from laptools import clap

cost_matrices = []
global_cost_matrices = []

# fmt: off

# cost_matrix0-expected_global_costs0
cost_matrices.append(
    [[4, 1, 3],
     [2, 0, 5],
     [3, 2, 2]])

global_cost_matrices.append(
    [[6, 5, 6],
     [5, 6, 9],
     [6, 7, 5]])

# cost_matrix1-expected_global_costs1
cost_matrices.append(
    [[4, 1, 3, 6],
     [2, 0, 5, 7],
     [3, 2, 2, 8]])

global_cost_matrices.append(
    [[6, 5, 6, 8],
     [5, 6, 9, 10],
     [6, 7, 5, 11]])

# cost_matrix2-expected_global_costs2
cost_matrices.append(
    [[4, 1, 3],
     [2, 0, 5],
     [3, 2, 2],
     [6, 7, 8]])

global_cost_matrices.append(
    [[6, 5, 6],
     [5, 6, 9],
     [6, 7, 5],
     [8, 11, 11]])

# cost_matrix3-expected_global_costs3
cost_matrices.append(
    [[np.inf, np.inf, np.inf, np.inf,      3],
     [     7, np.inf,     23, np.inf, np.inf],
     [    17,     24, np.inf, np.inf, np.inf],
     [np.inf,      6,     13,     20, np.inf]])

global_cost_matrices.append(
    [[np.inf, np.inf, np.inf, np.inf,     47],
     [    47, np.inf,     49, np.inf, np.inf],
     [    49,     47, np.inf, np.inf, np.inf],
     [np.inf,     49,     47,     54, np.inf]])

# cost_matrix4-expected_global_costs4
cost_matrices.append(
    [[4, 1, 3, np.inf],
     [2, 0, 5, np.inf],
     [3, 2, 2, np.inf]])

global_cost_matrices.append(
    [[6, 5, 6, np.inf],
     [5, 6, 9, np.inf],
     [6, 7, 5, np.inf]])

# cost_matrix5-expected_global_costs5
cost_matrices.append(
    [[4     , 1     ,      3],
     [2     , 0     ,      5],
     [np.inf, np.inf, np.inf],
     [3     , 2     ,      2],
     [6     , 7     ,      8]])

global_cost_matrices.append(
    [[6, 5, 6],
     [5, 6, 9],
     [np.inf, np.inf, np.inf],
     [6, 7, 5],
     [8, 11, 11]])

# cost_matrix6-expected_global_costs6
cost_matrices.append(
    [[0     , 0,      0],
     [np.inf, 0, np.inf],
     [0     , 0,      0]])

global_cost_matrices.append(
    [[     0, np.inf,      0],
     [np.inf,      0, np.inf],
     [     0, np.inf,      0]])

# cost_matrix7-expected_global_costs7
cost_matrices.append(
    [[3, 8, 1, 3, 8],
     [2, 0, 6, 8, 9],
     [6, 7, 5, 8, 5],
     [6, 3, 8, 2, 0],
     [2, 9, 6, 6, 3]])

global_cost_matrices.append(
    [[13, 20, 10, 10, 17],
     [15, 10, 18, 18, 21],
     [12, 15, 10, 11, 10],
     [17, 16, 18, 10, 10],
     [10, 19, 15, 13, 12]])

# cost_matrix8-expected_global_costs8
cost_matrices.append(
    [[4,      1,      3],
     [2, np.inf, np.inf],
     [3, np.inf, np.inf]])

global_cost_matrices.append(
    [[np.inf, np.inf, np.inf],
     [np.inf, np.inf, np.inf],
     [np.inf, np.inf, np.inf]])

# fmt: on


class TestClap:
    # @pytest.mark.parametrize(
    #     "i, j, cost_matrix, expected",
    #     [
    #         (0, 0, cost_matrix_0, 6),
    #         (0, 1, cost_matrix_0, 5),
    #         (0, 2, cost_matrix_0, 6),
    #         (1, 0, cost_matrix_0, 5),
    #         (1, 1, cost_matrix_0, 6),
    #         (1, 2, cost_matrix_0, 9),
    #         (2, 0, cost_matrix_0, 6),
    #         (2, 1, cost_matrix_0, 7),
    #         (2, 2, cost_matrix_0, 5),
    #         (0, 3, cost_matrix_1, 8),
    #         (1, 3, cost_matrix_1, 10),
    #         (2, 3, cost_matrix_1, 11),
    #         (3, 0, cost_matrix_2, 8),
    #         (3, 1, cost_matrix_2, 11),
    #         (3, 2, cost_matrix_2, 11),
    #     ],
    # )
    # def test_clap_cost(self, i, j, cost_matrix, expected):
    #     """Verify clap.cost works on small examples computable by hand."""
    #     assert clap.cost(i, j, cost_matrix) == expected

    @pytest.mark.parametrize(
        "cost_matrix, expected_global_costs",
        list(zip(cost_matrices, global_cost_matrices)),
        # [
        #     (cost_matrix_0, global_cost_0),
        #     (cost_matrix_1, global_cost_1),
        #     (cost_matrix_2, global_cost_2),
        #     (cost_matrix_3, global_cost_3),
        #     (cost_matrix_4, global_cost_4),
        #     (cost_matrix_5, global_cost_5),
        #     (cost_matrix_6, global_cost_6),
        #     (cost_matrix_7, global_cost_7),
        #     (cost_matrix_8, global_cost_8),
        # ],
    )
    def test_clap_costs(self, cost_matrix, expected_global_costs):
        """Verify clap.constrained_lsap_costs works on small examples."""
        assert clap.costs(cost_matrix).tolist() == expected_global_costs

        # num_rows, num_cols = np.array(cost_matrix).shape
        # for i in range(num_rows):
        #     for j in range(num_cols):
        #         assert clap.cost(i, j, cost_matrix) == expected_global_costs[i, j]
