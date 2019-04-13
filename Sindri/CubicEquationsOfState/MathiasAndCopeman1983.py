from CubicEquationsOfState.PengAndRobinson1976 import PR1976, thetaiPR1976
import numpy as np
from typing import List
from compounds import SubstanceProp


class thetaiMathiasCopeman1983(thetaiPR1976):
    def __init__(self):
        self.subset = ["water", "methanol", "ethanol"]

    def c1(self, i: int, substances: List[SubstanceProp]):
        w = substances[i].omega
        name = substances[i].Name
        if name in self.subset:
            _c1 = 1.0113 * w * w + 1.1538 * w + 0.4021
        else:
            _c1 = 0.3906 + 1.4031 * w + 0.1316 * w * w

        return _c1

    def c2(self, i: int, substances: List[SubstanceProp]):
        w = substances[i].omega
        name = substances[i].Name
        if name in self.subset:
            _c2 = -7.7867 * w * w + 2.2590 * w - 0.2011
        else:
            _c2 = -1.3127 * w * w + 0.3015 * w - 0.1213
        return _c2

    def c3(self, i: int, substances: List[SubstanceProp]):
        w = substances[i].omega
        name = substances[i].Name
        if name in self.subset:
            _c3 = w * w * 2.8127 - 1.0040 * w + 0.3964
        else:
            _c3 = 0.7661 * w + 0.3041
        return _c3

    def alpha(self, i: int, T: float, substances):
        c1 = self.c1(i, substances)
        c2 = self.c2(i, substances)
        c3 = self.c3(i, substances)
        tr = T / substances[i].Tc
        return (
            np.exp(c1 * (1 - tr))
            * (1 + c2 * (1 - tr ** 0.5) ** 2 + c3 * (1 - tr ** 0.5) ** 3) ** 2
        )


class MathiasCopeman1983(PR1976):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Mathias and Copeman (1983)"
        self.thetaiBehavior = thetaiMathiasCopeman1983()
