from typing import List

import numpy as np

from CubicEquationsOfState.vanderWaals1890 import thetaivanderWaals1890, vanderWaals1890
from compounds import SubstanceProp


class thetaiSoave1984(thetaivanderWaals1890):
    def m(self, i: int, T: float, substances: List[SubstanceProp]):
        w = substances[i].omega
        return 0.4998 + w * (1.5928 + w * (-0.19563 + w * 0.025))

    def alpha(self, i: int, T: float, substances: List[SubstanceProp]):
        tr = T / substances[i].Tc
        m = self.m(i, T, substances)
        return (1.0 + m * (1.0 - np.sqrt(tr))) ** 2

    def getThetai(self, i: int, T: float, substances: List[SubstanceProp]) -> float:
        a = self.a(i, T, substances)
        alpha = self.alpha(i, T, substances)
        return a * alpha


class Soave1984(vanderWaals1890):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Soave (1984)"
        self.thetaiBehavior = thetaiSoave1984()
