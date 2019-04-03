import numpy as np
from EOSMixture import EOSMixture
from scipy.integrate import quad
from CubicEOS import CubicEOS
from constants import R_IG
from compounds import MixtureProp
from Properties import DeltaProp, VaporPressure, Props
from polyEqSolver import solve_cubic
from CubicEquationsOfState.PengAndRobinson1976 import PR1976
from CubicEquationsOfState.vanderWaals1890 import vanderWaals1890
from CubicEquationsOfState.RedlichAndKwong1949 import RedlichAndKwong1949
from CubicEquationsOfState.Wilson1964 import Wilson1964
from CubicEquationsOfState.Soave1972 import Soave1972
from CubicEquationsOfState.Soave1984 import Soave1984
from CubicEquationsOfState.PenelouxEtAl1982 import PenelouxEtAl1982
from CubicEquationsOfState.PatelAndTeja1982 import PT1982
from CubicEquationsOfState.AdachiEtAl1983 import Adachi1983

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
    elif eostype == "Wilson (1964)":
        return Wilson1964(substances, k)
    elif eostype == "Soave (1972)":
        return Soave1972(substances, k)
    elif eostype == "Peng and Robinson (1976)":
        return PR1976(substances, k)
    elif eostype == "Patel and Teja (1982)":
        return PT1982(substances, k)
    elif eostype == "Péneloux, et al. (1982)":
        return PenelouxEtAl1982(substances, k)
    elif eostype == "Adachi, et al. (1983)":
        return Adachi1983(substances, k)
    elif eostype == "Soave (1984)":
        return Soave1984(substances, k)
    else:
        return None


def getEOSMixOptions():
    options = [
        "van der Waals (1890)",
        "Redlich and Kwong (1949)",
        "Wilson (1964)",
        "Soave (1972)",
        "Peng and Robinson (1976)",
        # "Schmidt and Wenzel (1979)",
        "Patel and Teja (1982)",
        "Péneloux, et al. (1982)",
        "Adachi, et al. (1983)",
        "Soave (1984)",
    ]
    return options
