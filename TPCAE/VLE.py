import os

import numpy as np
from numba import njit, float64, int64

import VLEBinaryDiagrams
from constants import R_IG, DBL_EPSILON
from polyEqSolver import solve_cubic
from units import conv_unit

from VLEEOSIterfaces import *

vle_options = {
    # "van der Waals (1890)": "van_der_waals_1890",
    # "Redlich and Kwong (1949)": "redlich_and_kwong_1949",
    "Soave (1972)": "soave_1972",
    "Peng and Robinson (1976)": "peng_and_robinson_1976",
    # "Péneloux, et al. (1982)": "peneloux_et_al_1982",
    # "Patel and Teja (1982)": "patel_and_teja_1982",
    "Mathias and Copeman (1983)": "mathias_and_copeman_1983",
    "Stryjek and Vera (1986)": "stryjek_and_vera_1986",
    "Twu, et al. (1995)": "twu_et_al_1995",
    # "Tsai and Chen (1998)": "tsai_and_chen_1998",
    "Gasem, et al. PR modification (2001)": "gasem_et_al_pr_2001",
    "Gasem, et al. Twu modificaton (2001)": "gasem_et_al_twu_2001",
    "Gasem, et al.(2001)": "gasem_et_al_2001",
    "Coquelet, et al. (2004)": "coquelet_et_al_2004",
}

calc_options = {
    "Bubble-point Pressure": "bubbleP",
    "Dew-point Pressure": "dewP",
    "Bubble-point Temperature": "bubbleT",
    "Dew-point Temperature": "dewT",
    "Flash": "flash",
}


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
        elif self.eosval == "van_der_waals_1890":
            self.eoseq = VLE_VanDerWalls(self.mix, self.k)
        elif self.eosval == "redlich_and_kwong_1949":
            self.eoseq = VLE_RK1949(self.mix, self.k)
        elif self.eosval == "soave_1972":
            self.eoseq = VLE_Soave1972(self.mix, self.k)
        elif self.eosval == "patel_and_teja_1982":
            self.eoseq = VLE_PatelTeja1982(self.mix, self.k)
        elif self.eosval == "twu_et_al_1995":
            self.eoseq = VLE_TwuEtAl1995(self.mix, self.k)
        elif self.eosval == "stryjek_and_vera_1986":
            self.eoseq = VLE_Stryjek1986(self.mix, self.k)
        elif self.eosval == "gasem_et_al_pr_2001":
            self.eoseq = VLE_Gasem_et_al_PR_2001(self.mix, self.k)
        elif self.eosval == "gasem_et_al_twu_2001":
            self.eoseq = VLE_Gasem_et_al_Twu_2001(self.mix, self.k)
        elif self.eosval == "gasem_et_al_2001":
            self.eoseq = VLE_Gasem_et_al_2001(self.mix, self.k)
        elif self.eosval == "tsai_and_chen_1998":
            self.eoseq = VLE_Tsai1998(self.mix, self.k)
        elif self.eosval == "mathias_and_copeman_1983":
            self.eoseq = VLE_Mathias_Copeman1983(self.mix, self.k)
        elif self.eosval == "coquelet_et_al_2004":
            self.eoseq = VLE_Coquelet_2004(self.mix, self.k)

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

    # TODO optimize this!
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

        # tb = np.sum(x * Tbi)
        tb = _helper_bubble_T_guess_from_wilson(
            x, P, np.sum(x * Tbi), self.Pcs, self.Tcs, self.omegas
        )

        k = np.exp(
            np.log(self.Pcs / P) + 5.373 * (1 + self.omegas) * (1.0 - self.Tcs / tb)
        )
        # y = np.full(self.n, 1.0 / self.n)
        y = x * k / np.sum(x * k)

        err = 100
        ite = 0

        phivap = np.empty(self.n, dtype=np.float64)
        philiq = np.empty(self.n, dtype=np.float64)
        diffk = np.empty(self.n, dtype=np.float64)
        h = 1e-3

        while err > tol and ite < kmax:
            ite += 1

            zsvap = self.getZ(P, tb, y)
            zsliq = self.getZ(P, tb, x)

            zvap = np.max(zsvap)
            zliq = np.min(zsliq)

            for i in range(self.n):
                phivap[i] = self.getPhi_i(i, y, P, tb, zvap)
                philiq[i] = self.getPhi_i(i, x, P, tb, zliq)
                dphiv = self._getdiffPhi_i_respT(i, y, P, tb, zvap)
                dphil = self._getdiffPhi_i_respT(i, x, P, tb, zliq)
                diffk[i] = (-dphil * phivap[i] + philiq[i] * dphiv) / philiq[i] ** 2

                # dphiv = self._getdiffPhi_i_respT(i, y, P, tb, zvap)
                # dphil = self._getdiffPhi_i_respT(i, x, P, tb, zliq)
                # diffk[i] = (dphil * phivap[i] - philiq[i] * dphiv) / phivap[i] ** 2

            k = philiq / phivap
            tb = tb - (np.sum(y / k) - 1.0) / (np.sum(y * diffk))

            # k = philiq / phivap
            # tb = tb - (np.sum(x * k) - 1.0) / (np.sum(x * diffk))

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

        title = "{} (1) / {} (2) at {:0.3f} {}\nEquation of state: {}".format(
            self.mix[0].Name,
            self.mix[1].Name,
            conv_unit(P, "Pa", Punit),
            Punit,
            self.eos,
        )

        vleplot = VLEBinaryDiagrams.VLEBinaryMixturePlot(
            "isobaric", T, x, y, Tunit, title, plottype
        )
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

        title = "{} (1) / {} (2) at {:0.3f} {}\nEquation of state: {}".format(
            self.mix[0].Name,
            self.mix[1].Name,
            conv_unit(T, "K", Tunit),
            Tunit,
            self.eos,
        )

        vleplot = VLEBinaryDiagrams.VLEBinaryMixturePlot(
            "isothermal", P, x, y, Punit, title, plottype
        )
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
    return 1.0 / np.sum(y / (Pcs * np.exp(5.373 * (1.0 + omegas) * (1.0 - Tcs / T))))


@njit(
    float64(float64[:], float64, float64, float64[:], float64[:], float64[:]),
    cache=True,
)
def _helper_f_for_temperature_bubble_point_guess(x, P, T, Pcs, Tcs, omegas):
    return -P + np.sum(Pcs * x * np.exp(5.373 * (1.0 + omegas) * (1.0 - Tcs / T)))


@njit(
    float64(float64[:], float64, float64, float64[:], float64[:], float64[:]),
    cache=True,
)
def _helper_diff_f_for_temperature_bubble_point_guess(x, P, T, Pcs, Tcs, omegas):
    h = 1e-3
    f1 = _helper_f_for_temperature_bubble_point_guess(x, P, T + h, Pcs, Tcs, omegas)
    f2 = _helper_f_for_temperature_bubble_point_guess(x, P, T - h, Pcs, Tcs, omegas)
    return (f1 - f2) / (2.0 * h)


@njit(
    float64(float64[:], float64, float64, float64[:], float64[:], float64[:]),
    cache=True,
)
def _helper_bubble_T_guess_from_wilson(x, P, T, Pcs, Tcs, omegas):

    tol = 1e-8
    kmax = 1000
    k = 0
    err = 999

    while k < kmax and err < tol:

        k += 1
        told = T - _helper_f_for_temperature_bubble_point_guess(
            x, P, T, Pcs, Tcs, omegas
        ) / _helper_diff_f_for_temperature_bubble_point_guess(x, P, T, Pcs, Tcs, omegas)
        err = T - told
        T = told

    return T
