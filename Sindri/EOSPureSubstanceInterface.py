from typing import List

import numpy as np

from Factories.EOSMixFactory import createEOSMix
from compounds import SubstanceProp, MixtureProp
from constants import DBL_EPSILON, R_IG
from Properties import Props


class EOSPureSubstanceInterface:
    def __init__(self, subs: List[SubstanceProp], eosname: str):
        self.eosname = eosname
        self.substances = subs
        self.n = int(len(self.substances))
        assert self.n == 1
        self.eosmix = createEOSMix(self.substances, self.eosname)
        self.y = np.ones(self.n, dtype=np.float64)
        self.mix = MixtureProp(self.substances, self.y)

    def getPvp(
        self, _T: float, _P: float, tol: float = 10.0 * DBL_EPSILON, kmax: int = 100
    ):
        for i in range(1, kmax + 1):
            Zs = self.eosmix.getZfromPT(_P, _T, self.y)
            Zl, Zv = np.min(Zs), np.max(Zs)
            Vl, Vv = Zl * R_IG * _T / _P, Zv * R_IG * _T / _P

            fL = self.eosmix.getFugacity(self.y, _P, _T, Vl, Zl)
            fV = self.eosmix.getFugacity(self.y, _P, _T, Vv, Zv)
            _P = _P * fL / fV
            error = fL / fV - 1.0
            if np.abs(error) < tol:
                return _P, i
        return _P, i

    def getZfromPT(self, _P: float, _T: float):
        return self.eosmix.getZfromPT(_P, _T, self.y)

    def getAllProps(
        self, Tref: float, T: float, Pref: float, P: float
    ) -> (Props, Props):
        return self.eosmix.getAllProps(self.y, Tref, T, Pref, P)

    def getEOSDisplayName(self):
        return self.eosname
