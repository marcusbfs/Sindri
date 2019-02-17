import numpy as np
import sympy as sp
from scipy.integrate import quad

import units
# from scipy.optimize import root_scalar
# from scipy.misc import derivative
# import matplotlib.pyplot as plt
from constants import *
from db_utils import get_compound_properties

eos_options = {"van der Waals (1890)": "van_der_waals_1890",
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

    def __init__(self, name, formula, eos):
        self.eos = eos.lower()
        self.compound = get_compound_properties(name, formula)
        self.Tc = self.compound["Tc_K"]
        self.Pc = self.compound["Pc_bar"] * units.bar_to_Pa  # convert to pascal
        self.Zc = self.compound["Zc"]
        self.Vc = self.compound["Vc_cm3/mol"]
        self.omega = self.compound["omega"]

        self.V, self.T = sp.symbols('V T', real=True, positive=True)
        self.P = sp.symbols('P', real=True)
        self.Z, self.deltal, self.Bl, self.thetal, self.epsilonl = sp.symbols('Z deltal Bl thetal epsilonl', real=True)
        self.a, self.b, self.delta, self.theta, self.epsilon = sp.symbols('a b delta theta epsilon', real=True)
        self.alpha = sp.symbols('alpha', real=True)
        self.Tr, self.Pr = sp.symbols('Tr Pr', real=True)

        self.Z_V_T = None
        self.Z_P_T = None

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

            k0 = .465 + 1.347 * self.omega - .528 * self.omega ** 2
            k = k0 + (5 * self.Tr - 3 * k0 - 1) ** 2 / 70
            self.alpha = (1 + k * (1 - self.Tr ** .5)) ** 2

            self.delta = self.b * u
            self.epsilon = w * self.b ** 2
            self.theta = ac * self.alpha

        elif self.eos == "peneloux_et_al_1982":
            self.a = .42748 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = .08664 / self.Pc_RTc
            c = .40768 * (R_IG * self.Tc / self.Pc) * (0.00385 + 0.08775 * self.omega)
            self.delta = self.b + 2 * c
            self.epsilon = c * (self.b + c)
            self.alpha = (1. + (.48 + 1.574 * self.omega - .176 * self.omega ** 2) * (1. - self.Tr ** .5)) ** 2
            self.theta = self.a * self.alpha

        elif self.eos == "patel_and_teja_1982":
            F = 0.45241 + 1.30982 * self.omega - .295937 * self.omega ** 2
            zeta_c = 0.32903 - 0.076799 * self.omega + .0211947 * self.omega ** 2

            r = np.roots([1, 2 - 3 * zeta_c, 3 * zeta_c ** 2, -zeta_c ** 3])
            omega_b = np.min(r[r >= 0])
            omega_c = 1 - 3 * zeta_c
            omega_a = 3 * zeta_c ** 2 + 3 * (1 - 2 * zeta_c) * omega_b + omega_b ** 2 + 1 - 3 * zeta_c

            c = omega_c * R_IG * self.Tc / self.Pc
            self.b = omega_b * R_IG * self.Tc / self.Pc
            self.alpha = (1 + F * (1 - self.Tr ** .5)) ** 2
            self.a = omega_a * (R_IG * self.Tc) ** 2 / self.Pc

            self.delta = self.b + c
            self.epsilon = -self.b * c
            self.theta = self.a * self.alpha

        elif self.eos == "adachi_et_al_1983":
            b1 = R_IG * self.Tc * (.08974 - .03452 * self.omega + 0.00330 * self.omega ** 2) / self.Pc
            b2 = R_IG * self.Tc * (
                    .03686 + .00405 * self.omega - .01073 * self.omega ** 2 + .00157 * self.omega ** 3) / self.Pc
            b3 = R_IG * self.Tc * (
                    .154 + .14122 * self.omega - .00272 * self.omega ** 2 - .00484 * self.omega ** 3) / self.Pc

            self.a = (R_IG * self.Tc) ** 2 * (
                    .44869 + .04024 * self.omega + .01111 * self.omega ** 2 - .00576 * self.omega ** 3) / self.Pc
            self.b = b1
            self.delta = b3 - b2
            self.epsilon = -b2 * b3
            self.alpha = (1 + (.407 + 1.3787 * self.omega - .2933 * self.omega ** 2) * (1. - self.Tr ** .5)) ** 2
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
            self.a = .42188 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = .08333 / self.Pc_RTc
            self.delta = self.b
            self.epsilon = .001736 / self.Pc_RTc ** 2
            self.alpha = (1. + (.4998 + 1.5928 * self.omega - .19563 * self.omega ** 2 + .025 * self.omega ** 3) * (
                    1. - self.Tr ** .5)) ** 2
            self.theta = self.a * self.alpha

        elif self.eos == "adachi_et_al_1985":
            self.a = (R_IG * self.Tc) ** 2 * (
                    .43711 + .02366 * self.omega + .10538 * self.omega ** 2 + .10164 * self.omega ** 3) / self.Pc
            self.b = (R_IG * self.Tc) * (
                    .08779 - .02181 * self.omega - .06708 * self.omega ** 2 + .10617 * self.omega ** 3) / self.Pc
            c = (R_IG * self.Tc) * (
                    .0506 + .04184 * self.omega + .16413 * self.omega ** 2 - .03975 * self.omega ** 3) / self.Pc
            self.delta = 2 * c
            self.epsilon = - c ** 2
            self.alpha = (1 + (.4406 + 1.7039 * self.omega - 1.729 * self.omega ** 2 + .9929 * self.omega ** 3) * (
                    1 - self.Tr ** .5)) ** 2
            self.theta = self.a * self.alpha


        elif self.eos == "twu_et_al_1995":
            self.b = (R_IG * self.Tc) * .0777960739039 / self.Pc
            self.delta = 2 * self.b
            self.epsilon = - self.b ** 2
            self.a = (R_IG * self.Tc) ** 2 * 0.457235528921 / self.Pc
            alpha0 = self.Tr ** (-0.171813) * sp.exp(0.125283 * (1 - self.Tr ** 1.77634))
            alpha1 = self.Tr ** (-.607352) * sp.exp(0.511614 * (1 - self.Tr ** 2.20517))
            self.alpha = alpha0 + self.omega * (alpha1 - alpha0)
            self.theta = self.a * self.alpha

        elif self.eos == "gasem_et_al_pr_2001":
            self.a = .45724 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = .07780 / self.Pc_RTc
            self.delta = 2 * self.b
            self.epsilon = -self.b ** 2
            self.alpha = (1. + (0.386590 + 1.50226 * self.omega - .1687 * self.omega ** 2) * (
                    1. - self.Tr ** .5)) ** 2
            self.theta = self.a * self.alpha

        elif self.eos == "gasem_et_al_twu_2001":
            self.a = .45724 * (R_IG * self.Tc) ** 2 / self.Pc
            self.b = .07780 / self.Pc_RTc
            self.delta = 2 * self.b
            self.epsilon = -self.b ** 2
            alpha0 = self.Tr ** (-0.207176) * sp.exp(0.092099 * (1 - self.Tr ** (1.94800)))
            alpha1 = self.Tr ** (-0.502297) * sp.exp(0.603486 * (1 - self.Tr ** (2.09626)))
            self.alpha = alpha0 + self.omega * (alpha1 - alpha0)
            self.theta = self.a * self.alpha

        self.return_Z_V_T()
        self.return_Z_P_T()

    def return_Z_V_T(self):
        if self.Z_V_T is None:
            self.Z_V_T = self.V / (self.V - self.b) - ((self.theta / (R_IG * self.T) * self.V * (self.V - self.b))) / (
                    (self.V - self.b) * (self.V ** 2 + self.delta * self.V + self.epsilon))
        # print(self.Z_V_T)
        return self.Z_V_T

    def return_Z_P_T(self):
        if self.Z_P_T is None:
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

    def return_departureProperties(self, _P, _T, _V, _Z):
        # calculate UR
        f_to_integrate = self.T * sp.diff(self.Z_V_T, self.T) / self.V
        f_to_integrate = sp.lambdify(self.V, f_to_integrate.subs(self.T, _T))
        UR_RT = quad(f_to_integrate, _V, np.inf)[0]
        UR = UR_RT * _T * R_IG
        # calculate AR
        f_to_integrate = (1 - self.Z_V_T) / self.V
        f_to_integrate = sp.lambdify(self.V, f_to_integrate.subs(self.T, _T))
        AR_RT = quad(f_to_integrate, _V, np.inf)[0] + np.log(_Z)
        AR = AR_RT * _T * R_IG
        # calculate HR
        HR_RT = UR_RT + 1. - _Z
        HR = HR_RT * R_IG * _T
        # calculate SR
        SR_R = UR_RT - AR_RT
        SR = SR_R * R_IG
        # calculate GR
        GR_RT = AR_RT + 1 - _Z
        GR = GR_RT * R_IG * _T

        fugacity = _P * np.e ** (-GR_RT)

        # print("HR: ", HR)
        # print("GR: ", GR)
        # print("SR: ", SR)
        # print("AR: ", AR)
        # print("UR: ", UR)
        # print("fugacity: ", fugacity)

        dict_ans = {
            "HR": HR,
            "SR": SR,
            "GR": GR,
            "UR": UR,
            "AR": AR,
            "f": fugacity
        }
        return dict_ans

    def return_delta_ResProperties(self, _Pref, _Tref, _Vref, _Zref,
                                   _P, _T, _V, _Z):
        ref = self.return_departureProperties(_Pref, _Tref, _Vref, _Zref)
        proc = self.return_departureProperties(_P, _T, _V, _Z)
        delta = np.array(list(proc.values())) - np.array(list(ref.values()))
        dict_delta = dict(zip(ref.keys(), delta))
        dict_delta["f"] = proc["f"]
        return dict_delta

    def return_Pvp_EOS(self, _T, initialP, tol=1e-3, k=500):
        error = 0.01
        _P = initialP

        f_to_integrate = (1 - self.Z_V_T) / self.V
        f_to_integrate = sp.lambdify(self.V, f_to_integrate.subs(self.T, _T))

        def helper_f(hv, hz):
            return hz - 1. - np.log(hz) - quad(f_to_integrate, hv, np.inf)[0]

        for i in range(1, k + 1):
            Zs = self.return_Z_given_PT(_P, _T)
            Zl = np.min(Zs)
            Zv = np.max(Zs)
            Vl = Zl * R_IG * _T / _P
            Vv = Zv * R_IG * _T / _P

            fL = _P * np.e ** helper_f(Vl, Zl)
            fV = _P * np.e ** helper_f(Vv, Zv)
            _P = _P * fL / fV
            error = fL / fV - 1.0
            if abs(error) < tol:
                return _P, i

        return _P, str(i) + " (max iterations)"


if __name__ == "__main__":
    cname = "methane"
    cformula = "CH4"

    # eos = "van_der_waals_1890"
    # eos = "redlich_and_kwong_1949"
    # eos = "wilson_1964"
    # eos = "soave_1972"
    eos = "peng_and_robinson_1976"
    # eos = "soave_1984"

    T = 150  # k
    P = 1 * units.bar_to_Pa  # bar

    Tref = 300  # k
    Pref = 1 * units.bar_to_Pa  # bar

    c = EOS(cname, cformula, eos)

    Zs = c.return_Z_given_PT(P, T)
    print(Zs)
    Vs = c.return_V_given_PT(P, T)
    print(Vs)

    Zvap = np.max(Zs)
    Vvap = np.max(Vs)

    # c.return_departureProperties(P, T, Vvap, Zvap)
    c.return_departureProperties()
