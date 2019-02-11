import numpy as np
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
        self.T = T
        self.P = P

        self.initialize()
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

        self.eta = self.b
        # except:
        #     raise TypeError("One or more variables needed are not set")

    def return_P(self, V):
        # return - P + R_IG * T / (V - b) - theta * (V - eta) / ((V - b) * (V ** 2 + delta * V + epsilon))
        return R_IG * self.T / (V - self.b) - self.theta * (V - self.eta) / (
                (V - self.b) * (V ** 2 + self.delta * V + self.epsilon))

    def def_T(self, T):
        self.T = T
        self.initialize()

    def def_EOS(self, name):
        self.eos = name

    def return_Z(self):
        P_RT = self.P / (R_IG * self.T)
        Bl = self.b * P_RT
        deltal = self.delta * P_RT
        thetal = self.theta * self.P / (R_IG * self.T) ** 2
        epsilonl = self.epsilon * P_RT ** 2
        etal = Bl

        coefs = [1., deltal - Bl - 1., thetal + epsilonl - deltal * (Bl + 1.), -(epsilonl * (Bl + 1.) + thetal * etal)]
        r = np.roots(coefs)
        real_valued = r.real[abs(r.imag) < 1e-7]
        ans = real_valued[real_valued > 0]
        if ans.size == 0:
            raise Exception("There are no positive real roots for Z")
        return ans

    def return_V(self):
        ans = self.return_Z() * R_IG * self.T / self.P
        return ans

    def diagram_PV(self, vi, vf, n_of_points):
        self.multiple_diagram_PV(self, vi, vf, n_of_points, self.T)
        # v = np.linspace(vi, vf, n_of_points, endpoint=True)
        # p = self.return_P(v)
        #
        # fig, ax = plt.subplots()
        # ax.plot(v, p)
        # ax.set(xlabel="molar volume (m3/mol)", ylabel="pressure (Pa)")
        # ax.grid()
        # plt.show()

    def multiple_diagram_PV(self, vi, vf, n_of_points, temps):
        temps = np.atleast_1d(temps)
        v = np.linspace(vi, vf, n_of_points, endpoint=True)
        fig, ax = plt.subplots()

        for i in range(len(temps)):
            self.def_T(temps[i])
            p = self.return_P(v)
            ax.plot(v, p, label="T = " + str(round(temps[i], 2)) + " K")

        title = "PV diagram - " + self.compound["Name"].title() + " - " + self.eos_options[self.eos]
        ax.set(xlabel="molar volume (m3/mol)", ylabel="pressure (Pa)", title=title)
        ax.grid()
        ax.legend()
        plt.show()


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
    c.show_eos_options()
    r = c.return_V()
    print(r)

    rr = c.return_P(r)
    print(rr)

    vi = 1.1e-4
    vf = 7.08e-4
    n = 10000

    T = [359.8, 369.8, 379.8]
    T = np.linspace(350, 390, 4)

    c.multiple_diagram_PV(vi, vf, n, T)
