import numpy as np
from EOSMixture import EOSMixture
from CubicEquationsOfState.PengAndRobinson1976 import PengAndRobinson1976
from CubicEquationsOfState.vanderWaals1890 import vanderWaals1890
from CubicEquationsOfState.RedlichAndKwong1949 import RedlichAndKwong1949

_subs = []
_k = []


def createEOSMix(substances, eostype: str, k=None) -> EOSMixture:

    if k is None:
        n = len(substances)
        k = np.zeros((n, n), dtype=np.float64)

    if eostype == "van der Waals (1890)":
        return vanderWaals1890(substances, k)
    elif eostype == "Redlich and Kwong (1949)":
        return RedlichAndKwong1949(substances, k)
    elif eostype == "Peng and Robinson (1976)":
        return PengAndRobinson1976(substances, k)
    else:
        return None

def getEOSMixOptions():
    options = ["van der Waals (1890)",
        "Peng and Robinson (1976)",
               ]
    return options
