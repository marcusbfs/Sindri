from collections import namedtuple
import numpy as np
import sympy as sp
from scipy.integrate import quad

import matplotlib.pyplot as plt
from constants import R_IG
from db_utils import get_compound_properties
from units import conv_unit

eos_options = {
    "van der Waals (1890)": "van_der_waals_1890",
    "Redlich and Kwong (1949)": "redlich_and_kwong_1949",
    "Wilson (1964)": "wilson_1964",
    "Soave (1972)": "soave_1972",
    "Peng and Robinson (1976)": "peng_and_robinson_1976",
    # "Fuller (1976)": "fuller_1976",
    "Schmidt and Wenzel (1979)": "schmidt_and_wenzel_1979",
    "Péneloux, et al. (1982)": "peneloux_et_al_1982",
    "Patel and Teja (1982)": "patel_and_teja_1982",
    "Adachi, et al. (1983)": "adachi_et_al_1983",
    # "Mathias and Copeman (1983)": "mathias_and_copeman_1983",
    "Soave (1984)": "soave_1984",
    "Adachi, et al. (1985)": "adachi_et_al_1985",
    "Twu, et al. (1995)": "twu_et_al_1995",
    "Gasem, et al. PR modification (2001)": "gasem_et_al_pr_2001",
    "Gasem, et al. Twu modificaton (2001)": "gasem_et_al_twu_2001",
}


