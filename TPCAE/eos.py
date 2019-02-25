import numpy as np
import sympy as sp

from constants import R_IG
from db_utils import get_compound_properties
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

        self.Tr = self.T / self.Tc
        self.Pc_RTc = self.Pc / (R_IG * self.Tc)

        self.initialize()

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
