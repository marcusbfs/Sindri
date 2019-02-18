from collections import namedtuple


def antoineVP(T, A, B, C, Tmin, Tmax):
    """Returns the vapor pressure at T temperature using the Antoine equation.

    Apply the Antoine equation:
        log10(P) = A - B/(T + C - 273.15)
    where P is the vapor pressure, bar, T is the temperature, K, and A, B and C are the Antoine parameters.
    Tmin and Tmax gives the range in which the Antoine equation is valid.

    Parameters
    ----------
    T : float
        Temperature in Kelvin used to calculate the vapor pressure.
    A, B, C : float
        Antoine equation parameters.
    Tmin : float
        Lower bound temperature to Antoine equation.
    Tmax : float
        Higher bound temperature to Antoine equation.

    Returns
    -------
    retval : namedtuple
        Namedtuple containing information.
    retval.Pvp : float
        Calculated vapor pressure at 'T', ginve in bar.
    retval.msg : None or str
        Returns a message warning of out of bounds calculation. If returned value is None, then there's no error.

    """
    msg = None
    ans = 10 ** (A - B / (T + C - 273.15))

    if T < Tmin:
        msg = "T < Tmin"
    elif T > Tmax:
        msg = "T > Tmax"

    retval = namedtuple("Pvp_antoine", ["Pvp", "msg"])
    ans = retval(ans, msg)

    return ans
