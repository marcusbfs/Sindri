from numba import jit, float64

from constants import DBL_EPSILON


@jit((float64, float64, float64), nopython=True, cache=True)
def solve_quadratic(a, b, c):
    """
    Solves the real roots of a quadratic equation.

    Solves the real root of the equation
        a*x^2 + b*x + c = 0

    Parameters
    ----------
    a : float
    b : float
    c : float

    Returns
    -------
    ret : list of floats or None
        list of floats containing all roots of the equation. If no real roots are found,
        returns None.

    """

    if abs(a) < DBL_EPSILON:  # linear
        return [-c / b]

    delta = b ** 2 - 4 * a * c
    if abs(delta) < DBL_EPSILON:
        x1 = (-b) / (2 * a)
        ret = [x1, x1]
        return ret
    elif delta > 0:
        x1 = (-b + delta ** 0.5) / (2 * a)
        x2 = -b / a - x1
        ret = [x1, x2]
        return ret
    else:
        return


# @jit((float64, float64, float64, float64, Omitted(float64)), nopython=True, cache=True)
@jit(nopython=True, cache=True)
def solve_cubic(a, b, c, d, x0=1.0):
    """
    Solves the real roots of a cubic equation.

    Solves the real root of the equation
        a*x^3 + b*x^2 + c*x + d = 0

    Parameters
    ----------
    a : float
    b : float
    c : float
    d : float
    x0 : float
        initial guess for finding the first root using Newton-Raphson method

    Returns
    -------
    ret : list of floats or None
        list of floats containing all roots of the equation. If no real roots are found,
        returns None.

    """

    if abs(a) < DBL_EPSILON:  # quadratic
        ret = solve_quadratic(b, c, d)
        return ret

    err = 1
    k = 0
    kmax = 5000
    while err > DBL_EPSILON and k < kmax:  # newton method
        # x0l = x0 - (a * x0 ** 3 + b * x0 ** 2 + c * x0 + d) / (
        #     3 * a * x0 ** 2 + 2 * b * x0 + c
        # )
        x0l = (x0 * x0 * (2.0 * a * x0 + b) - d) / (x0 * (3.0 * a * x0 + 2.0 * b) + c)
        err = abs(x0l - x0)
        x0 = x0l
        k += 1

    # xs = solve_quadratic(a, b + a * x0, c + b * x0 + a * x0 ** 2)
    xs = solve_quadratic(a, b + a * x0, c + x0 * (b + a * x0))
    if xs is not None:
        ret = [x0] + xs
    else:
        ret = [x0]
    return ret


# @jit((float64, float64, float64, float64), nopython=True, cache=True)
# def solve_cubic(a, b, c, d):
#     if
#
#
#
#     np.abs(a) < 10 * DBL_EPSILON:
#         if np.abs(b) < 10 * DBL_EPSILON:
#             # // Linear solution if a = 0 and b = 0
#             x0 = -d / c
#             return [x0]
#
#         else:
#             # // Quadratic solution(s) if a = 0 and b != 0
#             x0 = (-c + np.sqrt(c * c - 4 * b * d)) / (2 * b)
#             x1 = (-c - np.sqrt(c * c - 4 * b * d)) / (2 * b)
#             return [x0, x1]
#
#     # // Ok, it is really a cubic
#
#     # // Discriminant
#     DELTA = (
#             18 * a * b * c * d
#             - 4 * b * b * b * d
#             + b * b * c * c
#             - 4 * a * c * c * c
#             - 27 * a * a * d * d
#     )
#     # // Coefficients for the depressed cubic t^3+p*t+q = 0
#     p = (3 * a * c - b * b) / (3 * a * a)
#     q = (2 * b * b * b - 9 * a * b * c + 27 * a * a * d) / (27 * a * a * a)
#
#     if DELTA < 0:
#
#         # // One real root
#         if 4 * p * p * p + 27 * q * q > 0 and p < 0:
#
#             t0 = (
#                     -2.0
#                     * np.abs(q)
#                     / q
#                     * np.sqrt(-p / 3.0)
#                     * np.cosh(
#                 1.0
#                 / 3.0
#                 * np.arccosh(-3.0 * np.abs(q) / (2.0 * p) * np.sqrt(-3.0 / p))
#             )
#             )
#
#         else:
#
#             t0 = (
#                     -2.0
#                     * np.sqrt(p / 3.0)
#                     * np.sinh(
#                 1.0 / 3.0 * np.arcsinh(3.0 * q / (2.0 * p) * np.sqrt(3.0 / p))
#             )
#             )
#
#         x0 = t0 - b / (3 * a)
#         x1 = t0 - b / (3 * a)
#         x2 = t0 - b / (3 * a)
#         return [x0, x1, x2]
#
#     else:  # //(DELTA>0)
#
#         # // Three real roots
#         t0 = (
#                 2.0
#                 * np.sqrt(-p / 3.0)
#                 * np.cos(
#             1.0 / 3.0 * np.arccos(3.0 * q / (2.0 * p) * np.sqrt(-3.0 / p))
#             - 0 * 2.0 * np.pi / 3.0
#         )
#         )
#         t1 = (
#                 2.0
#                 * np.sqrt(-p / 3.0)
#                 * np.cos(
#             1.0 / 3.0 * np.arccos(3.0 * q / (2.0 * p) * np.sqrt(-3.0 / p))
#             - 1 * 2.0 * np.pi / 3.0
#         )
#         )
#         t2 = (
#                 2.0
#                 * np.sqrt(-p / 3.0)
#                 * np.cos(
#             1.0 / 3.0 * np.arccos(3.0 * q / (2.0 * p) * np.sqrt(-3.0 / p))
#             - 2 * 2.0 * np.pi / 3.0
#         )
#         )
#
#         x0 = t0 - b / (3 * a)
#         x1 = t1 - b / (3 * a)
#         x2 = t2 - b / (3 * a)
#         return [x0, x1, x2]
