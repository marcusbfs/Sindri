import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.misc import derivative
import matplotlib.pyplot as plt
from constants import R_IG
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

        self.Z, self.deltal, self.Bl, self.thetal, self.epsilonl = sp.symbols('Z deltal Bl thetal epsilonl', real=True)
        self.b, self.P, self.R_IG, self.T, self.delta, self.theta, self.epsilon = sp.symbols(
            'b P R_IG T delta theta epsilon', real=True)
        self.V = sp.symbols('V', real=True)

        self.eos_eq = self.Z ** 3 + (self.deltal - self.Bl - 1) * self.Z ** 2 + self.Z * (
                self.thetal + self.epsilonl - self.deltal * (self.Bl + 1)) - (
                              self.epsilonl * (self.Bl + 1) + self.Bl * self.thetal)
        self.eos_eq = self.eos_eq.subs(self.Bl, self.b * self.P / (R_IG * self.T))
        self.eos_eq = self.eos_eq.subs(self.deltal, self.delta * self.P / (R_IG * self.T))
        self.eos_eq = self.eos_eq.subs(self.thetal, self.theta * self.P / (R_IG * self.T) ** 2)
        self.eos_eq = self.eos_eq.subs(self.epsilonl, self.epsilon * (self.P / (R_IG * self.T)) ** 2)

        self.Tcval = self.compound["Tc_K"]
        self.Pcval = self.compound["Pc_bar"] * units.bar_to_Pa  # convert to pascal
        self.omegaval = self.compound["omega"]
        self.Tval = T
        self.Pval = P

        self.initialize()

        self.ZVT = self.V /

        print(self.eos_eq)

        return 0

        # self.eos_eq = self.eos_eq.subs(self.theta, self.thetaval)
        # self.eos_eq = self.eos_eq.subs(self.b, self.bval)
        # self.eos_eq = self.eos_eq.subs(self.epsilon, self.epsilonval)
        # self.eos_eq = self.eos_eq.subs(self.delta, self.deltaval)
        # self.eos_eq = sp.simplify(self.eos_eq)

    def return_Z(self, _T, _P):
        ans = sp.solve(self.eos_eq.subs([(self.T, _T), (self.P, _P)]))
        ans = np.array(ans)
        return ans

    def return_GR(self):
        Z_func_of_P = sp.solve(self.eos_eq.subs(self.T, self.Tval), self.Z)
        for i in Z_func_of_P:
            try:
                e = (i - 1) / self.P
                f = sp.lambdify([self.P], e)

                def ff(p):
                    if p == 0: return 0
                    return f(p)

                print(ff(self.Pval))
                ans = quad(ff, 0, self.Pval)
                print(ans)
            except:
                print("i cry")

    def show_eos_options(self):
        r = list(self.eos_options.keys())
        print(r)
        return r

    def initialize(self):
        # try:
        self.Trval = self.Tval / self.Tcval
        self.Pc_RTc = self.Pcval / (R_IG * self.Tcval)

        if self.eos == "van_der_waals_1890":
            self.aval = .42188 * (R_IG * self.Tcval) ** 2 / self.Pcval
            self.bval = .125 / self.Pc_RTc
            self.deltaval = 0.
            self.epsilonval = 0.
            self.alphaval = 1.
            self.thetaval = self.aval

        elif self.eos == "redlich_and_kwong_1949":
            self.aval = .42748 * (R_IG * self.Tcval) ** 2 / self.Pcval
            self.bval = .08664 / self.Pc_RTc
            self.deltaval = 0.08664 / self.Pc_RTc
            self.epsilonval = 0.
            self.alphaval = 1. / self.Trval ** 0.5
            self.thetaval = self.aval / self.Trval ** .5

        elif self.eos == "wilson_1964":
            self.aval = .42748 * (R_IG * self.Tcval) ** 2 / self.Pcval
            self.bval = .08664 / self.Pc_RTc
            self.deltaval = self.bval
            self.epsilonval = 0.
            self.alphaval = self.Trval * (1 + (1.57 + 1.62 * self.omegaval) * (1. / self.Trval - 1.))
            self.thetaval = self.aval * self.alphaval

        elif self.eos == "soave_1972":
            self.aval = .42748 * (R_IG * self.Tcval) ** 2 / self.Pcval
            self.bval = .08664 / self.Pc_RTc
            self.deltaval = self.bval
            self.epsilonval = 0.
            self.alphaval = (1. + (.48 + 1.574 * self.omegaval - .176 * self.omegaval ** 2) * (
                    1. - self.Trval ** .5)) ** 2
            self.thetaval = self.aval * self.alphaval

        elif self.eos == "peng_and_robinson_1976":
            self.aval = .45724 * (R_IG * self.Tcval) ** 2 / self.Pcval
            self.bval = .07780 / self.Pc_RTc
            self.deltaval = .15559 / self.Pc_RTc
            self.epsilonval = -.006053 / self.Pc_RTc ** 2
            self.alphaval = (1. + (.37464 + 1.54226 * self.omegaval - .2699 * self.omegaval ** 2) * (
                    1. - self.Trval ** .5)) ** 2
            self.thetaval = self.aval * self.alphaval

        elif self.eos == "soave_1984":
            self.aval = .42188 * (R_IG * self.Tcval) ** 2 / self.Pcval
            self.bval = .08333 / self.Pc_RTc
            self.deltaval = self.bval
            self.epsilonval = .001736 / self.Pc_RTc ** 2
            self.alphaval = (1. + (
                    .4998 + 1.5928 * self.omegaval - .19563 * self.omegaval ** 2 + .025 * self.omegaval ** 3) * (
                                     1. - self.Trval ** .5)) ** 2
            self.thetaval = self.aval * self.alphaval

        self.etaval = self.bval
        # except:
        #     raise TypeError("One or more variables needed are not set")


if __name__ == "__main__":
    cname = "propane"
    cformula = "C3H8"

    eos = "van_der_waals_1890"
    eos = "redlich_and_kwong_1949"
    # eos = "wilson_1964"
    # eos = "soave_1972"
    eos = "peng_and_robinson_1976"
    # eos = "soave_1984"

    T = 359.8
    P = 1.0e5

    c = EOS(cname, cformula, eos, T, P)
    # a = c.return_Z(T, P)
    a = c.return_GR()
