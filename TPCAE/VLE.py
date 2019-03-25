import sympy as sp
import numpy as np
from numba import njit, float64, int64

from polyEqSolver import solve_cubic
from constants import R_IG, DBL_EPSILON
from units import conv_unit
import os
import VLEBinaryDiagrams


vle_options = {
    "Peng and Robinson (1976)": "peng_and_robinson_1976",
    "Péneloux, et al. (1982)": "peneloux_et_al_1982",
}

calc_options = {
    "Bubble-point Pressure": "bubbleP",
    "Dew-point Pressure": "dewP",
    "Bubble-point Temperature": "bubbleT",
    "Dew-point Temperature": "dewT",
    "Flash": "flash",
}


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

    def thetai(self, i, T):
        alpha = (
            1.0
            + (0.37464 + 1.54226 * self.mix[i].omega - 0.2699 * self.mix[i].omega ** 2)
            * (1.0 - (T / self.mix[i].Tc) ** 0.5)
        ) ** 2
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
        bm = self.bm(y) + cm
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


class VLE(object):
    def __init__(self, mix, eos, k=None):

        self.mix = mix
        self.eos = eos
        self.eosval = vle_options[self.eos]
        self.bm = None
        self.b = None
        self.n = len(mix)
        self.eoseq = None

        self.Vcs = np.zeros(self.n)
        self.Pcs = np.zeros(self.n)
        self.Tcs = np.zeros(self.n)
        self.omegas = np.zeros(self.n)

        for i in range(self.n):
            self.Vcs[i] = self.mix[i].Vc
            self.Tcs[i] = self.mix[i].Tc
            self.Pcs[i] = self.mix[i].Pc
            self.omegas[i] = self.mix[i].omega

        if k is None:
            self.k = np.empty((self.n, self.n))
            for i in range(self.n):
                for j in range(self.n):
                    self.k[i][j] = 0.0
        else:
            self.k = k

        self.setup()

    def setup(self):
        if self.eosval == "peng_and_robinson_1976":
            self.eoseq = VLE_PR1976(self.mix, self.k)
        elif self.eosval == "peneloux_et_al_1982":
            self.eoseq = VLE_Peneloux1982(self.mix, self.k)

    def getZ(self, P, T, y):
        return self.eoseq.getZfromPT(P, T, y)

    def getPhi_i(self, i, y, P, T, Z):
        return self.eoseq.phi_i(i, y, P, T, Z)

    def _getPb_guess(self, x, T):
        return _helper_getPb_guess(x, T, self.Pcs, self.Tcs, self.omegas)

    def _getPd_guess(self, y, T):
        return _helper_getPd_guess(y, T, self.Pcs, self.Tcs, self.omegas)

    def getBubblePointPressure(self, x, T, tol=1e3 * DBL_EPSILON, kmax=10000):

        assert len(x) == self.n
        assert np.sum(x) == 1.0

        x = np.atleast_1d(x)
        pb = self._getPb_guess(x, T)

        k = np.exp(
            np.log(self.Pcs / pb) + 5.373 * (1 + self.omegas) * (1.0 - self.Tcs / T)
        )
        y = x * k / np.sum(x * k)

        err = 100
        ite = 0

        phivap = np.empty(self.n, dtype=np.float64)
        philiq = np.empty(self.n, dtype=np.float64)

        while err > tol and ite < kmax:
            ite += 1

            zsvap = self.getZ(pb, T, y)
            zsliq = self.getZ(pb, T, x)

            zvap = np.max(zsvap)
            zliq = np.min(zsliq)

            for i in range(self.n):
                phivap[i] = self.getPhi_i(i, y, pb, T, zvap)
                philiq[i] = self.getPhi_i(i, x, pb, T, zliq)

            k = philiq / phivap
            y = x * k
            yt = np.sum(y)
            pb = pb * yt
            err = np.abs(1.0 - yt)

        return y, pb, phivap, philiq, k, ite

    def getDewPointPressure(self, y, T, tol=1e3 * DBL_EPSILON, kmax=1000):
        assert len(y) == self.n
        assert np.sum(y) == 1.0

        y = np.atleast_1d(y)
        pd = self._getPd_guess(y, T)

        k = np.exp(
            np.log(self.Pcs / pd) + 5.373 * (1 + self.omegas) * (1.0 - self.Tcs / T)
        )
        x = y / k

        err = 100
        ite = 0

        phivap = np.empty(self.n, dtype=np.float64)
        philiq = np.empty(self.n, dtype=np.float64)

        while err > tol and ite < kmax:
            ite += 1

            zsvap = self.getZ(pd, T, y)
            zsliq = self.getZ(pd, T, x)

            zvap = np.max(zsvap)
            zliq = np.min(zsliq)

            for i in range(self.n):
                phivap[i] = self.getPhi_i(i, y, pd, T, zvap)
                philiq[i] = self.getPhi_i(i, x, pd, T, zliq)

            k = philiq / phivap
            x = y / k
            xt = np.sum(x)
            pd = pd / xt
            err = np.abs(1.0 - xt)
            x = x / xt

        return x, pd, phivap, philiq, k, ite

    def _getdiffPhi_i_respT(self, i, x, p, t, z, h=1e-4):
        return (self.getPhi_i(i, x, p, t + h, z) - self.getPhi_i(i, x, p, t - h, z)) / (
            2.0 * h
        )

    def getBubblePointTemperature(self, x, P, tol=1e3 * DBL_EPSILON, kmax=100):

        assert len(x) == self.n
        x = np.atleast_1d(x)
        assert np.sum(x) == 1.0

        Tbi = np.empty(self.n)
        for i in range(self.n):
            if self.mix[i].Tb > 0:
                Tbi[i] = self.mix[i].Tb
            else:
                Tbi[i] = 100.0

        tb = np.sum(x * Tbi)

        y = np.full(self.n, 1.0 / self.n)

        err = 100
        ite = 0

        phivap = np.empty(self.n, dtype=np.float64)
        philiq = np.empty(self.n, dtype=np.float64)
        diffk = np.empty(self.n, dtype=np.float64)

        while err > tol and ite < kmax:
            ite += 1

            zsvap = self.getZ(P, tb, y)
            zsliq = self.getZ(P, tb, x)

            zvap = np.max(zsvap)
            zliq = np.min(zsliq)

            for i in range(self.n):
                dphiv = self._getdiffPhi_i_respT(i, y, P, tb, zvap)
                dphil = self._getdiffPhi_i_respT(i, x, P, tb, zliq)
                phivap[i] = self.getPhi_i(i, y, P, tb, zvap)
                philiq[i] = self.getPhi_i(i, x, P, tb, zliq)
                diffk[i] = (dphil * phivap[i] - philiq[i] * dphiv) / phivap[i] ** 2

            k = philiq / phivap
            tb = tb - (np.sum(x * k) - 1.0) / (np.sum(x * diffk))

            y = x * k
            yt = np.sum(y)
            err = np.abs(1.0 - yt)
            y = y / yt

        return y, tb, phivap, philiq, k, ite

    def getDewPointTemperature(self, y, P, tol=1e3 * DBL_EPSILON, kmax=1000):
        assert len(y) == self.n
        y = np.atleast_1d(y)
        assert np.sum(y) == 1.0

        Tdi = np.empty(self.n)

        for i in range(self.n):
            if self.mix[i].Tb > 0:
                Tdi[i] = self.mix[i].Tb
            else:
                Tdi[i] = 100.0

        td = np.sum(y * Tdi)

        x = np.full(self.n, 1.0 / self.n)

        err = 100
        ite = 0

        phivap = np.empty(self.n, dtype=np.float64)
        philiq = np.empty(self.n, dtype=np.float64)
        diffkl = np.empty(self.n, dtype=np.float64)

        while err > tol and ite < kmax:
            ite += 1

            zsvap = self.getZ(P, td, y)
            zsliq = self.getZ(P, td, x)

            zvap = np.max(zsvap)
            zliq = np.min(zsliq)

            for i in range(self.n):
                dphiv = self._getdiffPhi_i_respT(i, y, P, td, zvap)
                dphil = self._getdiffPhi_i_respT(i, x, P, td, zliq)
                phivap[i] = self.getPhi_i(i, y, P, td, zvap)
                philiq[i] = self.getPhi_i(i, x, P, td, zliq)
                diffkl[i] = (-dphil * phivap[i] + philiq[i] * dphiv) / philiq[i] ** 2

            k = philiq / phivap
            td = td - (np.sum(y / k) - 1.0) / (np.sum(y * diffkl))

            x = y / k
            xt = np.sum(x)
            err = np.abs(1.0 - xt)
            x = x / xt

        return x, td, phivap, philiq, k, ite

    def getFlash(self, z, P, T, tol=1e5 * DBL_EPSILON, kmax=1000):

        assert self.n == len(z)
        z = np.atleast_1d(z)
        assert np.sum(z) == 1.0

        # check if is flash problem
        y, pd, pv, pl, k, ite = self.getDewPointPressure(z, T)
        x, pb, pv, pl, k, ite = self.getBubblePointPressure(z, T)

        if not (pd <= P <= pb):
            raise ValueError("P is not bewteen Pdew and Pbubble")
            return -1

        # pb = self._getPb_guess(z, T)
        # pd = self._getPd_guess(z, T)
        v = (pb - P) / (pb - pd)
        # v = 0.5

        err = 100
        ite = 0

        phivap = np.empty(self.n, dtype=np.float64)
        philiq = np.empty(self.n, dtype=np.float64)

        y = np.full(self.n, 1.0 / self.n)
        x = np.full(self.n, 1.0 / self.n)

        while err > tol and ite < kmax:
            ite += 1
            zsvap = self.getZ(P, T, y)
            zsliq = self.getZ(P, T, x)

            zvap = np.max(zsvap)
            zliq = np.min(zsliq)

            for i in range(self.n):
                phivap[i] = self.getPhi_i(i, y, P, T, zvap)
                philiq[i] = self.getPhi_i(i, x, P, T, zliq)

            k = philiq / phivap

            vold = v
            v = _RachfordRice(v, k, z, tol=1e-8, kmax=500)
            x = z / (1.0 + v * (k - 1.0))
            y = k * x
            err = np.abs(v - vold)

        return x, y, v, phivap, philiq, k, ite

    def isobaricBinaryMixtureGenData(self, P, x=None, Punit="Pa", Tunit="K"):

        assert self.n == 2

        if x is None:
            x = [
                0,
                0.01,
                0.02,
                0.03,
                0.04,
                0.06,
                0.08,
                0.1,
                0.15,
                0.2,
                0.25,
                0.3,
                0.35,
                0.4,
                0.45,
                0.5,
                0.55,
                0.6,
                0.65,
                0.7,
                0.75,
                0.8,
                0.85,
                0.9,
                0.92,
                0.94,
                0.96,
                0.97,
                0.98,
                0.99,
                1,
            ]

        x = np.atleast_1d(x)

        xmix = np.empty(2, dtype=np.float64)
        y = np.empty(len(x), dtype=np.float64)
        T = np.empty(len(x), dtype=np.float64)

        for i in range(len(x)):
            xmix[0] = x[i]
            xmix[1] = 1.0 - x[i]

            yres, T[i], pv, pl, k, ite = self.getBubblePointTemperature(xmix, P)
            T[i] = conv_unit(T[i], "K", Tunit)
            y[i] = yres[0]

        return x, y, T

    def isothermalBinaryMixtureGenData(self, T, x=None, Punit="Pa", Tunit="K"):

        assert self.n == 2

        if x is None:
            x = [
                0,
                0.01,
                0.02,
                0.03,
                0.04,
                0.06,
                0.08,
                0.1,
                0.15,
                0.2,
                0.25,
                0.3,
                0.35,
                0.4,
                0.45,
                0.5,
                0.55,
                0.6,
                0.65,
                0.7,
                0.75,
                0.8,
                0.85,
                0.9,
                0.92,
                0.94,
                0.96,
                0.97,
                0.98,
                0.99,
                1,
            ]

        x = np.atleast_1d(x)

        xmix = np.empty(2, dtype=np.float64)
        y = np.empty(len(x), dtype=np.float64)
        P = np.empty(len(x), dtype=np.float64)

        for i in range(len(x)):
            xmix[0] = x[i]
            xmix[1] = 1.0 - x[i]

            yres, P[i], pv, pl, k, ite = self.getBubblePointPressure(
                xmix, T, tol=1e-5, kmax=100
            )
            P[i] = conv_unit(P[i], "Pa", Punit)
            y[i] = yres[0]

        return x, y, P

    def isobaricBinaryMixturePlot(
        self, P, x=None, Punit="Pa", Tunit="K", expfilename="", plottype="both"
    ):

        assert self.n == 2

        if x is None:
            x = [
                0.0,
                0.01,
                0.02,
                0.03,
                0.04,
                0.06,
                0.08,
                0.1,
                0.15,
                0.2,
                0.25,
                0.3,
                0.35,
                0.4,
                0.45,
                0.5,
                0.55,
                0.6,
                0.65,
                0.7,
                0.75,
                0.8,
                0.85,
                0.9,
                0.92,
                0.94,
                0.96,
                0.97,
                0.98,
                0.99,
                1.0,
            ]

        x, y, T = self.isobaricBinaryMixtureGenData(P, x, Punit=Punit, Tunit=Tunit)

        title = "{} (1) / {} (2) at {:0.3f} {}".format(
            self.mix[0].Name, self.mix[1].Name, conv_unit(P, "Pa", Punit), Tunit
        )
        vleplot = VLEBinaryDiagrams.VLEBinaryMixturePlot("isobaric", T, x, y, Tunit, title, plottype)
        if os.path.exists(expfilename):
            vleplot.expPlot(expfilename)
        vleplot.plot()

    def isothermalBinaryMixturePlot(
        self, T, x=None, Punit="Pa", Tunit="K", expfilename="", plottype="both"
    ):

        assert self.n == 2

        if x is None:
            x = [
                0,
                0.01,
                0.02,
                0.03,
                0.04,
                0.06,
                0.08,
                0.1,
                0.15,
                0.2,
                0.25,
                0.3,
                0.35,
                0.4,
                0.45,
                0.5,
                0.55,
                0.6,
                0.65,
                0.7,
                0.75,
                0.8,
                0.85,
                0.9,
                0.92,
                0.94,
                0.96,
                0.97,
                0.98,
                0.99,
                1,
            ]

        x, y, P = self.isothermalBinaryMixtureGenData(T, x, Punit=Punit, Tunit=Tunit)
        title = "{} (1) / {} (2) at {:0.3f} {}".format(
            self.mix[0].Name, self.mix[1].Name, conv_unit(T, "K", Tunit), Tunit
        )
        vleplot = VLEBinaryDiagrams.VLEBinaryMixturePlot("isothermal", P, x, y, Punit, title, plottype)
        if os.path.exists(expfilename):
            vleplot.expPlot(expfilename)
        vleplot.plot()



