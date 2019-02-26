import numpy as np
import sympy as sp
from numba import njit, cfunc, types
from scipy import LowLevelCallable
from scipy.integrate import quad

import IdealGasPropertiesPureSubstance as IGPROP
from constants import R_IG
from polyEqSolver import solve_cubic
from units import conv_unit

eos_options = {
    "van der Waals (1890)": "van_der_waals_1890",
    "Redlich and Kwong (1949)": "redlich_and_kwong_1949",
    "Wilson (1964)": "wilson_1964",
    "Soave (1972)": "soave_1972",
    "Peng and Robinson (1976)": "peng_and_robinson_1976",
    "Schmidt and Wenzel (1979)": "schmidt_and_wenzel_1979",
    "Péneloux, et al. (1982)": "peneloux_et_al_1982",
    "Patel and Teja (1982)": "patel_and_teja_1982",
    "Adachi, et al. (1983)": "adachi_et_al_1983",
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

    def __init__(self, compounds, y, k, eos):
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
        self.compounds = compounds
        self.n = len(self.compounds)  # number of compounds

        self.Zcs = []
        self.Vcs = []
        self.Pcs = []
        self.Tcs = []
        self.omegas = []
        for cmpnd in self.compounds:
            self.Zcs.append(cmpnd["Zc"])
            self.Vcs.append(cmpnd["Vc_cm3/mol"])
            self.Tcs.append(cmpnd["Tc_K"])
            self.Pcs.append(conv_unit(cmpnd["Pc_bar"], "bar", "Pa"))
            self.omegas.append(cmpnd["omega"])

        self.compound = compounds[0]
        self.y = y
        self.k = k
        self.eos = eos.lower()
        # compound : dictionary containing the values extracted from the database.
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

        self.Tr = self.T / self.Tc
        self.Pc_RTc = self.Pc / (R_IG * self.Tc)

        self.initialize()
        self.initialize_functions()

        self.eos_options = eos_options

    def show_eos_options(self):
        r = list(self.eos_options.keys())
        return r

    def initialize(self):
        """ Get the correct parameters for the cubic equation of state selected.

        The parameters are  'b', 'theta', 'delta' and 'epsilon'. The equation has the form:
            P = R * T / (V - b) - theta / (V**2 + delta * V + epsilon)
        where:
            theta = a * alpha
        This equation was taken from Poling, 2002.

        """

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

            self.bs = []
            self.ass = []
            self.alphas = []
            self.thetas = []
            self.b = 0
            for i in range(self.n):
                self.bs.append(0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i])))
                self.b += self.y[i] * self.bs[i]
                self.ass.append(0.45724 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i])
                self.alphas.append(
                    (
                        1.0
                        + (
                            0.37464
                            + 1.54226 * self.omegas[i]
                            - 0.2699 * self.omegas[i] ** 2
                        )
                        * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                    )
                    ** 2
                )
                self.thetas.append(self.ass[i] * self.alphas[i])

            self.theta = 0
            for i in range(self.n):
                inner_sum = 0
                for j in range(self.n):
                    # inner_sum += self.y[i]*self.y[j] * (self.thetas[i]*self.thetas[j])**.5*(1-self.k[i][j])
                    inner_sum += (
                        self.y[i]
                        * self.y[j]
                        * sp.sqrt(self.thetas[i] * self.thetas[j])
                        * (1 - self.k[i][j])
                    )
                self.theta += inner_sum

            self.delta = 2 * self.b
            self.epsilon = -self.b * self.b

            # ============================
            # self.a = 0.45724 * (R_IG * self.Tc) ** 2 / self.Pc
            # self.b = 0.07780 / self.Pc_RTc
            # self.delta = 2 * self.b
            # self.epsilon = -self.b * self.b
            # self.alpha = (
            #     1.0
            #     + (0.37464 + 1.54226 * self.omega - 0.2699 * self.omega ** 2)
            #     * (1.0 - self.Tr ** 0.5)
            # ) ** 2
            # self.theta = self.a * self.alpha

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
            alpha0 = self.Tr ** (-0.171813) * 2.718281828459045235360 ** (
                0.125283 * (1 - self.Tr ** 1.77634)
            )
            alpha1 = self.Tr ** (-0.607352) * 2.718281828459045235360 ** (
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
            alpha0 = self.Tr ** (-0.207176) * 2.718281828459045235360 ** (
                0.092099 * (1 - self.Tr ** 1.94800)
            )
            alpha1 = self.Tr ** (-0.502297) * 2.718281828459045235360 ** (
                0.603486 * (1 - self.Tr ** 2.09626)
            )
            self.alpha = alpha0 + self.omega * (alpha1 - alpha0)
            self.theta = self.a * self.alpha

    # TODO put this function in EOS class? maybe it'll be better for mixture calculations
    def initialize_functions(self):

        self.b = np.real(self.b)
        self.delta = np.real(self.delta)
        self.epsilon = np.real(self.epsilon)

        self.Z_V_T = None
        self.dZ_VT_dT = None
        self.numfunc_P_given_VT = None

        self.return_Z_V_T()
        self.return_diff_Z_V_T_dT()

        # create numerical functions
        self.numf_Z_VT = njit()(
            sp.lambdify([self.V, self.T], self.Z_V_T, modules="numpy")
        )
        self.numf_dZdT_VT = njit()(
            sp.lambdify([self.V, self.T], sp.diff(self.Z_V_T, self.T), modules="numpy")
        )
        self.numf_theta_T = njit()(sp.lambdify([self.T], self.theta, modules="numpy"))
        self.numf_P_VT = njit()(
            sp.lambdify(
                [self.V, self.T], self.Z_V_T * self.T * R_IG / self.V, modules="numpy"
            )
        )

        # this ain't pretty but hey, it works fast!
        self.tmp_cfunc = None
        c_sig = types.double(types.intc, types.CPointer(types.double))
        exec(
            "self.tmp_cfunc = lambda n, data: {:s}".format(
                str((1 - self.Z_V_T) / self.V)
                .replace("V", "data[0]")
                .replace("T", "data[1]")
                .replace("Abs", "np.abs")
                .replace("sign", "np.sign")
            )
        )
        qf = cfunc(c_sig)(self.tmp_cfunc)
        self.qnf = LowLevelCallable(qf.ctypes)

        # TODO send this to pure substance?
        self.helper_Pvp_f = (
            lambda hv, hz, _T: hz
            - 1.0
            - np.log(hz)
            - quad(self.qnf, hv, np.inf, args=(_T,))[0]
        )

        exec(
            "self.tmp_cfunc2 = lambda n, data: {:s}".format(
                str(self.T * sp.diff(self.Z_V_T, self.T) / self.V)
                .replace("V", "data[0]")
                .replace("T", "data[1]")
                .replace("Abs", "np.abs")
                .replace("sign", "np.sign")
            )
        )
        tf = cfunc(c_sig)(self.tmp_cfunc2)
        self.numf_UR = LowLevelCallable(tf.ctypes)

    def return_Z_V_T(self):
        """
        Creates the symbolic equation:
            Z = V / (V - b) - ((theta / (R_IG * T)) * V) / (V**2 + delta * V + epsilon)

        Returns
        -------
        self.Z_V_T : sympy symbolic expression.

        """
        if self.Z_V_T is None:
            self.Z_V_T = self.V / (self.V - self.b) - (
                self.theta / (R_IG * self.T)
            ) * self.V / (self.V ** 2 + self.delta * self.V + self.epsilon)

    def return_Z_given_PT(self, _P, _T):
        """ Return the positive roots (Z) of the cubic equation.

        parameters
        ----------
        _P : float
            pressure, pa.
        _T : float
            temperature, k.

        Returns
        -------
        ans : array, float
            Returns an array of the real roots of the cubic equation of state. The minimum value of this array
            corresponds to the vapor state, while the maximum value corresponds to the liquid state.

        """

        Bl = self.b * _P / (R_IG * _T)
        deltal = self.delta * _P / (R_IG * _T)
        thetal = self.numf_theta_T(_T) * _P / (R_IG * _T) ** 2
        epsilonl = self.epsilon * (_P / (R_IG * _T)) ** 2
        a = 1.0
        b = deltal - Bl - 1.0
        c = thetal + epsilonl - deltal * (Bl + 1.0)
        d = -(epsilonl * (Bl + 1.0) + Bl * thetal)

        coefs = (a, b, c, d)

        ans = np.asarray(solve_cubic(*coefs))
        return ans[ans > 0]

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

    def return_P_given_VT(self, _V, _T):
        """ Return the values of '_P' given '_V' and '_T' using the cubic equation of state.

        Parameters
        ----------
        _V : float
            molar volume, m3/mol.
        _T : float
            temperature, Kelvin.

        Returns
        -------
        _P : float
            pressure at '_T' and '_V', Pascal.

        """
        _P = self.numf_P_VT(_V, _T)
        return _P

    def return_diff_Z_V_T_dT(self):
        if self.dZ_VT_dT is None:
            self.return_Z_V_T()
            self.dZ_VT_dT = sp.diff(self.Z_V_T, self.T)

    def return_fugacity(self, _P, _T, _V, _Z):
        f = _P * np.e ** self.helper_Pvp_f(_V, _Z, _T)
        return f

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
        UR_RT = quad(self.numf_UR, _V, np.inf, args=(_T,))[0]
        UR = UR_RT * _T * R_IG
        # calculate AR
        AR_RT = quad(self.qnf, _V, np.inf, args=(_T,))[0] + np.log(_Z)
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

        # fugacity = _P * np.exp(-GR_RT)

        dict_ans = {"HR": HR, "SR": SR, "GR": GR, "UR": UR, "AR": AR}
        return dict_ans

    def return_delta_ResProperties(self, _Pref, _Tref, _Vref, _Zref, _P, _T, _V, _Z):
        ref = self.return_departureProperties(_Pref, _Tref, _Vref, _Zref)
        proc = self.return_departureProperties(_P, _T, _V, _Z)
        delta = np.array(list(proc.values())) - np.array(list(ref.values()))
        dict_delta = dict(zip(ref.keys(), delta))
        # dict_delta["f"] = proc["f"]
        return dict_delta

    def return_delta_prop(self, _P, _T, _Pref, _Tref):

        log = ""

        try:  # Calculate Z
            Zs = self.return_Z_given_PT(_P, _T)
            Zliq = np.min(Zs)
            Zvap = np.max(Zs)

            Zsref = self.return_Z_given_PT(_Pref, _Tref)
            Zliqref = np.min(Zsref)
            Zvapref = np.max(Zsref)

        except Exception as e:
            print(str(e))
            raise ValueError("Error calculating Z\n" + str(e))

        state = IGPROP.return_fluidState(
            _P,
            conv_unit(self.compound["Pc_bar"], "bar", "Pa"),
            _T,
            self.compound["Tc_K"],
            1e5,
            delta=1e-4,
        )

        supercritical = True if state == "supercritical fluid" else False

        Vliq = Zliq * R_IG * _T / _P
        Vvap = Zvap * R_IG * _T / _P
        Vliqref = Zliqref * R_IG * _Tref / _Pref
        Vvapref = Zvapref * R_IG * _Tref / _Pref
        rholiq = self.compound["Mol. Wt."] * 1e-3 / Vliq
        rhovap = self.compound["Mol. Wt."] * 1e-3 / Vvap

        if (
            self.compound["a0"] is not None
            and self.compound["a1"] is not None
            and self.compound["a2"] is not None
            and self.compound["a3"] is not None
            and self.compound["a4"] is not None
        ):
            has_cp = True
        else:
            has_cp = False

        try:
            dProp_liq = self.return_delta_ResProperties(
                _Pref, _Tref, Vliqref, Zliqref, _P, _T, Vliq, Zliq
            )
            dProp_vap = self.return_delta_ResProperties(
                _Pref, _Tref, Vvapref, Zvapref, _P, _T, Vvap, Zvap
            )
        except:
            raise ValueError("Error evaluating departure functions")

        if has_cp:
            a0 = self.compound["a0"]
            a1 = self.compound["a1"]
            a2 = self.compound["a2"]
            a3 = self.compound["a3"]
            a4 = self.compound["a4"]
            Tmin = self.compound["Tcpmin_K"]
            Tmax = self.compound["Tcpmax_K"]

            try:
                IGprop = IGPROP.return_IdealGasProperties(
                    _Tref, _T, _Pref, _P, a0, a1, a2, a3, a4, Tmin, Tmax
                )
            except Exception as e:
                print(str(e))
                raise ValueError("Error calculating ideal properties\n" + str(e))

            ideal_ret = [
                IGprop["Cp_IG"],
                IGprop["dH_IG"],
                IGprop["dS_IG"],
                IGprop["dG_IG"],
                IGprop["dU_IG"],
                IGprop["dA_IG"],
            ]

            if IGprop["msg"] is not None:
                log += "WARNING Cp temperature range: {0:s}\n".format(IGprop["msg"])

            dH_liq = IGprop["dH_IG"] - dProp_liq["HR"]
            dS_liq = IGprop["dS_IG"] - dProp_liq["SR"]
            dG_liq = IGprop["dG_IG"] - dProp_liq["GR"]
            dU_liq = IGprop["dU_IG"] - dProp_liq["UR"]
            dA_liq = IGprop["dA_IG"] - dProp_liq["AR"]

            dH_vap = IGprop["dH_IG"] - dProp_vap["HR"]
            dS_vap = IGprop["dS_IG"] - dProp_vap["SR"]
            dG_vap = IGprop["dG_IG"] - dProp_vap["GR"]
            dU_vap = IGprop["dU_IG"] - dProp_vap["UR"]
            dA_vap = IGprop["dA_IG"] - dProp_vap["AR"]
        else:
            ideal_dict = None
            dH_liq = None
            dS_liq = None
            dG_liq = None
            dU_liq = None
            dA_liq = None

            dH_vap = None
            dS_vap = None
            dG_vap = None
            dU_vap = None
            dA_vap = None

        liq_ret = [Zliq, Vliq, rholiq, dH_liq, dS_liq, dG_liq, dU_liq, dA_liq, _P, _T]

        vap_ret = [Zvap, Vvap, rhovap, dH_vap, dS_vap, dG_vap, dU_vap, dA_vap, _P, _T]

        return ideal_ret, liq_ret, vap_ret, log, supercritical

    def show_eos_options(self):
        r = list(self.eos_options.keys())
        return r

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
        self.initialize()
        self.initialize_functions()
