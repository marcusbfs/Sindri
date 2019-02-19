from polyEqSolver import solve_quadratic, solve_cubic
import numpy as np


def test_quadratic_solver():
    parameters = (0.4, -0.2, -0.1)
    expected = np.array([0.8090169943749475, -0.30901699437494745])
    returned = solve_quadratic(parameters)
    np.testing.assert_almost_equal(expected, returned)


def test_quadratic_solver():
    parameters = (2, -4, -22, 24)
    expected = np.array([1, 4, -3])
    returned = solve_cubic(parameters)
    np.testing.assert_almost_equal(expected, returned)
