import os
from typing import List

import numpy as np
from numba import njit, float64, int64
from scipy.integrate import quad

import VLEBinaryDiagrams
from EOSParametersBehavior.ParametersBehaviorInterface import (
    BiBehavior,
    DeltaiBehavior,
    ThetaiBehavior,
    EpsiloniBehavior,
)
from MixtureRules.MixtureRulesInterface import (
    DeltaMixtureRuleBehavior,
    EpsilonMixtureRuleBehavior,
    MixtureRuleBehavior,
)
from Properties import DeltaProp, Props
from compounds import MixtureProp
from compounds import SubstanceProp
from constants import R_IG, DBL_EPSILON
from polyEqSolver import solve_cubic
from units import conv_unit

x_vec_for_plot = [
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
    0.50,
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

calc_options = {
    "Bubble-point Pressure": "bubbleP",
    "Dew-point Pressure": "dewP",
    "Bubble-point Temperature": "bubbleT",
    "Dew-point Temperature": "dewT",
    "Flash": "flash",
}


class EOSMixture:
    def __init__(self, _subs: List[SubstanceProp], _k):
        self.substances = _subs
        self.k = _k
        self.eosname = ""
        self.mixRuleBehavior = MixtureRuleBehavior()
        self.thetaiBehavior = ThetaiBehavior()
        self.biBehavior = BiBehavior()
        # TODO remove deltai and epsiloni?
        self.deltaiBehavior = DeltaiBehavior()
        self.epsiloniBehavior = EpsiloniBehavior()
        self.deltaMixBehavior = DeltaMixtureRuleBehavior()
        self.epsilonMixBehavior = EpsilonMixtureRuleBehavior()
        self.n = len(self.substances)

        self.Vcs = np.zeros(self.n)
        self.Pcs = np.zeros(self.n)
        self.Tcs = np.zeros(self.n)
        self.omegas = np.zeros(self.n)

        for i in range(self.n):
            self.Vcs[i] = self.substances[i].Vc
            self.Tcs[i] = self.substances[i].Tc
            self.Pcs[i] = self.substances[i].Pc
            self.omegas[i] = self.substances[i].omega

    def getZfromPT(self, P: float, T: float, y):

        b = self.mixRuleBehavior.bm(y, T, self.biBehavior, self.substances)
        theta = self.mixRuleBehavior.thetam(
            y, T, self.thetaiBehavior, self.substances, self.k
        )
        delta = self.deltaMixBehavior.deltam(
            y, T, self.biBehavior, self.mixRuleBehavior, self.substances
        )
        epsilon = self.epsilonMixBehavior.epsilonm(
            y, T, self.biBehavior, self.mixRuleBehavior, self.substances
        )

        Bl = b * P / (R_IG * T)
        deltal = delta * P / (R_IG * T)
        epsilonl = epsilon * np.power(P / (R_IG * T), 2)
        thetal = theta * P / np.power(R_IG * T, 2)

        # 0 = ax ^ 3 + b * x ^ 2 + c * x + d
        _a = 1.0
        _b = deltal - Bl - 1.0
        _c = thetal + epsilonl - deltal * (1.0 + Bl)
        _d = -(epsilonl * (Bl + 1.0) + Bl * thetal)

        roots = np.asarray(solve_cubic(_a, _b, _c, _d))
        real_values = roots[roots >= 0]
        return real_values

    def getPhi_i(self, i: int, y, P: float, T: float, Z: float):

        RT = R_IG * T

        V = RT * Z / P

        bm = self.mixRuleBehavior.bm(y, T, self.biBehavior, self.substances)

        thetam = self.mixRuleBehavior.thetam(
            y, T, self.thetaiBehavior, self.substances, self.k
        )

        deltam = self.deltaMixBehavior.deltam(
            y, T, self.biBehavior, self.mixRuleBehavior, self.substances
        )

        epsilonm = self.epsilonMixBehavior.epsilonm(
            y, T, self.biBehavior, self.mixRuleBehavior, self.substances
        )

        deltam2_minus_4epislonm = deltam * deltam - 4.0 * epsilonm

        # derivatives
        diffthetam = self.mixRuleBehavior.diffThetam(
            i, y, T, self.thetaiBehavior, self.substances, self.k
        )
        diffbm = self.mixRuleBehavior.diffBm(i, y, T, self.biBehavior, self.substances)
        diffdeltam = self.deltaMixBehavior.diffDeltam(
            i, y, T, self.biBehavior, self.mixRuleBehavior, self.substances
        )
        diffepsilonm = self.epsilonMixBehavior.diffEpsilonm(
            i, y, T, self.biBehavior, self.mixRuleBehavior, self.substances
        )
        deltaN = deltam * diffdeltam * 2.0 - 4.0 * diffepsilonm

        if abs(deltam2_minus_4epislonm) < 100 * DBL_EPSILON:
            substitute_term = -1.0 / (V + deltam / 2.0)
            first_term = substitute_term * diffthetam / RT
            last_term = diffbm / (V - bm) - np.log((V - bm) / V) - np.log(Z)
            return np.exp(first_term + last_term)

        sqrt_d2_minus_4eps = np.sqrt(deltam2_minus_4epislonm)
        twoV_plus_deltam_minus_sqrtd24eps = 2.0 * V + deltam - sqrt_d2_minus_4eps
        twoV_plus_deltam_plus_sqrtd24eps = 2.0 * V + deltam + sqrt_d2_minus_4eps

        # Equation(Poling, 2001)

        firstline = (1.0 / sqrt_d2_minus_4eps) * (diffthetam / RT) - (
            thetam / RT
        ) * deltaN / (2.0 * np.power(deltam2_minus_4epislonm, 1.5))

        secline_p1 = np.log(
            twoV_plus_deltam_minus_sqrtd24eps / twoV_plus_deltam_plus_sqrtd24eps
        )

        secline_p2 = (thetam / RT) / sqrt_d2_minus_4eps

        thirdline = (
            (diffdeltam - deltaN / (2.0 * sqrt_d2_minus_4eps))
            / twoV_plus_deltam_minus_sqrtd24eps
            - (diffdeltam + deltaN / (2.0 * sqrt_d2_minus_4eps))
            / twoV_plus_deltam_plus_sqrtd24eps
        )

        fourthline = diffbm / (V - bm) - np.log((V - bm) / V) - np.log(Z)

        lnphi_i = firstline * secline_p1 + secline_p2 * thirdline + fourthline
        phi_i = np.exp(lnphi_i)
        return phi_i

    def getFugacity(self, y, _P: float, _T: float, _V: float, _Z: float) -> float:
        f = 0.0
        for i in range(self.n):
            f += y[i] * self.getPhi_i(i, y, _P, _T, _Z)
        return f * _P

    def getAllProps(
        self, y, Tref: float, T: float, Pref: float, P: float
    ) -> (Props, Props):
        log = ""

        zs = self.getZfromPT(P, T, y)
        zliq, zvap = np.min(zs), np.max(zs)
        vliq, vvap = zliq * R_IG * T / P, zvap * R_IG * T / P

        MixSubs = MixtureProp(self.substances, y)
        avgMolWt = MixSubs.getMolWt()

        if avgMolWt:
            rholiq, rhovap = avgMolWt * 1e-3 / vliq, avgMolWt * 1e-3 / vvap
        else:
            rholiq, rhovap = 0, 0

        if MixSubs.hasCp():
            igprops = MixSubs.getIGProps(Tref, T, Pref, P)
            log += MixSubs.getCpLog(Tref, T)
            pliq, pvap = self.getCpHSGUA(y, Tref, T, Pref, P)
        else:
            igprops = 0
            pliq, pvap = 0, 0
            log += "Couldn't calculate properties: missing Cp paramaters"

        fl, fv = (
            self.getFugacity(y, P, T, vliq, zliq),
            self.getFugacity(y, P, T, vvap, zvap),
        )

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

    def getdZdT(self, P: float, T: float, y) -> [float, float]:
        h = 1e-5
        z_plus_h = self.getZfromPT(P, T + h, y)
        z_minus_h = self.getZfromPT(P, T - h, y)
        zs = (z_plus_h - z_minus_h) / (2.0 * h)
        return np.min(zs), np.max(zs)

    # TODO speed up this part with numba
    def getDepartureProps(self, y, P, T, V, Z):
        def _Zfunc(v, t):
            bm = self.mixRuleBehavior.bm(y, t, self.biBehavior, self.substances)
            thetam = self.mixRuleBehavior.thetam(
                y, t, self.thetaiBehavior, self.substances, self.k
            )
            delta = self.deltaMixBehavior.deltam(
                y, t, self.biBehavior, self.mixRuleBehavior, self.substances
            )
            epsilon = self.epsilonMixBehavior.epsilonm(
                y, t, self.biBehavior, self.mixRuleBehavior, self.substances
            )
            return v / (v - bm) - (thetam / (R_IG * t)) * v / (
                v ** 2 + v * delta + epsilon
            )

        def _dZdT(v, t):
            h = 1e-5
            return (_Zfunc(v, t + h) - _Zfunc(v, t - h)) / (2.0 * h)

        def _URfunc(v, t):
            return t * _dZdT(v, t) / v

        def _ARfunc(v, t):
            return (1.0 - _Zfunc(v, t)) / v

        # calculate UR
        nhau = _URfunc(V, T)
        UR_RT = quad(_URfunc, V, np.inf, args=(T,))[0]
        UR = UR_RT * T * R_IG
        # calculate AR
        AR_RT = quad(_ARfunc, V, np.inf, args=(T,))[0] + np.log(Z)
        AR = AR_RT * T * R_IG
        # calculate HR
        HR_RT = UR_RT + 1.0 - Z
        HR = HR_RT * R_IG * T
        # calculate SR
        SR_R = UR_RT - AR_RT
        SR = SR_R * R_IG
        # calculate GR
        GR_RT = AR_RT + 1 - Z
        GR = GR_RT * R_IG * T

        ret = DeltaProp(0, HR, SR, GR, UR, AR)
        return ret

    def getDeltaDepartureProps(
        self,
        y,
        _Pref: float,
        _Tref: float,
        _Vref: float,
        _Zref: float,
        _P: float,
        _T: float,
        _V: float,
        _Z: float,
    ) -> DeltaProp:
        ref = self.getDepartureProps(y, _Pref, _Tref, _Vref, _Zref)
        state = self.getDepartureProps(y, _P, _T, _V, _Z)
        delta = state.subtract(ref)
        return delta

    def getCpHSGUA(self, y, Tref: float, T: float, Pref: float, P: float):
        zs = self.getZfromPT(P, T, y)
        zsref = self.getZfromPT(Pref, Tref, y)

        zliq, zvap = np.min(zs), np.max(zs)
        zliqref, zvapref = np.min(zsref), np.max(zsref)

        vliq, vvap = zliq * R_IG * T / P, zvap * R_IG * T / P
        vliqref, vvapref = zliqref * R_IG * Tref / Pref, zvapref * R_IG * Tref / Pref
        MixSubs = MixtureProp(self.substances, y)

        igprop = MixSubs.getIGProps(
            Tref, T, Pref, P
        )  # make sure that mixture can handle single substances

        ddp_liq = self.getDeltaDepartureProps(
            y, Pref, Tref, vliqref, zliqref, P, T, vliq, zliq
        )
        ddp_vap = self.getDeltaDepartureProps(
            y, Pref, Tref, vvapref, zvapref, P, T, vvap, zvap
        )
        pliq = igprop.subtract(ddp_liq)
        pvap = igprop.subtract(ddp_vap)

        return pliq, pvap

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

            zsvap = self.getZfromPT(pb, T, y)
            zsliq = self.getZfromPT(pb, T, x)

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
        x = x / np.sum(x)

        err = 100
        ite = 0

        phivap = np.empty(self.n, dtype=np.float64)
        philiq = np.empty(self.n, dtype=np.float64)

        while err > tol and ite < kmax:
            ite += 1

            zsvap = self.getZfromPT(pd, T, y)
            zsliq = self.getZfromPT(pd, T, x)

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

    # TODO optimize this! here, I used the secant method for Tb convergence.
    def getBubblePointTemperature(self, x, P, tol=1e3 * DBL_EPSILON, kmax=100):

        assert len(x) == self.n
        x = np.atleast_1d(x)
        assert np.sum(x) == 1.0

        Tbi = np.empty(self.n)
        for i in range(self.n):
            if self.substances[i].Tb > 0:
                Tbi[i] = self.substances[i].Tb
            else:
                Tbi[i] = 100.0

        tb = _helper_bubble_T_guess_from_wilson(
            x, P, np.sum(x * Tbi), self.Pcs, self.Tcs, self.omegas
        )

        k = np.exp(
            np.log(self.Pcs / P) + 5.373 * (1 + self.omegas) * (1.0 - self.Tcs / tb)
        )
        y = x * k / np.sum(x * k)

        err = 100
        ite = 0

        tb2 = tb
        f2 = np.sum(x * k) - 1.0

        tb1 = tb * 1.1
        k = np.exp(
            np.log(self.Pcs / P) + 5.373 * (1 + self.omegas) * (1.0 - self.Tcs / tb1)
        )
        f1 = np.sum(x * k) - 1.0

        y = x * k / np.sum(x * k)

        phivap = np.empty(self.n, dtype=np.float64)
        philiq = np.empty(self.n, dtype=np.float64)

        while err > tol and ite < kmax:
            ite += 1

            tb = tb1 - f1 * ((tb1 - tb2) / (f1 - f2))

            zsvap = self.getZfromPT(P, tb, y)
            zsliq = self.getZfromPT(P, tb, x)

            zvap = np.max(zsvap)
            zliq = np.min(zsliq)

            for i in range(self.n):
                phivap[i] = self.getPhi_i(i, y, P, tb, zvap)
                philiq[i] = self.getPhi_i(i, x, P, tb, zliq)

            k = philiq / phivap

            y = x * k
            yt = np.sum(y)
            err = np.abs(1.0 - yt)
            y = y / yt
            tb2 = tb1
            tb1 = tb
            f2 = f1
            f1 = np.sum(k * x) - 1.0

        return y, tb, phivap, philiq, k, ite

    def getDewPointTemperature(
        self, y, P: float, tol: float = 1e3 * DBL_EPSILON, kmax: int = 1000
    ):
        assert len(y) == self.n
        y = np.atleast_1d(y)
        assert np.sum(y) == 1.0

        Tdi = np.empty(self.n)

        for i in range(self.n):
            if self.substances[i].Tb > 0:
                Tdi[i] = self.substances[i].Tb
            else:
                Tdi[i] = 100.0

        td = np.sum(y * Tdi)

        k = np.exp(
            np.log(self.Pcs / P) + 5.373 * (1 + self.omegas) * (1.0 - self.Tcs / td)
        )

        td2 = td
        f2 = np.sum(y / k) - 1.0

        td1 = td * 1.1
        k = np.exp(
            np.log(self.Pcs / P) + 5.373 * (1 + self.omegas) * (1.0 - self.Tcs / td1)
        )
        f1 = np.sum(y / k) - 1.0

        err = 100
        ite = 0
        # x = np.full(self.n, 1.0 / self.n)
        x = (y / k) / np.sum(y / k)

        phivap = np.empty(self.n, dtype=np.float64)
        philiq = np.empty(self.n, dtype=np.float64)

        while err > tol and ite < kmax:
            ite += 1

            td = td1 - f1 * ((td1 - td2) / (f1 - f2))

            zsvap = self.getZfromPT(P, td, y)
            zsliq = self.getZfromPT(P, td, x)

            zvap = np.max(zsvap)
            zliq = np.min(zsliq)

            for i in range(self.n):
                phivap[i] = self.getPhi_i(i, y, P, td, zvap)
                philiq[i] = self.getPhi_i(i, x, P, td, zliq)

            k = philiq / phivap

            x = y / k
            xt = np.sum(x)
            err = np.abs(1.0 - xt)

            x = x / xt
            td2 = td1
            td1 = td
            f2 = f1
            f1 = np.sum(y / k) - 1.0

        return x, td, phivap, philiq, k, ite

    def getFlash(self, z, P, T, tol=1e5 * DBL_EPSILON, kmax=1000):

        assert self.n == len(z)
        z = np.atleast_1d(z)
        assert np.sum(z) == 1.0

        # check if is flash problem
        y, pd, pv, pl, k, ite = self.getDewPointPressure(z, T)
        x, pb, pv, pl, k, ite = self.getBubblePointPressure(z, T)

        if not (pd <= P <= pb):
            raise ValueError("P is not between Pdew and Pbubble")

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
            zsvap = self.getZfromPT(P, T, y)
            zsliq = self.getZfromPT(P, T, x)

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
            x = x_vec_for_plot

        x = np.atleast_1d(x)

        xmix = np.empty(2, dtype=np.float64)
        y = np.empty(len(x), dtype=np.float64)
        T = np.empty(len(x), dtype=np.float64)

        for i in range(len(x)):
            xmix[0] = x[i]
            xmix[1] = 1.0 - x[i]

            try:
                yres, T[i], pv, pl, k, ite = self.getBubblePointTemperature(xmix, P)
            except:
                try:
                    yres = [0, 0]
                    yres[0] = y[i - 1]
                    T[i] = T[i - 1]
                    x[i] = x[i - 1]
                except:
                    yres = [0, 0]
                    yres[0] = y[i + 1]
                    T[i] = T[i + 1]
                    x[i] = x[i + 1]

            T[i] = conv_unit(T[i], "K", Tunit)
            y[i] = yres[0]

        return x, y, T

    def isothermalBinaryMixtureGenData(self, T, x=None, Punit="Pa", Tunit="K"):

        assert self.n == 2

        if x is None:
            x = x_vec_for_plot

        x = np.atleast_1d(x)

        xmix = np.empty(2, dtype=np.float64)
        y = np.empty(len(x), dtype=np.float64)
        P = np.empty(len(x), dtype=np.float64)

        for i in range(len(x)):
            xmix[0] = x[i]
            xmix[1] = 1.0 - x[i]

            try:
                yres, P[i], pv, pl, k, ite = self.getBubblePointPressure(
                    xmix, T, tol=1e-5, kmax=100
                )
            except:
                try:
                    yres = [0, 0]
                    yres[0] = y[i - 1]
                    P[i] = P[i - 1]
                    x[i] = x[i - 1]
                except:
                    yres = [0, 0]
                    yres[0] = y[i + 1]
                    P[i] = P[i + 1]
                    x[i] = x[i + 1]
            P[i] = conv_unit(P[i], "Pa", Punit)
            y[i] = yres[0]

        return x, y, P

    def isobaricBinaryMixturePlot(
        self, P, x=None, Punit="Pa", Tunit="K", expfilename="", plottype="both"
    ):

        assert self.n == 2

        if x is None:
            x = x_vec_for_plot

        x, y, T = self.isobaricBinaryMixtureGenData(P, x, Punit=Punit, Tunit=Tunit)

        title = "{} (1) / {} (2) at {:0.3f} {}\nEquation of state: {}".format(
            self.substances[0].Name,
            self.substances[1].Name,
            conv_unit(P, "Pa", Punit),
            Punit,
            self.eosname,
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
            x = x_vec_for_plot

        x, y, P = self.isothermalBinaryMixtureGenData(T, x, Punit=Punit, Tunit=Tunit)

        title = "{} (1) / {} (2) at {:0.3f} {}\nEquation of state: {}".format(
            self.substances[0].Name,
            self.substances[1].Name,
            conv_unit(T, "K", Tunit),
            Tunit,
            self.eosname,
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
        err = np.abs(T - told)
        T = told

    return T