class EOS:
    """
    This class is used for calculations of a pure substance properties using a Cubic Equation of State.
    """

    def __init__(self, name, formula, eos):
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
        self.eos = eos.lower()
        # compound : dictionary containing the values extracted from the database.
        self.compound = get_compound_properties(name, formula)
        # Tc : float, critical temperature of the compound in Kelvin.
        self.Tc = self.compound["Tc_K"]
        # Pc : float, critical pressure of the compound in Pascal.
        self.Pc = conv_unit(self.compound["Pc_bar"], "bar", "Pa")
        # Zc : float, critical ompressibility factor, adimensional. Defined as Zc = Pc*Vc/(R_IG*Tc).
        self.Zc = self.compound["Zc"]
        # Vc : float, critical molar volume of the compound, in cm3/mol.
        self.Vc = self.compound["Vc_cm3/mol"]
        # omega : float, acentric factor of the compound, adimensinoal.
        self.omega = self.compound["omega"]

        # V : volume and temperature variables for symbolic math.
        self.V, self.T = sp.symbols("V T", real=True, positive=True)
        # P : pressure variable for symbolic math.
        self.P = sp.symbols("P", real=True)

        self.Z, self.deltal, self.Bl, self.thetal, self.epsilonl = sp.symbols(
            "Z deltal Bl thetal epsilonl", real=True
        )

        self.Z_V_T = None
        self.Z_P_T = None

        self.initialize()

        self.return_Z_V_T()
        self.return_Z_P_T()

        self.eos_options = eos_options

    def show_eos_options(self):
        r = list(self.eos_options.keys())
        # print(r)
        return r

    def initialize(self):
        """ Get the correct parameters for the cubic equation of state selected.

        The parameters are  'b', 'theta', 'delta' and 'epsilon'. The equation has the form:
            P = R * T / (V - b) - theta / (V**2 + delta * V + epsilon)
        where:
            theta = a * alpha
        This equation was taken from Poling, 2002.

        """
        self.Tr = self.T / self.Tc
        self.Pc_RTc = self.Pc / (R_IG * self.Tc)

        if self.eos == "van_der_waals_1890":
            self.a = 0.42188 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = 0.125 / self.Pc_RTc
            self.delta = 0.0
            self.epsilon = 0.0
            self.alpha = 1.0
            self.theta = self.a

        elif self.eos == "redlich_and_kwong_1949":
            self.a = 0.42748 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = 0.08664 / self.Pc_RTc
            self.delta = 0.08664 / self.Pc_RTc
            self.epsilon = 0.0
            self.alpha = 1.0 / self.Tr ** 0.5
            self.theta = self.a / self.Tr ** 0.5

        elif self.eos == "wilson_1964":
            self.a = 0.42748 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = 0.08664 / self.Pc_RTc
            self.delta = self.b
            self.epsilon = 0.0
            self.alpha = self.Tr * (
                1 + (1.57 + 1.62 * self.omega) * (1.0 / self.Tr - 1.0)
            )
            self.theta = self.a * self.alpha

        elif self.eos == "soave_1972":
            self.a = 0.42748 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = 0.08664 / self.Pc_RTc
            self.delta = self.b
            self.epsilon = 0.0
            self.alpha = (
                1.0
                + (0.48 + 1.574 * self.omega - 0.176 * self.omega ** 2)
                * (1.0 - self.Tr ** 0.5)
            ) ** 2
            self.theta = self.a * self.alpha

        elif self.eos == "peng_and_robinson_1976":
            self.a = 0.45724 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = 0.07780 / self.Pc_RTc
            self.delta = 0.15559 / self.Pc_RTc
            self.epsilon = -0.006053 / self.Pc_RTc ** 2
            self.alpha = (
                1.0
                + (0.37464 + 1.54226 * self.omega - 0.2699 * self.omega ** 2)
                * (1.0 - self.Tr ** 0.5)
            ) ** 2
            self.theta = self.a * self.alpha

        # elif self.eos == "fuller_1976":
        #     beta = self.b / self.V
        #     c = (sp.sqrt(1 / beta - 3 / 4) - 3 / 2) / beta
        #     omegab = beta * ((1 - beta) * (2 + c * beta) - (1 + c * beta)) / ((2 + c * beta) * (1 - beta) ** 2)
        #     omegaa = omegab * (1 + c * beta) ** 2 / (beta * (1 - beta) ** 2 * (2 + c * beta))
        #     self.b = omegab * R_IG * self.Tc / self.Pc
        #     self.a = omegaa * R_IG ** 2 * self.Tc / self.Pc
        #     m = .48 + 1.574 * self.omega - .176 * self.omega ** 2
        #     q = m * (beta / .26) ** .25
        #     self.alpha = (1 + q * (1 - self.Tr ** .5)) ** 2
        #     self.delta = c * self.b
        #     self.epsilon = 0
        #     self.theta = self.a * self.alpha

        elif self.eos == "schmidt_and_wenzel_1979":

            w = -self.omega * 3
            u = 1 - w
            r = np.roots([6 * self.omega + 1, 3, 3, -1])
            beta_c = np.min(r[r >= 0])
            zeta_c = 1 / (3 * (1 + beta_c * self.omega))

            omega_b = beta_c * zeta_c
            omega_a = (1 - zeta_c * (1 - beta_c)) ** 3

            self.b = omega_b * R_IG * self.Tc / self.Pc
            ac = omega_a * (R_IG * self.Tc) ** 2 / self.Pc

            k0 = 0.465 + 1.347 * self.omega - 0.528 * self.omega ** 2
            k = k0 + (5 * self.Tr - 3 * k0 - 1) ** 2 / 70
            self.alpha = (1 + k * (1 - self.Tr ** 0.5)) ** 2

            self.delta = self.b * u
            self.epsilon = w * self.b ** 2
            self.theta = ac * self.alpha

        elif self.eos == "peneloux_et_al_1982":
            self.a = 0.42748 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = 0.08664 / self.Pc_RTc
            c = 0.40768 * (R_IG * self.Tc / self.Pc) * (0.00385 + 0.08775 * self.omega)
            self.delta = self.b + 2 * c
            self.epsilon = c * (self.b + c)
            self.alpha = (
                1.0
                + (0.48 + 1.574 * self.omega - 0.176 * self.omega ** 2)
                * (1.0 - self.Tr ** 0.5)
            ) ** 2
            self.theta = self.a * self.alpha

        elif self.eos == "patel_and_teja_1982":
            F = 0.45241 + 1.30982 * self.omega - 0.295937 * self.omega ** 2
            zeta_c = 0.32903 - 0.076799 * self.omega + 0.0211947 * self.omega ** 2

            r = np.roots([1, 2 - 3 * zeta_c, 3 * zeta_c ** 2, -zeta_c ** 3])
            omega_b = np.min(r[r >= 0])
            omega_c = 1 - 3 * zeta_c
            omega_a = (
                3 * zeta_c ** 2
                + 3 * (1 - 2 * zeta_c) * omega_b
                + omega_b ** 2
                + 1
                - 3 * zeta_c
            )

            c = omega_c * R_IG * self.Tc / self.Pc
            self.b = omega_b * R_IG * self.Tc / self.Pc
            self.alpha = (1 + F * (1 - self.Tr ** 0.5)) ** 2
            self.a = omega_a * (R_IG * self.Tc) ** 2 / self.Pc

            self.delta = self.b + c
            self.epsilon = -self.b * c
            self.theta = self.a * self.alpha

        elif self.eos == "adachi_et_al_1983":
            b1 = (
                R_IG
                * self.Tc
                * (0.08974 - 0.03452 * self.omega + 0.00330 * self.omega ** 2)
                / self.Pc
            )
            b2 = (
                R_IG
                * self.Tc
                * (
                    0.03686
                    + 0.00405 * self.omega
                    - 0.01073 * self.omega ** 2
                    + 0.00157 * self.omega ** 3
                )
                / self.Pc
            )
            b3 = (
                R_IG
                * self.Tc
                * (
                    0.154
                    + 0.14122 * self.omega
                    - 0.00272 * self.omega ** 2
                    - 0.00484 * self.omega ** 3
                )
                / self.Pc
            )

            self.a = (
                (R_IG * self.Tc) ** 2
                * (
                    0.44869
                    + 0.04024 * self.omega
                    + 0.01111 * self.omega ** 2
                    - 0.00576 * self.omega ** 3
                )
                / self.Pc
            )
            self.b = b1
            self.delta = b3 - b2
            self.epsilon = -b2 * b3
            self.alpha = (
                1
                + (0.407 + 1.3787 * self.omega - 0.2933 * self.omega ** 2)
                * (1.0 - self.Tr ** 0.5)
            ) ** 2
            self.theta = self.a * self.alpha

        # elif self.eos == "mathias_and_copeman_1983":
        #     self.a = .42748 * (R_IG * self.Tc) ** 2 / self.Pc
        #     self.b = .08664 / self.Pc_RTc
        #     self.delta = self.b
        #     self.epsilon = 0.
        #     c1 = 0.5178 + 1.6054 * self.omega - .1094 * self.omega ** 2
        #     c2 = .3279 - .4291 * self.omega
        #     c3 = .4866 + 1.3506 * self.omega
        #     self.alpha = (1 + c1 * (1 - self.Tr ** .5) + c2 * (1 - self.Tr ** .5) ** 2 + c3 * (
        #             1 - self.Tr ** 2) ** 3) ** 2
        #     self.theta = self.a * self.alpha

        elif self.eos == "soave_1984":
            self.a = 0.42188 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = 0.08333 / self.Pc_RTc
            self.delta = self.b
            self.epsilon = 0.001736 / self.Pc_RTc ** 2
            self.alpha = (
                1.0
                + (
                    0.4998
                    + 1.5928 * self.omega
                    - 0.19563 * self.omega ** 2
                    + 0.025 * self.omega ** 3
                )
                * (1.0 - self.Tr ** 0.5)
            ) ** 2
            self.theta = self.a * self.alpha

        elif self.eos == "adachi_et_al_1985":
            self.a = (
                (R_IG * self.Tc) ** 2
                * (
                    0.43711
                    + 0.02366 * self.omega
                    + 0.10538 * self.omega ** 2
                    + 0.10164 * self.omega ** 3
                )
                / self.Pc
            )
            self.b = (
                (R_IG * self.Tc)
                * (
                    0.08779
                    - 0.02181 * self.omega
                    - 0.06708 * self.omega ** 2
                    + 0.10617 * self.omega ** 3
                )
                / self.Pc
            )
            c = (
                (R_IG * self.Tc)
                * (
                    0.0506
                    + 0.04184 * self.omega
                    + 0.16413 * self.omega ** 2
                    - 0.03975 * self.omega ** 3
                )
                / self.Pc
            )
            self.delta = 2 * c
            self.epsilon = -c ** 2
            self.alpha = (
                1
                + (
                    0.4406
                    + 1.7039 * self.omega
                    - 1.729 * self.omega ** 2
                    + 0.9929 * self.omega ** 3
                )
                * (1 - self.Tr ** 0.5)
            ) ** 2
            self.theta = self.a * self.alpha

        elif self.eos == "twu_et_al_1995":
            self.b = (R_IG * self.Tc) * 0.0777960739039 / self.Pc
            self.delta = 2 * self.b
            self.epsilon = -self.b ** 2
            self.a = (R_IG * self.Tc) ** 2 * 0.457235528921 / self.Pc
            alpha0 = self.Tr ** (-0.171813) * sp.exp(
                0.125283 * (1 - self.Tr ** 1.77634)
            )
            alpha1 = self.Tr ** (-0.607352) * sp.exp(
                0.511614 * (1 - self.Tr ** 2.20517)
            )
            self.alpha = alpha0 + self.omega * (alpha1 - alpha0)
            self.theta = self.a * self.alpha

        elif self.eos == "gasem_et_al_pr_2001":
            self.a = 0.45724 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = 0.07780 / self.Pc_RTc
            self.delta = 2 * self.b
            self.epsilon = -self.b ** 2
            self.alpha = (
                1.0
                + (0.386590 + 1.50226 * self.omega - 0.1687 * self.omega ** 2)
                * (1.0 - self.Tr ** 0.5)
            ) ** 2
            self.theta = self.a * self.alpha

        elif self.eos == "gasem_et_al_twu_2001":
            self.a = 0.45724 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = 0.07780 / self.Pc_RTc
            self.delta = 2 * self.b
            self.epsilon = -self.b ** 2
            alpha0 = self.Tr ** (-0.207176) * sp.exp(
                0.092099 * (1 - self.Tr ** (1.94800))
            )
            alpha1 = self.Tr ** (-0.502297) * sp.exp(
                0.603486 * (1 - self.Tr ** (2.09626))
            )
            self.alpha = alpha0 + self.omega * (alpha1 - alpha0)
            self.theta = self.a * self.alpha

        self.return_Z_V_T()
        self.return_Z_P_T()

    def return_Z_V_T(self):
        """
        Creates the symbolic equation
            Z = V / (V - b) - ((theta / (R_IG * T)) * V) / (V**2 + delta * V + epsilon)

        Returns
        -------
        self.Z_V_T : sympy symbolic expression.

        """
        if self.Z_V_T is None:
            self.Z_V_T = self.V / (self.V - self.b) - (
                (self.theta / (R_IG * self.T) * self.V * (self.V - self.b))
            ) / ((self.V - self.b) * (self.V ** 2 + self.delta * self.V + self.epsilon))
        return self.Z_V_T

    def return_Z_P_T(self):
        """
        Creates a cubic equation in Z.

        Returns
        -------
        self.Z_P_T : sympy symbolic expression.

        """
        if self.Z_P_T is None:
            self.eos_eq = (
                self.Z ** 3
                + (self.deltal - self.Bl - 1) * self.Z ** 2
                + self.Z * (self.thetal + self.epsilonl - self.deltal * (self.Bl + 1))
                - (self.epsilonl * (self.Bl + 1) + self.Bl * self.thetal)
            )
            self.eos_eq = self.eos_eq.subs(self.Bl, self.b * self.P / (R_IG * self.T))
            self.eos_eq = self.eos_eq.subs(
                self.deltal, self.delta * self.P / (R_IG * self.T)
            )
            self.eos_eq = self.eos_eq.subs(
                self.thetal, self.theta * self.P / (R_IG * self.T) ** 2
            )
            self.Z_P_T = self.eos_eq.subs(
                self.epsilonl, self.epsilon * (self.P / (R_IG * self.T)) ** 2
            )
        return self.Z_P_T

    def return_Z_given_PT(self, _P, _T):
        """ return the positive roots (Z) of the cubic equation.

        parameters
        ----------
        _p : float
            pressure, pa.
        _t : float
            temperature, k.

        returns
        -------
        ans : array, float
            returns an array of the real roots of the cubic equation of state. the minimum value of this array
            corresponds to the vapor state, while the maximum value corresponds to the liquid state.

        """
        f = sp.lambdify([self.P, self.T], self.return_Z_P_T(), modules="numpy")
        p = sp.Poly(f(_P, _T), self.Z).coeffs()

        r = np.roots(p)
        real_valued = r.real[abs(r.imag) < 1e-5]
        ans = real_valued[real_valued >= 0]
        if ans.size == 0:
            raise Exception("There are no positive real roots for Z")
        self.Zval = ans
        return ans

    def return_V_given_PT(self, _P, _T):
        """ Return the positive roots (V) of the cubic equation.

        Parameters
        ----------
        _P : float
            pressure, Pa.
        _T : float
            temperature, K.

        Returns
        -------
        ans : array, float
            Returns an array of the real roots of the cubic equation of state. The minimum value of this array
            corresponds to the vapor state, while the maximum value corresponds to the liquid state.

        """
        ans = self.return_Z_given_PT(_P, _T) * R_IG * _T / _P
        self.Vval = ans
        return ans

    def return_departureProperties(self, _P, _T, _V, _Z):
        """
        Returns the enthalpy, entropy, Gibbs energy, internal energy, Helmholtz energy and fugacity at
        '_P' and '_T', utilizing departure functions from Poling (2002). All values are in the S.I. units.

        Parameters
        ----------
        _P : float
            pressure, Pa.
        _T : float
            temperature, K.
        _V : float
            molar volume, m3/mol.
        _Z : float
            compressibility factor, adimensional.

        Returns
        -------
        dict_ans : dictionary, float
            Returns a dictionary with the values of thermodynamics properties calculated using the departure
            functions. The dictionary keys are: 'HR', 'SR', 'GR', 'UR', 'AR', 'f'.

        """
        # calculate UR
        f_to_integrate = self.T * sp.diff(self.Z_V_T, self.T) / self.V
        f_to_integrate = sp.lambdify(
            self.V, f_to_integrate.subs(self.T, _T), modules="numpy"
        )
        UR_RT = quad(f_to_integrate, _V, np.inf)[0]
        UR = UR_RT * _T * R_IG
        # calculate AR
        f_to_integrate = (1 - self.Z_V_T) / self.V
        f_to_integrate = sp.lambdify(
            self.V, f_to_integrate.subs(self.T, _T), modules="numpy"
        )
        AR_RT = quad(f_to_integrate, _V, np.inf)[0] + np.log(_Z)
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

        fugacity = _P * np.e ** (-GR_RT)

        dict_ans = {"HR": HR, "SR": SR, "GR": GR, "UR": UR, "AR": AR, "f": fugacity}
        return dict_ans

    def return_delta_ResProperties(self, _Pref, _Tref, _Vref, _Zref, _P, _T, _V, _Z):
        ref = self.return_departureProperties(_Pref, _Tref, _Vref, _Zref)
        proc = self.return_departureProperties(_P, _T, _V, _Z)
        delta = np.array(list(proc.values())) - np.array(list(ref.values()))
        dict_delta = dict(zip(ref.keys(), delta))
        dict_delta["f"] = proc["f"]
        return dict_delta

    def return_Pvp_EOS(self, _T, initialP, tol=1e-4, k=50):
        """ Return the vapor pressure estimated at '_T', using the cubic equation of state.

        Estimates the vapor pressure by applying the liquid-vapor equilibrium condition: in this condition, the
        fugacity value of both states must be equal (fL = fV). This function returns the pressure value that
        satisfies this condition, given a tolerance. The fugacity values are calculated using the departure functions
        given by Poling (2002).

        Parameters
        ----------
        _T : float
            given temperature, in Kelvin, to estimate the vapor pressure..
        initialP : float
            initial pressure guess, in bar.
        tol : float, optional
            maximum tolerance for the error.
        k : int, optional
            maximum iterations value.

        Returns
        -------
        Pvp_EOS : namedtuple of (float, int, str or None)
            Pvp_EOS.Pvp : float
                The vapor pressure calculated, in Pascal.
            Pvp_EOS.iter : int
                The number of iterations needed to calculate Pvp_EOS.Pvp.
            Pvp_EOS.msg : str or None
                Returns a warning message if the calcualtes exceeds the maximum iterations value. Else, returns None.

        """
        _P = initialP

        f_to_integrate = (1 - self.Z_V_T) / self.V
        f_to_integrate = sp.lambdify(
            self.V, f_to_integrate.subs(self.T, _T), modules="numpy"
        )

        def _helper_f(hv, hz):
            return hz - 1.0 - np.log(hz) - quad(f_to_integrate, hv, np.inf)[0]

        PvpEOS = namedtuple("Pvp_EOS", ["Pvp", "iter", "msg"])

        for i in range(1, k + 1):
            Zs = self.return_Z_given_PT(_P, _T)
            Zl = np.min(Zs)
            Zv = np.max(Zs)
            Vl = Zl * R_IG * _T / _P
            Vv = Zv * R_IG * _T / _P

            fL = _P * np.e ** _helper_f(Vl, Zl)
            fV = _P * np.e ** _helper_f(Vv, Zv)
            _P = _P * fL / fV
            error = fL / fV - 1.0
            if abs(error) < tol:
                return PvpEOS(_P, i, None)

        return PvpEOS(_P, k, str(k) + " (max iterations)")

    def change_eos(self, new_eos):
        """ Change and update the cubic equation of state used by this class.

        This function updates the variables 'self.Z_V_T' and 'self.Z_P_T' using the new cubic equation of state
        paramaters.

        Parameters
        ----------
        new_eos : str
            New cubic equation of state name. This name must be a valid value from the 'eos_options' dictionary.

        """
        self.eos = new_eos.lower()
        self.Z_V_T = None
        self.Z_P_T = None
        self.initialize()

    def PV_diagrams(self, var, Punit, Vunit, Tunit, a, b, points, Ts):
        # TODO converter unidades antes
        Tfp = self.compound["Tfp_K"]  # freezing point temperature at 1 atm, K
        Tb = self.compound["Tb_K"]  # boiling temperature at 1 atm, K
        Tc = self.Tc
        Pc = self.Pc

        Tvec = np.linspace(Tfp, Tc, points)
        # # print(Tvec)
        #
        # check if compound has antoine coefs
        if self.compound["ANTOINE_A"] is not None:
            import antoineVP

            ant_A = self.compound["ANTOINE_A"]
            ant_B = self.compound["ANTOINE_B"]
            ant_C = self.compound["ANTOINE_C"]
            ant_Tmin = self.compound["Tmin_K"]
            ant_Tmax = self.compound["Tmax_K"]
            #
            Pvp_guess = [
                conv_unit(
                    antoineVP.antoineVP(T, ant_A, ant_B, ant_C, ant_Tmin, ant_Tmax)[0],
                    "bar",
                    "Pa",
                )
                for T in Tvec
            ]
        else:
            Pvp_guess = [1 for T in Tvec]

        Pvp = [self.return_Pvp_EOS(T, P)[0] for T, P in zip(Tvec, Pvp_guess)]

        V = [np.min(self.return_V_given_PT(P, T)) for P, T in zip(Pvp, Tvec)]

        fig, ax = plt.subplots()
        ax.plot(V, Pvp)
        plt.show()

        if var == "volume":
            x = np.linspace(a, b, points)
