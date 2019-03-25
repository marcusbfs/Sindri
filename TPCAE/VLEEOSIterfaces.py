import os

import numpy as np
from numba import njit, float64, int64

import VLEBinaryDiagrams
from constants import R_IG, DBL_EPSILON
from polyEqSolver import solve_cubic
from units import conv_unit


class InterfaceEosVLE(object):
    def __init__(self):
        self.k = None

    def bm(self, y):
        s = 0
        for i in range(len(y)):
            s += y[i] * self.bi(i)
        return s

    def thetam(self, y, T):
        s1 = 0
        for i in range(len(y)):
            s2 = 0
            for j in range(len(y)):
                s2 += (
                    y[i]
                    * y[j]
                    * np.sqrt(self.thetai(i, T) * self.thetai(j, T))
                    * (1 - self.k[i][j])
                )
            s1 += s2
        return s1

    def thetaij(self, i, j, T):
        return np.sqrt(self.thetai(i, T) * self.thetai(j, T)) * (1 - self.k[i][j])


class VLE_PR1976(InterfaceEosVLE):
    def __init__(self, mix, k):
        super().__init__()
        self.mix = np.atleast_1d(mix)
        self.k = k

    def bi(self, i):
        return 0.07780 / (self.mix[i].Pc / (R_IG * self.mix[i].Tc))

    def mOfAlphaFunction(self, i, t):
        return 0.37464 + 1.54226 * self.mix[i].omega - 0.26992 * self.mix[i].omega ** 2

    def alphafunction(self, i, T):
        alpha = (
            1.0 + self.mOfAlphaFunction(i, T) * (1.0 - (T / self.mix[i].Tc) ** 0.5)
        ) ** 2

        return alpha

    def thetai(self, i, T):
        alpha = self.alphafunction(i, T)
        return alpha * 0.45724 * (R_IG * self.mix[i].Tc) ** 2 / self.mix[i].Pc

    def getZfromPT(self, P, T, y):
        A = self.thetam(y, T) * P / (R_IG * T) ** 2
        B = self.bm(y) * P / (R_IG * T)

        roots = np.asarray(
            solve_cubic(
                1.0, -(1.0 - B), (A - 3 * B * B - 2.0 * B), -(A * B - B * B - B ** 3)
            )
        )
        real_values = roots[roots > 0]
        return real_values

    def phi_i(self, i, y, P, T, Z):
        b = self.bm(y)
        a = self.thetam(y, T)

        bi = self.bi(i)
        A = a * P / (R_IG * T) ** 2
        B = b * P / (R_IG * T)

        aji = 0
        for j in range(len(y)):
            aji += y[j] * self.thetaij(j, i, T)

        lnphi = (
            bi * (Z - 1) / b
            - np.log(Z - B)
            - A
            / (2 * B * np.sqrt(2))
            * (2 * aji / a - bi / b)
            * np.log((Z + 2.414 * B) / (Z - 0.414 * B))
        )
        return np.exp(lnphi)


