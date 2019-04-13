from CubicEquationsOfState.MathiasAndCopeman1983 import (
    MathiasCopeman1983,
    thetaiMathiasCopeman1983,
)
import numpy as np
from typing import List
from compounds import SubstanceProp


class thetaiCoquelet2004(thetaiMathiasCopeman1983):
    def c1(self, i: int, substances: List[SubstanceProp]):
        w = substances[i].omega
        name = substances[i].Name
        if name in self.subset:
            _c1 = 1.3569 * w * w + 0.9957 * w + 0.4077
        else:
            _c1 = 0.1441 * w * w + 1.3838 * w + 0.387

        return _c1

    def c2(self, i: int, substances: List[SubstanceProp]):
        w = substances[i].omega
        name = substances[i].Name
        if name in self.subset:
            _c2 = -11.2986 * w * w + 3.5590 * w - 0.1146
        else:
            _c2 = -2.5214 * w * w + 0.6939 * w + 0.0325
        return _c2

    def c3(self, i: int, substances: List[SubstanceProp]):
        w = substances[i].omega
        name = substances[i].Name
        if name in self.subset:
            _c3 = w * w * 11.7802 - 3.890 * w + 0.5033
        else:
            _c3 = 0.6225 * w + 0.2236
        return _c3


class Coquelet2004(MathiasCopeman1983):
    def __init__(self, _subs, _k):
        super().__init__(_subs, _k)
        self.eosname = "Coquelet, et al. (2004)"
        self.thetaiBehavior = thetaiCoquelet2004()
