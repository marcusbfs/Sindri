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
        return 0.125 * R_IG * self.mix[i].Tc / self.mix[i].Pc

    def thetai(self, i, T):
        return 0.42188 * (R_IG * self.mix[i].Tc) ** 2 / self.mix[i].Pc

    def thetam(self, y, T):
        s = 0
        for i in range(len(y)):
            s += y[i] * self.thetai(i, T) ** 0.5
        return s ** 2

    def getZfromPT(self, P, T, y):

        b = self.bm(y)
        theta = self.thetam(y, T)
        delta = 0
        epsilon = 0

        _Bl = b * P / (R_IG * T)
        _deltal = delta * P / (R_IG * T)
        _thetal = theta * P / (R_IG * T) ** 2
        _epsilonl = epsilon * (P / (R_IG * T)) ** 2

        # coefficients Z**3 + a0*Z**2 + a1*Z + a2 = 0
        _a0 = _deltal - _Bl - 1
        _a1 = _thetal + _epsilonl - _deltal * (_Bl + 1)
        _a2 = -(_epsilonl * (_Bl + 1) + _thetal * _Bl)

        roots = np.asarray(solve_cubic(1.0, _a0, _a1, _a2))
        real_values = roots[roots > 0]
        return real_values

    def phi_i(self, i, y, P, T, Z):
        b = self.bm(y)
        bi = self.bi(i)
        theta = self.thetam(y, T)
        thetai = self.thetai(i, T)
        v = Z * R_IG * T / P

        RT = R_IG * T
        rtlnphi = (
            RT * np.log(v / (v - b))
            - RT * np.log(Z)
            - (RT * bi / (v - b) + 2.0 * (theta * thetai) ** 0.5 / v)
        )

        return np.exp(rtlnphi / RT)


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

    def mOfAlphaFunction(self, i, T):
        k0 = (
            0.378893
            + 1.48971530 * self.mix[i].omega
            - 0.17131848 * self.mix[i].omega ** 2
            + 0.0196554 * self.mix[i].omega ** 3
        )

        k1 = 0
        name = self.mix[i].Name
        if name == "hexadecane":
            k1 = 0.02665
        elif name == "hexane":
            k1 = 0.05104
        elif name == "cyclohexane":
            k1 = 0.07023
        elif name == "methane":
            k1 = -0.00159

        Tr = T / self.mix[i].Tc
        k = k0 + k1 * (1 + Tr) * (0.7 - Tr)
        return k


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
        return np.exp((A + B * Tr) * (1.0 - Tr ** (C + w * (D + E * w))))