class VLE_Peneloux1982(InterfaceEosVLE):
    def __init__(self, mix, k):
        # interface: bm, thetam, thetaij
        super().__init__()
        self.mix = np.atleast_1d(mix)
        self.k = k

    def ci(self, i):
        return (
            0.40768
            * (R_IG * self.mix[i].Tc / self.mix[i].Pc)
            * (0.00385 + 0.08775 * self.mix[i].omega)
        )

    def bi(self, i):
        return 0.08664 / (self.mix[i].Pc / (R_IG * self.mix[i].Tc))

    def cm(self, y):
        c = 0
        for i in range(len(y)):
            c += y[i] * self.ci(i)
        return c

    def bm(self, y):
        b = 0
        for i in range(len(y)):
            b += y[i] * self.bi(i)
        return b - self.cm(y)

    def thetai(self, i, T):
        a = 0.42748 * (R_IG * self.mix[i].Tc) ** 2 / self.mix[i].Pc
        alpha = (
            1.0
            + (0.48 + 1.574 * self.mix[i].omega - 0.176 * self.mix[i].omega ** 2)
            * (1.0 - (T / self.mix[i].Tc) ** 0.5)
        ) ** 2
        return a * alpha

    def getZfromPT(self, P, T, y):
        A = self.thetam(y, T) * P / (R_IG * T) ** 2
        B = self.bm(y) * P / (R_IG * T)

        c = self.cm(y)
        b = self.bm(y)

        delta = b + 2 * c
        epsilon = c * (b + c)
        theta = self.thetam(y, T)

        _Bl = b * P / (R_IG * T)
        _deltal = delta * P / (R_IG * T)
        _thetal = theta * P / (R_IG * T) ** 2
        _epsilonl = epsilon * (P / (R_IG * T)) ** 2

        a = 1.0
        b = _deltal - _Bl - 1
        c = _thetal + _epsilonl - _deltal * (_Bl + 1)
        d = -(_epsilonl * (_Bl + 1) + _thetal * _Bl)

        roots = np.asarray(solve_cubic(a, b, c, d))
        real_values = roots[roots > 0]
        return real_values

    def phi_i(self, i, y, P, T, Z):

        cm = self.cm(y)
        ci = self.ci(i)
        bm = self.bm(y)
        bi = self.bi(i)
        thetam = self.thetam(y, T)
        thetai = self.thetai(i, T)

        A = thetam * P / (R_IG * T) ** 2
        B = bm * P / (R_IG * T)

        lnphi_soave1972 = (
            bi * (Z - 1) / bm
            - np.log(Z - B)
            - A / B * (2.0 * np.sqrt(thetai / thetam) - bi / bm) * np.log(1 + B / Z)
        )
        lnphi = lnphi_soave1972 - ci * P / (T * R_IG)
        return np.exp(lnphi)


class VLE_VanDerWalls(InterfaceEosVLE):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__()
        self.mix = np.atleast_1d(mix)
        self.k = k

    def bi(self, i):
        return 0.125 / (self.mix[i].Pc / (R_IG * self.mix[i].Tc))

    def thetai(self, i, T):
        return 0.42188 * (R_IG * self.mix[i].Tc) ** 2 / self.mix[i].Pc

    def getZfromPT(self, P, T, y):

        b = self.bm(y)

        theta = self.thetam(y, T)

        _Bl = b * P / (R_IG * T)
        _deltal = 0
        _thetal = theta * P / (R_IG * T) ** 2
        _epsilonl = 0

        a = 1.0
        b = _deltal - _Bl - 1
        c = _thetal + _epsilonl - _deltal * (_Bl + 1)
        d = -(_epsilonl * (_Bl + 1) + _thetal * _Bl)

        roots = np.asarray(solve_cubic(a, b, c, d))
        real_values = roots[roots > 0]
        return real_values

    def phi_i(self, i, y, P, T, Z):
        b = self.bm(y)
        bi = self.bi(i)
        theta = self.thetam(y, T)
        thetai = self.thetai(i, T)
        v = Z * R_IG * T / P

        lnphi = (
            -np.log((v - b) / v)
            + bi / (v - b)
            - 2 * thetai ** 0.5 / (R_IG * T * v) * theta
            - np.log(Z)
        )
        return np.exp(lnphi)


class VLE_RK1949(InterfaceEosVLE):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__()
        self.mix = np.atleast_1d(mix)
        self.k = k

    def bi(self, i):
        return 0.08664 / (self.mix[i].Pc / (R_IG * self.mix[i].Tc))

    def thetai(self, i, T):
        return (
            0.42748
            * (R_IG * self.mix[i].Tc) ** 2
            / self.mix[i].Pc
            / np.sqrt(T / self.mix[i].Tc)
        )

    def getZfromPT(self, P, T, y):
        b = self.bm(y)
        theta = self.thetam(y, T)
        delta = b

        _Bl = b * P / (R_IG * T)
        _deltal = delta * P / (R_IG * T)
        _thetal = theta * P / (R_IG * T) ** 2
        _epsilonl = 0

        a = 1.0
        b = _deltal - _Bl - 1
        c = _thetal + _epsilonl - _deltal * (_Bl + 1)
        d = -(_epsilonl * (_Bl + 1) + _thetal * _Bl)

        roots = np.asarray(solve_cubic(a, b, c, d))
        real_values = roots[roots > 0]
        return real_values

    def phi_i(self, i, y, P, T, Z):
        bi = self.bi(i)
        thetai = self.thetai(i, T)
        Bm = self.bm(y)
        Am = self.thetam(y, T)

        Ai = np.sqrt(thetai / (R_IG ** 2 * T ** 2.5))
        Bi = bi / (R_IG * T)

        lnphi = (
            0.4343 * (Z - 1) * Bi / Bm
            - np.log(Z - Bm * P)
            - Am ** 2 / Bm * (2 * Ai / Am - Bi / Bm) * np.log(1 + Bm * P / Z)
        )
        return np.exp(lnphi)


