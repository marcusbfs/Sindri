import numba
from numba import jit
from numpy import finfo

DBL_EPSILON = 10 * finfo(float).eps


@jit((numba.double, numba.double, numba.double), nopython=True, cache=True)
def solve_quadratic(a, b, c):

    if abs(a) < DBL_EPSILON:  # linear
        return [-c / b]

    delta = b ** 2 - 4 * a * c
    if delta < 0:
        return None
    x1 = (-b + delta ** 0.5) / (2 * a)
    x2 = -b / a - x1
    ret = [x1, x2]
    return ret


@jit(
    (numba.double, numba.double, numba.double, numba.double), nopython=True, cache=True
)
def solve_cubic(a, b, c, d):

    if abs(a) < DBL_EPSILON:  # quadratic
        ret = solve_quadratic(b, c, d)
        return ret

    x0 = 1.0
    err = 1
    k = 0
    kmax = 5000
    while err > DBL_EPSILON and k < kmax:
        x0l = x0 - (a * x0 ** 3 + b * x0 ** 2 + c * x0 + d) / (
            3 * a * x0 ** 2 + 2 * b * x0 + c
        )
        err = abs(x0l - x0)
        x0 = x0l
        k += 1

    xs = solve_quadratic(a, b + a * x0, c + b * x0 + a * x0 ** 2)
    if xs is not None:
        ret = [x0] + xs
    else:
        ret = [x0]
    return ret


# from numpy import finfo
# eps = finfo(float).eps
# @jit(nopython=True, cache=True)
# def solve_cubic(coefs):
#     a, b, c, d = coefs
#     if abs(a) < eps:
#         if abs(b) < eps:
#             # linear
#             return [-d / c]
#         else:
#             # quadratic
#             x0 = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
#             x1 = -b / a - x0
#             return [x0, x1]
#     # ok its cubic
#     delta = (
#         18 * a * b * c * d
#         - 4 * b * b * b * d
#         + b * b * c * c
#         - 4 * a * c * c * c
#         - 27 * a * a * d * d
#     )
#     p = (3 * a * c - b * b) / (3 * a * a)
#     q = (2 * b * b * b - 9 * a * b * c + 27 * a * a * d) / (27 * a * a * a)
#     if delta < 0:
#         # one real root
#         if 4 * p * p * p + 27 * q * q > 0 and p < 0:
#             t0 = (
#                 -2.0
#                 * abs(q)
#                 / (-p / 3.0) ** 0.5
#                 * cosh(
#                     1.0 / 3.0 * arccosh(-3.0 * abs(q) / (2.0 * p) * (-3.0 / p) ** 0.5)
#                 )
#             )
#         else:
#             t0 = (
#                 -2.0
#                 * (p / 3.0) ** 0.5
#                 * sinh(1.0 / 3.0 * arcsinh(3.0 * q / (2.0 * p) * (3.0 / p) ** 0.5))
#             )
#         x1 = t0 - b / (3 * a)
#         return [x1]
#     else:
#         # three real roots
#         t0 = (
#             2.0
#             * (-p / 3.0) ** 0.5
#             * cos(
#                 1.0 / 3.0 * arccos(3.0 * q / (2.0 * p) * (-3.0 / p) ** 0.5)
#                 - 0 * 2.0 * pi / 3.0
#             )
#         )
#         t1 = (
#             2.0
#             * (-p / 3.0) ** 0.5
#             * cos(
#                 1.0 / 3.0 * arccos(3.0 * q / (2.0 * p) * (-3.0 / p) ** 0.5)
#                 - 1 * 2.0 * pi / 3.0
#             )
#         )
#         t2 = (
#             2.0
#             * (-p / 3.0) ** 0.5
#             * cos(
#                 1.0 / 3.0 * arccos(3.0 * q / (2.0 * p) * (-3.0 / p) ** 0.5)
#                 - 2 * 2.0 * pi / 3.0
#             )
#         )
#         x0 = t0 - b / (3 * a)
#         x1 = t1 - b / (3 * a)
#         x2 = t2 - b / (3 * a)
#         return [x0, x1, x2]
