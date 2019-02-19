from collections import namedtuple
from units import conv_unit
import numpy as np


def leeKeslerVP(Pc, Tr, omega):
    """ Lee-Kesler correlation for estimating the vapor pressure.


    Parameters
    ----------
    Pc : float
        Critical pressure, in Pascal.
    Tr : float
        Reduced temperature, adimensional.
    omega : float
        Acentric factor, adimensinoal.

    Returns
    -------
    Pvp : float
        The estimated vapor pressure at T = Tc * Tr. The pressure is given in Pascal.

    """
    f0 = 5.92714 - 6.09648 / Tr - 1.28862 * np.log(Tr) + 0.169347 * Tr ** 6
    f1 = 15.2518 - 15.6878 / Tr - 13.4721 * np.log(Tr) + 0.43677 * Tr ** 6
    Pvpr = np.exp(f0 + omega * f1)
    Pvp = Pvpr * Pc
    return Pvp


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
        Calculated vapor pressure at 'T', given in Pascal.
    retval.msg : None or str
        Returns a message warning of out of bounds calculation. If returned value is None, then there's no error.

    """
    msg = None
    ans = 10 ** (A - B / (T + C - 273.15))
    P = conv_unit(ans, "bar", "Pa")

    if T < Tmin:
        msg = "T < Tmin"
    elif T > Tmax:
        msg = "T > Tmax"

    retval = namedtuple("Pvp_antoine", ["Pvp", "msg"])
    ans = retval(P, msg)

    return ans