class VLE_Soave1972(InterfaceEosVLE):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__()
        self.mix = np.atleast_1d(mix)
        self.k = k

    def bi(self, i):
        return 0.08664 * R_IG * self.mix[i].Tc / self.mix[i].Pc

    def thetai(self, i, T):
        mi = 0.48 + 1.574 * self.mix[i].omega - 0.176 * self.mix[i].omega ** 2
        alpha = (1 + mi * (1 - (T / self.mix[i].Tc) ** 0.5)) ** 2
        return alpha * 0.42747 * (R_IG * self.mix[i].Tc) ** 2 / self.mix[i].Pc

    def thetam(self, y, T):
        s = 0
        for i in range(len(y)):
            s += y[i] * self.thetai(i, T) ** 0.5
        return s ** 2

    def bm(self, y):
        s = 0
        for i in range(len(y)):
            s += y[i] * self.bi(i)
        return s

    def getZfromPT(self, P, T, y):

        A = self.thetam(y, T) * P / (R_IG * T) ** 2
        B = self.bm(y) * P / (R_IG * T)

        a = 1.0
        b = -1.0
        c = A - B * (1 + B)
        d = -A * B

        roots = np.asarray(solve_cubic(a, b, c, d))
        real_values = roots[roots > 0]
        return real_values

    def phi_i(self, i, y, P, T, Z):
        bi = self.bi(i)
        thetai = self.thetai(i, T)
        bm = self.bm(y)
        thetam = self.thetam(y, T)
        A = thetam * P / (R_IG * T) ** 2
        B = bm * P / (R_IG * T)

        lnphi = (
            bi / bm * (Z - 1)
            - np.log(Z - B)
            - A / B * (2 * (thetai / thetam) ** 0.5 - bi / bm) * np.log(1 + B / Z)
        )
        return np.exp(lnphi)


class VLE_PatelTeja1982(InterfaceEosVLE):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__()
        self.mix = np.atleast_1d(mix)
        self.k = k

    def thetai(self, i, T):

        F = 0.452413 + 1.30982 * self.mix[i].omega - 0.295937 * self.mix[i].omega ** 2
        zeta_c = (
            0.32903 - 0.076799 * self.mix[i].omega + 0.0211947 * self.mix[i].omega ** 2
        )

        r = np.atleast_1d(solve_cubic(1, 2 - 3 * zeta_c, 3 * zeta_c ** 2, -zeta_c ** 3))
        omega_b = np.min(r[r >= 0])
        omega_a = (
            3 * zeta_c ** 2
            + 3 * (1 - 2 * zeta_c) * omega_b
            + omega_b ** 2
            + 1
            - 3 * zeta_c
        )
        alpha = (1 + F * (1 - (T / self.mix[i].Tc) ** 0.5)) ** 2

        return alpha * omega_a * (R_IG * self.mix[i].Tc) ** 2 / self.mix[i].Pc

    def bi(self, i):
        zeta_c = (
            0.32903 - 0.076799 * self.mix[i].omega + 0.0211947 * self.mix[i].omega ** 2
        )

        r = np.atleast_1d(solve_cubic(1, 2 - 3 * zeta_c, 3 * zeta_c ** 2, -zeta_c ** 3))
        omega_b = np.min(r[r >= 0])
        return omega_b * (R_IG * self.mix[i].Tc) / self.mix[i].Pc

    def ci(self, i):
        zeta_c = (
            0.32903 - 0.076799 * self.mix[i].omega + 0.0211947 * self.mix[i].omega ** 2
        )
        omega_c = 1 - 3 * zeta_c
        return omega_c * (R_IG * self.mix[i].Tc) / self.mix[i].Pc

    def bm(self, y):
        s = 0
        for i in range(len(y)):
            s += y[i] * self.bi(i)
        return s

    def cm(self, y):
        s = 0
        for i in range(len(y)):
            s += y[i] * self.ci(i)
        return s

    def getZfromPT(self, P, T, y):
        b = self.bm(y)
        c = self.cm(y)
        theta = self.thetam(y, T)
        delta = b + c
        epsilon = -b * c

        _Bl = b * P / (R_IG * T)
        _deltal = delta * P / (R_IG * T)
        _thetal = theta * P / (R_IG * T) ** 2
        _epsilonl = epsilon * (P / (R_IG * T)) ** 2

        a = 1.0
        b = _deltal - _Bl - 1
        c = _thetal + _epsilonl - _deltal * (_Bl + 1)
        d = -(_epsilonl * (_Bl + 1) + _thetal * _Bl)

        roots = np.asarray(solve_cubic(a, b, c, d))
        real_values = roots[roots > 0]
        return real_values

    def phi_i(self, i, y, P, T, Z):

        bi = self.bi(i)
        thetai = self.thetai(i, T)
        bm = self.bm(y)
        thetam = self.thetam(y, T)
        ci = self.ci(i)
        cm = self.cm(y)

        B = bm * self.mix[i].Pc / (R_IG * self.mix[i].Tc)
        v = Z * R_IG * T / P

        sxthetaij = 0

        for j in range(len(y)):
            sxthetaij += y[j] * self.thetaij(i, j, T)

        d = np.sqrt(bm * cm + (bm + cm) ** 2 / 4)

        Q = v + 0.5 * (bm + cm)

        rtlnphi = (
            -R_IG * T * np.log(Z - B)
            + R_IG * T * (bi / (v - bm))
            - sxthetaij / d * np.log((Q + d) / (Q - d))
            + thetam * (bi + ci) / (2 * (Q ** 2 - d ** 2))
            + (thetam / (8 * d ** 3))
            * (ci * (3 * bm + cm) + bi * (3 * cm + bm))
            * (np.log((Q + d) / (Q - d)) + 2 * Q * d / (Q ** 2 - d ** 2))
        )

        return np.exp(rtlnphi / (R_IG * T))