@njit(float64(float64, float64[:], float64[:], float64, int64), cache=True)
def _RachfordRice(v, k, z, tol, kmax):

    v0 = v
    v1 = 999.0
    err = 1000.0

    iter = 0
    while err > tol or iter > kmax:
        iter += 1
        f = np.sum(z * (k - 1.0) / (1.0 + v0 * (k - 1.0)))
        dfdv = -np.sum(z * (k - 1.0) ** 2 / (1.0 + v0 * (k - 1.0)) ** 2)
        v1 = v0 - f / dfdv
        err = np.abs(v0 - v1)
        v0 = v1
    return v1


@njit(float64(float64[:], float64, float64[:], float64[:], float64[:]), cache=True)
def _helper_getPb_guess(x, T, Pcs, Tcs, omegas):
    x = np.atleast_1d(x)
    return np.sum(x * Pcs * np.exp(5.373 * (1.0 + omegas) * (1.0 - Tcs / T)))


@njit(float64(float64[:], float64, float64[:], float64[:], float64[:]), cache=True)
def _helper_getPd_guess(y, T, Pcs, Tcs, omegas):
    y = np.atleast_1d(y)
    return np.sum(y / (Pcs * np.exp(5.373 * (1.0 + omegas) * (1.0 - Tcs / T))))
