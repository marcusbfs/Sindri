import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.misc import derivative
import matplotlib.pyplot as plt
from constants import *
from db_utils import get_compound_properties
import units

eos_options = {"van der Waals (1890)": "van_der_waals_1890",
               "Redlich and Kwong (1949)": "redlich_and_kwong_1949",
               "Wilson (1964)": "wilson_1964",
               "Soave (1972)": "soave_1972",
               "Peng and Robinson (1976)": "peng_and_robinson_1976",
               "Soave (1984)": "soave_1984"
               }


class EOS:

    def __init__(self, name, formula, eos, T, P):
        self.eos = eos.lower()
        self.compound = get_compound_properties(name, formula)
        self.Tc = self.compound["Tc_K"]
        self.Pc = self.compound["Pc_bar"] * units.bar_to_Pa  # convert to pascal
        self.omega = self.compound["omega"]
        self.Tval = T
        self.Pval = P

        self.Z, self.deltal, self.Bl, self.thetal, self.epsilonl = sp.symbols('Z deltal Bl thetal epsilonl', real=True)
        self.a, self.b, self.P, self.T, self.delta, self.theta, self.epsilon = sp.symbols('a b P T delta theta epsilon',
                                                                                          real=True)
        self.alpha = sp.symbols('alpha', real=True)
        self.Tr, self.Pr = sp.symbols('Tr Pr', real=True)

        self.V = sp.symbols('V', real=True)

        self.Z_V_T = None
        self.Z_P_T = None
        self.Vval = None

        self.initialize()

        self.return_Z_V_T()
        self.return_Z_P_T()

        self.eos_options = eos_options

    def show_eos_options(self):
        r = list(self.eos_options.keys())
        print(r)
        return r

    def initialize(self):
        # try:
        self.Tr = self.T / self.Tc
        self.Pc_RTc = self.Pc / (R_IG * self.Tc)

        if self.eos == "van_der_waals_1890":
            self.a = .42188 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = .125 / self.Pc_RTc
            self.delta = 0.
            self.epsilon = 0.
            self.alpha = 1.
            self.theta = self.a

        elif self.eos == "redlich_and_kwong_1949":
            self.a = .42748 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = .08664 / self.Pc_RTc
            self.delta = 0.08664 / self.Pc_RTc
            self.epsilon = 0.
            self.alpha = 1. / self.Tr ** 0.5
            self.theta = self.a / self.Tr ** .5

        elif self.eos == "wilson_1964":
            self.a = .42748 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = .08664 / self.Pc_RTc
            self.delta = self.b
            self.epsilon = 0.
            self.alpha = self.Tr * (1 + (1.57 + 1.62 * self.omega) * (1. / self.Tr - 1.))
            self.theta = self.a * self.alpha

        elif self.eos == "soave_1972":
            self.a = .42748 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = .08664 / self.Pc_RTc
            self.delta = self.b
            self.epsilon = 0.
            self.alpha = (1. + (.48 + 1.574 * self.omega - .176 * self.omega ** 2) * (1. - self.Tr ** .5)) ** 2
            self.theta = self.a * self.alpha

        elif self.eos == "peng_and_robinson_1976":
            self.a = .45724 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = .07780 / self.Pc_RTc
            self.delta = .15559 / self.Pc_RTc
            self.epsilon = -.006053 / self.Pc_RTc ** 2
            self.alpha = (1. + (.37464 + 1.54226 * self.omega - .2699 * self.omega ** 2) * (
                    1. - self.Tr ** .5)) ** 2
            self.theta = self.a * self.alpha

        elif self.eos == "soave_1984":
            self.a = .42188 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = .08333 / self.Pc_RTc
            self.delta = self.b
            self.epsilon = .001736 / self.Pc_RTc ** 2
            self.alpha = (1. + (.4998 + 1.5928 * self.omega - .19563 * self.omega ** 2 + .025 * self.omega ** 3) * (
                    1. - self.Tr ** .5)) ** 2
            self.theta = self.a * self.alpha

    def return_Z_V_T(self):
        if not self.Z_V_T:
            self.Z_V_T = self.V / (self.V - self.b) - ((self.theta / (R_IG * self.T) * self.V * (self.V - self.b))) / (
                    (self.V - self.b) * (self.V ** 2 + self.delta * self.V + self.epsilon))
        # print(self.Z_V_T)
        return self.Z_V_T

    def return_Z_P_T(self):
        if not self.Z_P_T:
            self.eos_eq = self.Z ** 3 + (self.deltal - self.Bl - 1) * self.Z ** 2 + self.Z * (
                    self.thetal + self.epsilonl - self.deltal * (self.Bl + 1)) - (
                                  self.epsilonl * (self.Bl + 1) + self.Bl * self.thetal)
            self.eos_eq = self.eos_eq.subs(self.Bl, self.b * self.P / (R_IG * self.T))
            self.eos_eq = self.eos_eq.subs(self.deltal, self.delta * self.P / (R_IG * self.T))
            self.eos_eq = self.eos_eq.subs(self.thetal, self.theta * self.P / (R_IG * self.T) ** 2)
            self.Z_P_T = self.eos_eq.subs(self.epsilonl, self.epsilon * (self.P / (R_IG * self.T)) ** 2)
        # print(self.Z_P_T)
        return self.Z_P_T

    def return_Z_given_PT(self, _P, _T):
        # self.return_Z_P_T()
        f = sp.lambdify([self.P, self.T], self.return_Z_P_T())
        # print(f(_P, _T))
        p = sp.Poly(f(_P, _T), self.Z).coeffs()
        # print(p.coeffs())

        r = np.roots(p)
        real_valued = r.real[abs(r.imag) < 1e-5]
        ans = real_valued[real_valued >= 0]
        if ans.size == 0:
            raise Exception("There are no positive real roots for Z")
        # print(ans)
        self.Zval = ans
        return ans

    def return_V_given_PT(self, _P, _T):
        ans = self.return_Z_given_PT(_P, _T) * R_IG * _T / _P
        # print(ans)
        self.Vval = ans
        return ans

    def return_Z(self):
        return self.return_Z_given_PT(self.Pval, self.Tval)

    def return_V(self):
        return self.return_V_given_PT(self.Pval, self.Tval)

    def return_HR_given_VT(self, _P, _T, state):
        _V = self.return_V_given_PT(_P, _T)
        if state == "liq":
            _V = np.min(_V)
        elif state == "vap":
            _V = np.max(_V)
        _Z = self.Z_V_T.subs([(self.V, _V), (self.T, _T)]).evalf()
        _Z = float(_Z)
        # print(_V)
        # print(_T)
        # print(_Z)
        f_to_integrate = self.T * sp.diff(self.Z_V_T, self.T) / self.V
        f_to_integrate = sp.lambdify(self.V, f_to_integrate.subs(self.T, _T))
        ans = quad(f_to_integrate, _V, np.inf)[0] + 1 - _Z
        # print(ans)
        return ans * R_IG * _T

    def return_SR_given_VT(self, _P, _T, state):
        _V = self.return_V_given_PT(_P, _T)
        if state == "liq":
            _V = np.min(_V)
        elif state == "vap":
            _V = np.max(_V)
        _Z = self.Z_V_T.subs([(self.V, _V), (self.T, _T)])
        _Z = float(_Z)
        f_to_integrate = (self.T * sp.diff(self.Z_V_T, self.T) - 1 + self.Z_V_T) / self.V
        f_to_integrate = sp.lambdify(self.V, f_to_integrate.subs(self.T, _T))
        ans = quad(f_to_integrate, _V, np.inf)[0] + np.log(float(_Z)) + - np.log(float(_Z))
        # print(ans)
        return ans * R_IG

    def return_f_given_VT(self, _P, _T, state):
        _V = self.return_V_given_PT(_P, _T)
        if state == "liq":
            _V = np.min(_V)
        elif state == "vap":
            _V = np.max(_V)
        _Z = self.Z_V_T.subs([(self.V, _V), (self.T, _T)]).evalf()
        _Z = float(_Z)
        f_to_integrate = (1 - self.Z_V_T) / self.V
        f_to_integrate = sp.lambdify(self.V, f_to_integrate.subs(self.T, _T))
        ans = quad(f_to_integrate, _V, np.inf)[0] + np.log(_Z) + 1 - _Z
        return _P * np.e ** ans

    # def return

    # def return_UR(self):
    #     ans = self.return_UR_given_VT(self.Vval, self.Tval)
    #     # print(ans)
    #     return ans
    #
    # def return_AR(self):
    #     ans = self.return_AR_given_VT(self.Vval, self.Tval)
    #     # print(ans)
    #     return ans


if __name__ == "__main__":
    # cname = "propane"
    # cformula = "C3H8"
    cname = "water"
    cformula = "H2O"

    eos = "van_der_waals_1890"
    eos = "redlich_and_kwong_1949"
    # eos = "wilson_1964"
    # eos = "soave_1972"
    eos = "peng_and_robinson_1976"
    # eos = "soave_1984"

    T = 359.8
    P = 1.0e5

    c = EOS(cname, cformula, eos, T, P)
    c.return_Z_given_PT(P, T)
    c.return_V_given_PT(P, T)
    # c.return_UR()
    # c.return_AR()
    a = c.return_HR_given_VT(2.034e-5, 222)
    print(a)
