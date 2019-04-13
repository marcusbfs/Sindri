import abc

import numpy as np
import sympy as sp
from numba import njit, cfunc, types
from scipy import LowLevelCallable
from scipy.integrate import quad

from Properties import DeltaProp
from constants import R_IG, DBL_EPSILON
from polyEqSolver import solve_cubic


class CubicEOS(object):
    """
    This class is used for calculations of a pure substance properties using a Cubic Equation of State.
    """

    # def __init__(self, theta, b, delta, epsilon, eosDisplayName, eosinfo=""):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """ Initialize the EOS class.

        Parameters
        ----------
        name : str
            Name of the compound. This compound is going to be extracted from the database.
        formula : str
            Formula of the compound. This compound is going to be extracted from the database.
        eos : str
            Name of the cubic equation of state. This name must be equal one of the values from
            the 'eos_options' dictionary.

        """
        # eos : str, cubic equation of state name.
        self.T, self.V = sp.symbols("T V", real=True, positive=True)
        self.P = sp.symbols("P", real=True)
        self.b = None
        self.theta = None
        self.delta = None
        self.epsilon = None
        self.eosDisplayName = None
        self.eosInfo = None

    def _computeParameters(self):

        self.theta = sp.sympify(self.theta)
        self.b = sp.sympify(self.b)
        self.delta = sp.sympify(self.delta)
        self.epsilon = sp.sympify(self.epsilon)

        self.eosDisplayName = self.eosDisplayName
        self.eosInfo = self.eosInfo

        self._PsymbolicFromVT = R_IG * self.T / (self.V - self.b) - self.theta / (
            (self.V - self.b) * (self.V ** 2 + self.delta * self.V + self.epsilon)
        )
        self._ZsymbolicFromVT = self.V / (self.V - self.b) - (
            self.V * self.theta / (R_IG * self.T)
        ) / (self.V ** 2 + self.V * self.delta + self.epsilon)
        self._dZdTsymbolicFromVT = sp.diff(self._ZsymbolicFromVT, self.T)

        self._numf_ZfromVT = njit()(
            sp.lambdify([self.V, self.T], self._ZsymbolicFromVT, modules="numpy")
        )
        self._numf_dZdTfromVT = njit()(
            sp.lambdify([self.V, self.T], self._dZdTsymbolicFromVT, modules="numpy")
        )

        self._Bl = self.b * self.P / (R_IG * self.T)
        self._deltal = self.delta * self.P / (R_IG * self.T)
        self._thetal = self.theta * self.P / (R_IG * self.T) ** 2
        self._epsilonl = self.epsilon * (self.P / (R_IG * self.T)) ** 2

        # coefficients Z**3 + a0*Z**2 + a1*Z + a2 = 0
        self._a0 = self._deltal - self._Bl - 1
        self._a1 = self._thetal + self._epsilonl - self._deltal * (self._Bl + 1)
        self._a2 = -(self._epsilonl * (self._Bl + 1) + self._thetal * self._Bl)

        self._numf_a0 = njit()(sp.lambdify([self.P, self.T], self._a0, modules="numpy"))
        self._numf_a1 = njit()(sp.lambdify([self.P, self.T], self._a1, modules="numpy"))
        self._numf_a2 = njit()(sp.lambdify([self.P, self.T], self._a2, modules="numpy"))

        self.tmp_cfunc = None
        self.tmp_cfunc2 = None
        c_sig = types.double(types.intc, types.CPointer(types.double))

        exec(
            "self.tmp_cfunc = lambda n, data: {:s}".format(
                str((1 - self._ZsymbolicFromVT) / self.V)
                .replace("V", "data[0]")
                .replace("T", "data[1]")
                .replace("Abs", "np.abs")
                .replace("sign", "np.sign")
            )
        )
        qf = cfunc(c_sig)(self.tmp_cfunc)
        self._qnf = LowLevelCallable(qf.ctypes)

        exec(
            "self.tmp_cfunc2 = lambda n, data: {:s}".format(
                str(self.T * self._dZdTsymbolicFromVT / self.V)
                .replace("V", "data[0]")
                .replace("T", "data[1]")
                .replace("Abs", "np.abs")
                .replace("sign", "np.sign")
            )
        )
        tf = cfunc(c_sig)(self.tmp_cfunc2)
        self._numf_UR = LowLevelCallable(tf.ctypes)

    def getP(self, _V: float, _T: float):
        return np.real(self._numf_ZfromVT(_V, _T) * _T * R_IG / _V)

    def getZfromPT(self, _P: float, _T: float):
        a = 1.0
        b = np.real(self._numf_a0(_P, _T))
        c = np.real(self._numf_a1(_P, _T))
        d = np.real(self._numf_a2(_P, _T))
        roots = np.asarray(solve_cubic(a, b, c, d))
        real_values = roots[roots > 0]
        return real_values

    def getVfromPT(self, _P: float, _T: float):
        Zs = self.getZfromPT(_P, _T)
        return Zs * R_IG * _T / _P

    def getEOSDisplayName(self):
        return self.eosDisplayName

    def getEOSInfo(self):
        return self.eosInfo

    def getDepartureProps(
        self, _P: float, _T: float, _V: float, _Z: float
    ) -> DeltaProp:
        # calculate UR
        UR_RT = quad(self._numf_UR, _V, np.inf, args=(_T,))[0]
        UR = UR_RT * _T * R_IG
        # calculate AR
        AR_RT = quad(self._qnf, _V, np.inf, args=(_T,))[0] + np.log(_Z)
        # AR_RT = quad(self.numf_integratePvp, _V, np.inf, args=(_T,))[0] + np.log(_Z)
        AR = AR_RT * _T * R_IG
        # calculate HR
        HR_RT = UR_RT + 1.0 - _Z
        HR = HR_RT * R_IG * _T
        # calculate SR
        SR_R = UR_RT - AR_RT
        SR = SR_R * R_IG
        # calculate GR
        GR_RT = AR_RT + 1 - _Z
        GR = GR_RT * R_IG * _T

        ret = DeltaProp(0, HR, SR, GR, UR, AR)
        return ret

    def getDeltaDepartureProps(
        self,
        _Pref: float,
        _Tref: float,
        _Vref: float,
        _Zref: float,
        _P: float,
        _T: float,
        _V: float,
        _Z: float,
    ) -> DeltaProp:
        ref = self.getDepartureProps(_Pref, _Tref, _Vref, _Zref)
        state = self.getDepartureProps(_P, _T, _V, _Z)
        delta = state.subtract(ref)
        return delta

    def getCoefFugacity(self, _P: float, _T: float, _V: float, _Z: float) -> float:
        lnphi = _Z - 1.0 - (quad(self._qnf, _V, np.inf, args=(_T,))[0] + np.log(_Z))
        return np.e ** lnphi

    def getFugacity(self, _P: float, _T: float, _V: float, _Z: float) -> float:
        phi = self.getCoefFugacity(_P, _T, _V, _Z)
        f = _P * phi
        return f

    def getPvp(self, _T: float, _P: float, tol=DBL_EPSILON, kmax=100):
        for i in range(1, kmax + 1):
            Zs = self.getZfromPT(_P, _T)
            Zl, Zv = np.min(Zs), np.max(Zs)
            Vl, Vv = Zl * R_IG * _T / _P, Zv * R_IG * _T / _P

            fL = self.getFugacity(_P, _T, Vl, Zl)
            fV = self.getFugacity(_P, _T, Vv, Zv)
            _P = _P * fL / fV
            error = fL / fV - 1.0
            if np.abs(error) < tol:
                return _P, i
        return _P, i
