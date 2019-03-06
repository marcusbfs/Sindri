import sympy as sp
import numpy as np

from CubicEOS import CubicEOS
from constants import R_IG
from compounds import MixtureProp
from Properties import DeltaProp, VaporPressure, Props
from polyEqSolver import solve_cubic

eos_options = {
    "van der Waals (1890)": "van_der_waals_1890",
    "Redlich and Kwong (1949)": "redlich_and_kwong_1949",
    "Wilson (1964)": "wilson_1964",
    "Soave (1972)": "soave_1972",
    "Peng and Robinson (1976)": "peng_and_robinson_1976",
    # "Schmidt and Wenzel (1979)": "schmidt_and_wenzel_1979", # conferir regra de mistura para esse
    "Péneloux, et al. (1982)": "peneloux_et_al_1982",
    "Patel and Teja (1982)": "patel_and_teja_1982",
    "Adachi, et al. (1983)": "adachi_et_al_1983",
    "Soave (1984)": "soave_1984",
    "Adachi, et al. (1985)": "adachi_et_al_1985",
    "Twu, et al. (1995)": "twu_et_al_1995",
    "Ahlers-Gmehling (2001)": "ahlers_gmehling_2001",
    "Gasem, et al. PR modification (2001)": "gasem_et_al_pr_2001",
    "Gasem, et al. Twu modificaton (2001)": "gasem_et_al_twu_2001",
}


