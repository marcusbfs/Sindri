def solve_quadratic(coefs):
    a, b, c = coefs
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        return None
    x1 = (-b + delta ** 0.5) / (2 * a)
    x2 = -b / a - x1
    ret = [x1, x2]
    return ret


def solve_cubic(coefs):
    a, b, c, d = coefs
    tol = 1e-8

    def newton(x):
        return (a * x ** 3 + b * x ** 2 + c * x + d) / (3 * a * x ** 2 + 2 * b * x + c)

    x0 = 1.0
    err = 1
    while err > tol:
        x0l = x0 - newton(x0)
        err = abs(x0l - x0)
        x0 = x0l

    xs = solve_quadratic((a, b + a * x0, c + b * x0 + a * x0 ** 2))
    if xs is not None:
        ret = [x0] + xs
    else:
        ret = [x0]
    return ret
