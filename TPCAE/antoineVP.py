from collections import namedtuple
import numpy as np


def antoineVP(T, A, B, C, Tmin, Tmax):
    """
    log10(Pvp) = A - B/(T + C - 273.15)

    :param T: Temperature, K
    :param A, B, C: Antoine paramaters
    :return: vapor pressure, bar
    """
    msg = None
    ans = 10 ** (A - B / (T + C - 273.15))

    # T = np.asarray(T)
    if T < Tmin:
        msg = "T < Tmin"
    elif T > Tmax:
        msg = "T > Tmax"

    retval = namedtuple('Pvp_antoine', ['Pvp', 'msg'])
    ans = retval(ans, msg)

    return ans


if __name__ == "__main__":
    A = 4.1199
    B = 1070.2
    C = 228.83
    T = 309.429
    ans = antoineVP(T, A, B, C, 0, 100)
    print(ans)
    print(type(ans))