class EOS(CubicEOS):
    def __init__(self, mix: MixtureProp, k, eos):
        super().__init__()

        self.mix = mix
        self.y = np.atleast_1d(self.mix.y)
        self.k = k
        self.n = self.mix.n

        self.eosDisplayName = eos
        self.eosValue = eos_options[self.eosDisplayName]

        self.Zcs = np.zeros(self.n)
        self.Vcs = np.zeros(self.n)
        self.Pcs = np.zeros(self.n)
        self.Tcs = np.zeros(self.n)
        self.omegas = np.zeros(self.n)

        for i in range(self.n):
            self.Zcs[i] = self.mix.substances[i].Zc
            self.Vcs[i] = self.mix.substances[i].Vc
            self.Tcs[i] = self.mix.substances[i].Tc
            self.Pcs[i] = self.mix.substances[i].Pc
            self.omegas[i] = self.mix.substances[i].omega

        self._initialize()
        self._computeParameters()

    def _initialize(self):

        if self.eosValue == "van_der_waals_1890":
            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += (0.125 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                thetas.append(0.42188 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i])

            self._calculate_theta_mixture(thetas)
            self.delta = 0.0
            self.epsilon = 0.0

        elif self.eosValue == "redlich_and_kwong_1949":
            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += (0.08664 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                thetas.append(
                    (0.42748 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i])
                    / (self.T / self.Tcs[i]) ** 0.5
                )

            self._calculate_theta_mixture(thetas)
            self.delta = self.b
            self.epsilon = 0.0

        elif self.eosValue == "wilson_1964":
            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += (0.08664 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                a = 0.42748 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                alpha = (self.T / self.Tcs[i]) * (
                    1
                    + (1.57 + 1.62 * self.omegas[i])
                    * (1.0 / (self.T / self.Tcs[i]) - 1.0)
                )
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = self.b
            self.epsilon = 0.0

        elif self.eosValue == "soave_1972":
            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += (0.08664 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                a = 0.42748 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                alpha = (
                    1.0
                    + (0.48 + 1.574 * self.omegas[i] - 0.176 * self.omegas[i] ** 2)
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = self.b
            self.epsilon = 0.0

        elif self.eosValue == "peng_and_robinson_1976":

            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += self.y[i] * (0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i])))
                _tmpthetas = (
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
                ) * (0.45724 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i])
                thetas.append(_tmpthetas)

            self._calculate_theta_mixture(thetas)
            self.delta = 2 * self.b
            self.epsilon = -self.b * self.b

        elif self.eosValue == "peneloux_et_al_1982":
            thetas = []
            self.b = 0
            c = 0
            for i in range(self.n):
                a = 0.42748 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                c += (
                    0.40768
                    * (R_IG * self.Tcs[i] / self.Pcs[i])
                    * (0.00385 + 0.08775 * self.omegas[i])
                ) * self.y[i]
                self.b += (0.08664 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                alpha = (
                    1.0
                    + (0.48 + 1.574 * self.omegas[i] - 0.176 * self.omegas[i] ** 2)
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)
            self.b = self.b - c
            self._calculate_theta_mixture(thetas)
            self.delta = self.b + 2 * c
            self.epsilon = c * (self.b + c)

        elif self.eosValue == "patel_and_teja_1982":
            thetas = []
            self.b = 0
            c = 0
            for i in range(self.n):
                F = 0.45241 + 1.30982 * self.omegas[i] - 0.295937 * self.omegas[i] ** 2
                zeta_c = (
                    0.32903
                    - 0.076799 * self.omegas[i]
                    + 0.0211947 * self.omegas[i] ** 2
                )
                r = np.atleast_1d(
                    solve_cubic(1, 2 - 3 * zeta_c, 3 * zeta_c ** 2, -zeta_c ** 3)
                )
                omega_b = np.min(r[r >= 0])
                omega_c = 1 - 3 * zeta_c
                omega_a = (
                    3 * zeta_c ** 2
                    + 3 * (1 - 2 * zeta_c) * omega_b
                    + omega_b ** 2
                    + 1
                    - 3 * zeta_c
                )
                c += self.y[i]*omega_c * R_IG * self.Tcs[i] / self.Pcs[i]
                self.b += self.y[i]*omega_b * R_IG * self.Tcs[i] / self.Pcs[i]
                alpha = (1 + F * (1 - (self.T / self.Tcs[i]) ** 0.5)) ** 2
                a = omega_a * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                thetas.append(a * alpha)
            self._calculate_theta_mixture(thetas)
            self.delta = self.b + c
            self.epsilon = -self.b * c

        elif self.eosValue == "adachi_et_al_1983":
            thetas = []
            self.b = 0
            c = 0
            b1, b2, b3 = 0, 0, 0
            for i in range(self.n):
                b1 += self.y[i]*(
                    R_IG
                    * self.Tcs[i]
                    * (
                        0.08974
                        - 0.03452 * self.omegas[i]
                        + 0.00330 * self.omegas[i] ** 2
                    )
                    / self.Pcs[i]
                )
                b2 += self.y[i]*(
                    R_IG
                    * self.Tcs[i]
                    * (
                        0.03686
                        + 0.00405 * self.omegas[i]
                        - 0.01073 * self.omegas[i] ** 2
                        + 0.00157 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )
                b3 += self.y[i]*(
                    R_IG
                    * self.Tcs[i]
                    * (
                        0.154
                        + 0.14122 * self.omegas[i]
                        - 0.00272 * self.omegas[i] ** 2
                        - 0.00484 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )

                a = (
                    (R_IG * self.Tcs[i]) ** 2
                    * (
                        0.44869
                        + 0.04024 * self.omegas[i]
                        + 0.01111 * self.omegas[i] ** 2
                        - 0.00576 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )
                alpha = (
                    1
                    + (0.407 + 1.3787 * self.omegas[i] - 0.2933 * self.omegas[i] ** 2)
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)

            self.b = b1
            self._calculate_theta_mixture(thetas)
            self.delta = b3 - b2
            self.epsilon = -b2 * b3

        elif self.eosValue == "soave_1984":
            thetas = []
            self.b = 0
            self.epsilon = 0
            for i in range(self.n):
                self.b += (0.08333 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                self.epsilon += (
                    0.001736 / (self.Pcs[i] / (R_IG * self.Tcs[i])) ** 2 * self.y[i]
                )
                a = 0.42188 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                alpha = (
                    1.0
                    + (
                        0.4998
                        + 1.5928 * self.omegas[i]
                        - 0.19563 * self.omegas[i] ** 2
                        + 0.025 * self.omegas[i] ** 3
                    )
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = self.b

        elif self.eosValue == "adachi_et_al_1985":
            thetas = []
            self.b = 0
            c = 0
            for i in range(self.n):
                a = (
                    (R_IG * self.Tcs[i]) ** 2
                    * (
                        0.43711
                        + 0.02366 * self.omegas[i]
                        + 0.10538 * self.omegas[i] ** 2
                        + 0.10164 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )
                self.b += self.y[i] * (
                    (R_IG * self.Tcs[i])
                    * (
                        0.08779
                        - 0.02181 * self.omegas[i]
                        - 0.06708 * self.omegas[i] ** 2
                        + 0.10617 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )
                c += self.y[i] * (
                    (R_IG * self.Tcs[i])
                    * (
                        0.0506
                        + 0.04184 * self.omegas[i]
                        + 0.16413 * self.omegas[i] ** 2
                        - 0.03975 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )
                alpha = (
                    1
                    + (
                        0.4406
                        + 1.7039 * self.omegas[i]
                        - 1.729 * self.omegas[i] ** 2
                        + 0.9929 * self.omegas[i] ** 3
                    )
                    * (1 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = 2 * c
            self.epsilon = -c ** 2

        elif self.eosValue == "twu_et_al_1995":
            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += self.y[i]*(R_IG * self.Tcs[i]) * 0.0777960739039 / self.Pcs[i]
                a = (R_IG * self.Tcs[i]) ** 2 * 0.457235528921 / self.Pcs[i]
                alpha0 = (self.T / self.Tcs[i]) ** (
                    -0.171813
                ) * 2.718281828459045235360 ** (
                    0.125283 * (1 - (self.T / self.Tcs[i]) ** 1.77634)
                )
                alpha1 = (self.T / self.Tcs[i]) ** (
                    -0.607352
                ) * 2.718281828459045235360 ** (
                    0.511614 * (1 - (self.T / self.Tcs[i]) ** 2.20517)
                )
                alpha = alpha0 + self.omegas[i] * (alpha1 - alpha0)
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = self.b * 2
            self.epsilon = -self.b ** 2

        elif self.eosValue == "ahlers_gmehling_2001":
            thetas = []
            self.b = 0
            c = 0
            for i in range(self.n):
                a = 0.45724 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                alpha = (
                    1.0
                    + (
                        0.37464
                        + 1.54226 * self.omegas[i]
                        - 0.2699 * self.omegas[i] ** 2
                    )
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                gamma = 246.78 * self.Zcs[i] ** 2 - 107.21 * self.Zcs[i] + 12.67
                n = -74.458 * self.Zcs[i] + 26.966
                beta = 0.35 / (
                    0.35 + (n * np.abs((self.T / self.Tcs[i]) - alpha)) ** gamma
                )
                cc = (
                    (0.3074 - self.Zcs[i]) * R_IG * (self.T / self.Tcs[i]) / self.Pcs[i]
                )
                c += (cc * beta) * self.y[i]
                self.b += self.y[i] * 0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i]))
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.b = self.b - c
            self.delta = self.b * 2
            self.epsilon = -self.b * self.b + 4 * self.b * c - 2 * c ** 2

        elif self.eosValue == "gasem_et_al_pr_2001":
            thetas = []
            self.b = 0
            for i in range(self.n):
                a = 0.45724 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                self.b += self.y[i] * 0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i]))
                alpha = (
                    1.0
                    + (
                        0.386590
                        + 1.50226 * self.omegas[i]
                        - 0.1687 * self.omegas[i] ** 2
                    )
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = 2 * self.b
            self.epsilon = -self.b ** 2

        elif self.eosValue == "gasem_et_al_twu_2001":
            thetas = []
            self.b = 0
            for i in range(self.n):
                a = 0.45724 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                self.b += self.y[i] * 0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i]))
                alpha0 = (self.T / self.Tcs[i]) ** (
                    -0.207176
                ) * 2.718281828459045235360 ** (
                    0.092099 * (1 - (self.T / self.Tcs[i]) ** 1.94800)
                )
                alpha1 = (self.T / self.Tcs[i]) ** (
                    -0.502297
                ) * 2.718281828459045235360 ** (
                    0.603486 * (1 - (self.T / self.Tcs[i]) ** 2.09626)
                )
                alpha = alpha0 + self.omegas[i] * (alpha1 - alpha0)
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = 2 * self.b
            self.epsilon = -self.b ** 2

        else:
            raise ValueError("Equation of state doesn't exists in the current database")

        # ========= END OF self._initialize() ===============

    def _calculate_theta_mixture(self, thetas):
        self.theta = 0
        for i in range(self.n):
            inner_sum = 0
            for j in range(self.n):
                inner_sum += (
                    self.y[i]
                    * self.y[j]
                    * sp.sqrt(thetas[i] * thetas[j])
                    * (1 - self.k[i][j])
                )
            self.theta += inner_sum

    def getAllProps(
        self, Tref: float, T: float, Pref: float, P: float
    ) -> (Props, Props):
        log = ""

        zs = self.getZfromPT(P, T)
        zliq, zvap = np.min(zs), np.max(zs)
        vliq, vvap = zliq * R_IG * T / P, zvap * R_IG * T / P

        avgMolWt = self.mix.getMolWt()
        if avgMolWt:
            rholiq, rhovap = avgMolWt * 1e-3 / vliq, avgMolWt * 1e-3 / vvap
        else:
            rholiq, rhovap = 0, 0

        if self.mix.hasCp():
            igprops = self.mix.getIGProps(Tref, T, Pref, P)
            log += self.mix.getCpLog(Tref, T)
            pliq, pvap = self.getCpHSGUA(Tref, T, Pref, P)
        else:
            igprops = 0
            pliq, pvap = 0, 0
            log += "Couldn't calculate properties: missing Cp paramaters"

        fl, fv = self.getFugacity(P, T, vliq, zliq), self.getFugacity(P, T, vvap, zvap)

        retPropsliq, retPropsvap = Props(), Props()
        retPropsliq.Z, retPropsvap.Z = zliq, zvap
        retPropsliq.V, retPropsvap.V = vliq, vvap
        retPropsliq.rho, retPropsvap.rho = rholiq, rhovap
        retPropsliq.P, retPropsvap.P = P, P
        retPropsliq.T, retPropsvap.T = T, T
        retPropsliq.Fugacity, retPropsvap.Fugacity = fl, fv
        retPropsliq.IGProps, retPropsvap.IGProps = igprops, igprops
        retPropsliq.Props, retPropsvap.Props = pliq, pvap
        retPropsliq.log, retPropsvap.log = log, log

        return retPropsliq, retPropsvap

    def getCpHSGUA(self, Tref: float, T: float, Pref: float, P: float):
        zs = self.getZfromPT(P, T)
        zsref = self.getZfromPT(Pref, Tref)

        zliq, zvap = np.min(zs), np.max(zs)
        zliqref, zvapref = np.min(zsref), np.max(zsref)

        vliq, vvap = zliq * R_IG * T / P, zvap * R_IG * T / P
        vliqref, vvapref = zliqref * R_IG * Tref / Pref, zvapref * R_IG * Tref / Pref

        igprop = self.mix.getIGProps(
            Tref, T, Pref, P
        )  # make sure that mixture can handle single substances

        ddp_liq = self.getDeltaDepartureProps(
            Pref, Tref, vliqref, zliqref, P, T, vliq, zliq
        )
        ddp_vap = self.getDeltaDepartureProps(
            Pref, Tref, vvapref, zvapref, P, T, vvap, zvap
        )
        pliq = igprop.subtract(ddp_liq)
        pvap = igprop.subtract(ddp_vap)

        return pliq, pvap