class VLE_Tsai1998(InterfaceEosVLE):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__()
        self.mix = np.atleast_1d(mix)
        self.k = k

    def ti(self, i, T):
        k1 = self.k1(i)
        k3 = self.k3(i)
        k2 = self.k2(k3)
        Tr_pow_two_thirds = (T / self.mix[i].Tc) ** (2.0 / 3.0)

        return (R_IG * self.mix[i].Tc / self.mix[i].Pc) * (
            k1 + k2 * (1.0 - Tr_pow_two_thirds) + k3 * (1.0 - Tr_pow_two_thirds) ** 2
        )

    def k1(self, i):
        w = self.mix[i].omega
        return (
            0.00185
            + 0.00438 * w
            + 0.36322 * w ** 2
            - 0.90831 * w ** 3
            + 0.5588 * w ** 4
        )

    def k2(self, k3):
        return (
            -0.00542
            - 0.51112 * k3
            + 0.04533 * k3 ** 2
            + 0.07447 * k3 ** 3
            - 0.03831 * k3 ** 4
        )

    def tm(self, y, T):
        s = 0
        for i in range(len(y)):
            s += y[i] * self.ti(i, T)
        return s

    def bi(self, i):
        return 0.0778 * R_IG * self.mix[i].Tc / self.mix[i].Pc

    def thetai(self, i, T):
        return (
            0.45724 * (R_IG * self.mix[i].Tc) ** 2 / self.mix[i].Pc * self.alpha(i, T)
        )

    def alpha(self, i, T):
        Tr = T / self.mix[i].Tc
        w = self.mix[i].omega

        M = (
            0.20473
            + 0.83548 * w
            - 0.18470 * w ** 2
            + 0.16675 * w ** 3
            - 0.09881 * w ** 4
        )
        N = 0

        name = self.mix[i].Name

        if name == "water":
            N = 0.11560
        elif name == "methanol":
            N = 0.03221

        alp = (1 + M * (1 - Tr) + N * (1 - Tr) * (0.7 - Tr)) ** 2
        return alp

    def k3(self, i):
        k = 0
        name = self.mix[i].Name
        if name == "water":
            k = 0.01471
        elif name == "methanol":
            k = -0.04426
        return k

    def thetam(self, y, T):
        n = len(y)
        _thetam = 0
        for i in range(n):
            s = 0
            for j in range(n):
                s += (
                    y[i]
                    * y[j]
                    * (1 - self.k[i][j])
                    * (self.thetai(i, T) * self.thetai(j, T)) ** 0.5
                )
            _thetam += s
        return _thetam

    def bm(self, y):
        s = 0
        for i in range(len(y)):
            s += y[i] * self.bi(i)
        return s

    def phi_i(self, i, y, P, T, Z):
        bi = self.bi(i)
        tm = self.tm(y, T)

        while P < (1.0 - Z) * R_IG * T / tm:
            print(P)
            P = 1.1 * (1.0 - Z) * R_IG * T / tm
            print(P)
            tm = self.tm(y, T)

        tbar = P * tm / (R_IG * T)
        a = self.thetam(y, T)
        b = self.bm(y)

        A = P * a / (R_IG * T) ** 2
        B = P * b / (R_IG * T)

        xjaij = 0

        for j in range(len(y)):
            xjaij += (
                y[j]
                * (1 - self.k[i][j])
                * (self.thetai(i, T) * self.thetai(j, T)) ** 0.5
            )

        Z_plus_tbar_minus_1 = Z + tbar - 1.0
        termo1 = Z_plus_tbar_minus_1 * bi / B
        # if Z_plus_tbar_minus_1 > 0:
        #     termo2 = -np.log(Z_plus_tbar_minus_1)
        # else:
        #     termo2 = 0.0
        termo2 = -np.log(Z_plus_tbar_minus_1)
        if Z_plus_tbar_minus_1 < 0:
            print("Z + tbar -1 = ", Z_plus_tbar_minus_1)
        else:
            print("Z ok T = {}, P = {}".format(str(T), str(P)))

        termo3 = -(A / (2 * (2 * B) ** 0.5))
        termo4 = 2 * xjaij / A - bi / B
        termo5 = np.log(
            (Z + tbar + B * (1 + 2 ** 0.5)) / (Z + tbar + B * (1 - 2 ** 0.5))
        )

        lnphi = termo1 + termo2 + termo3 * termo4 * termo5

        # (Z + tbar - 1) * bi / B
        # - np.log(Z + tbar - 1)
        # - (A / (2 * (2 * B) ** 0.5))
        # * (2 * xjaij / A - bi / B)
        # * np.log((Z + tbar + B * (1 + 2 ** 0.5)) / (Z + tbar + B * (1 - 2 ** 0.5)))
        return np.exp(lnphi)

    def getZfromPT(self, P, T, y):

        bb = self.bm(y)
        tm = self.tm(y, T)
        theta = self.thetam(y, T)
        b = bb - tm

        delta = 2 * b
        epsilon = -b ** 2 + 4 * b * tm - 2 * tm ** 2

        _Bl = b * P / (R_IG * T)
        _deltal = delta * P / (R_IG * T)
        _thetal = theta * P / (R_IG * T) ** 2
        _epsilonl = epsilon * (P / (R_IG * T)) ** 2

        # coefficients Z**3 + a0*Z**2 + a1*Z + a2 = 0
        _a0 = _deltal - _Bl - 1
        _a1 = _thetal + _epsilonl - _deltal * (_Bl + 1)
        _a2 = -(_epsilonl * (_Bl + 1) + _thetal * _Bl)

        roots = np.asarray(solve_cubic(1, _a0, _a1, _a2))
        real_values = roots[roots > 0]
        return real_values


class VLE_Mathias_Copeman1983(VLE_PR1976):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__(mix, k)
        self.subset = ["water", "methanol", "ethanol"]

    def alphafunction(self, i, T):
        c1 = self.c1(i)
        c2 = self.c2(i)
        c3 = self.c3(i)
        tr = T / self.mix[i].Tc

        return (
            np.exp(c1 * (1 - tr))
            * (1 + c2 * (1 - tr ** 0.5) ** 2 + c3 * (1 - tr ** 0.5) ** 3) ** 2
        )

    def c1(self, i):
        w = self.mix[i].omega
        name = self.mix[i].Name
        if name in self.subset:
            _c1 = 1.0113 * w * w + 1.1538 * w + 0.4021
        else:
            _c1 = 0.3906 + 1.4031 * w + 0.1316 * w * w

        return _c1

    def c2(self, i):
        w = self.mix[i].omega
        name = self.mix[i].Name
        if name in self.subset:
            _c2 = -7.7867 * w * w + 2.2590 * w - 0.2011
        else:
            _c2 = -1.3127 * w * w + 0.3015 * w - 0.1213
        return _c2

    def c3(self, i):
        w = self.mix[i].omega
        name = self.mix[i].Name
        if name in self.subset:
            _c3 = w * w * 2.8127 - 1.0040 * w + 0.3964
        else:
            _c3 = 0.7661 * w + 0.3041
        return _c3


class VLE_Coquelet_2004(VLE_Mathias_Copeman1983):
    def __init__(self, mix, k):
        # interface: bi, thetai, getZfromPT, phi_i
        super().__init__(mix, k)

    def c1(self, i):
        w = self.mix[i].omega
        name = self.mix[i].Name
        if name in self.subset:
            _c1 = 1.3569 * w * w + 0.9957 * w + 0.4077
        else:
            _c1 = 0.1441 * w * w + 1.3838 * w + 0.387

        return _c1

    def c2(self, i):
        w = self.mix[i].omega
        name = self.mix[i].Name
        if name in self.subset:
            _c2 = -11.2986 * w * w + 3.5590 * w - 0.1146
        else:
            _c2 = -2.5214 * w * w + 0.6939 * w + 0.0325
        return _c2

    def c3(self, i):
        w = self.mix[i].omega
        name = self.mix[i].Name
        if name in self.subset:
            _c3 = w * w * 11.7802 - 3.890 * w + 0.5033
        else:
            _c3 = 0.6225 * w + 0.2236
        return _c3