class VLE_TwuEtAl1995(VLE_PR1976):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__(mix, k)

    def alphafunction(self, i, T):
        alpha0 = (T / self.mix[i].Tc) ** (-0.171813) * 2.718281828459045235360 ** (
            0.125283 * (1 - (T / self.mix[i].Tc) ** 1.77634)
        )
        alpha1 = (T / self.mix[i].Tc) ** (-0.607352) * 2.718281828459045235360 ** (
            0.511614 * (1 - (T / self.mix[i].Tc) ** 2.20517)
        )
        alpha = alpha0 + self.mix[i].omega * (alpha1 - alpha0)
        return alpha


class VLE_Stryjek1986(VLE_PR1976):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__(mix, k)

    def mOfAlphaFunction(self, i, t):
        return (
            0.378893
            + 1.48971530 * self.mix[i].omega
            - 0.17131848 * self.mix[i].omega ** 2
            + 0.0196554 * self.mix[i].omega ** 3
        )


class VLE_Gasem_et_al_PR_2001(VLE_PR1976):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__(mix, k)

    def mOfAlphaFunction(self, i, t):
        return 0.386590 + 1.50226 * self.mix[i].omega - 0.1687 * self.mix[i].omega ** 2


class VLE_Gasem_et_al_Twu_2001(VLE_PR1976):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__(mix, k)

    def alphafunction(self, i, T):

        alpha0 = (T / self.mix[i].Tc) ** (-0.207176) * 2.718281828459045235360 ** (
            0.092099 * (1 - (T / self.mix[i].Tc) ** 1.94800)
        )
        alpha1 = (T / self.mix[i].Tc) ** (-0.502297) * 2.718281828459045235360 ** (
            0.603486 * (1 - (T / self.mix[i].Tc) ** 2.09626)
        )
        alpha = alpha0 + self.mix[i].omega * (alpha1 - alpha0)
        return alpha


class VLE_Gasem_et_al_2001(VLE_PR1976):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__(mix, k)

    def alphafunction(self, i, T):

        A = 2.0
        B = 0.836
        C = 0.134
        D = 0.508
        E = -0.0467

        Tr = T / self.mix[i].Tc
        w = self.mix[i].omega
        return np.exp((A + B * Tr) * (1. - Tr ** (C + w * (D + E * w))))
