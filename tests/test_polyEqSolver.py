from polyEqSolver import *
import numpy as np


class TestCubicSolver:
    def test_no_real_roots(self):
        ret = solve_cubic(0, 1, 0, 1)
        assert ret is None

    def test_linear_solution(self):
        exp = [1.0]
        ret = solve_cubic(0, 0, 1, -1)
        np.testing.assert_allclose(exp, ret, 1e-8)

    def test_quadratic_solution(self):
        exp = [1.0, -1.0]
        ret = solve_cubic(0, 1, 0, -1)
        np.testing.assert_allclose(exp, ret, 1e-8)

    def test_cubic_solver(self):
        parameters = (2, -4, -22, 24)
        expected = np.array([1, 4, -3])
        returned = solve_cubic(*parameters)
        np.testing.assert_almost_equal(expected, returned)
