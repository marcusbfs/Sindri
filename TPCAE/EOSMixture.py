import numpy as np
from scipy.integrate import quad

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
from constants import R_IG, DBL_EPSILON
from polyEqSolver import solve_cubic
from typing import List
from compounds import SubstanceProp


class EOSMixture:
    def __init__(self, _subs : List[SubstanceProp], _k):
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
        real_values = roots[roots > 0]
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
        h = 1e-4
        z_plus_h = self.getZfromPT(P, T + h, y)
        z_minus_h = self.getZfromPT(P, T - h, y)
        zs = (z_plus_h - z_minus_h) / (2.0 * h)
        return np.min(zs), np.max(zs)

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
            h = 1e-4
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
