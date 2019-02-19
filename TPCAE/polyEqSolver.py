import numpy as np


def solve_quadratic(coefs):
    a, b, c = coefs
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        return np.array([])
    x1 = (-b + np.sqrt(delta)) / (2 * a)
    x2 = (-b - np.sqrt(delta)) / (2 * a)
    return np.array([x1, x2])


def solve_cubic(coefs):
    a, b, c, d = coefs
    tol = 1e-7

    def newton(x):
        return (a * x ** 3 + b * x ** 2 + c * x + d) / (3 * a * x ** 2 + 2 * b * x + c)

    x0 = 1.0
    err = 1
    while err > tol:
        x0l = x0 - newton(x0)
        err = np.abs(x0l - x0)
        x0 = x0l

    xs = solve_quadratic((a, b + a * x0, c + b * x0 + a * x0 ** 2))
    return np.concatenate((np.atleast_1d(x0), xs))
