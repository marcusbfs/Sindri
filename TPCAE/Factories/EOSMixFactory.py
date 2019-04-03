import numpy as np

from CubicEquationsOfState.AdachiEtAl1983 import Adachi1983
from CubicEquationsOfState.PatelAndTeja1982 import PT1982
from CubicEquationsOfState.PenelouxEtAl1982 import PenelouxEtAl1982
from CubicEquationsOfState.PengAndRobinson1976 import PR1976
from CubicEquationsOfState.RedlichAndKwong1949 import RedlichAndKwong1949
from CubicEquationsOfState.Soave1972 import Soave1972
from CubicEquationsOfState.Soave1984 import Soave1984
from CubicEquationsOfState.Wilson1964 import Wilson1964
from CubicEquationsOfState.vanderWaals1890 import vanderWaals1890
from CubicEquationsOfState.AdachiEtAl1985 import Adachi1985
from CubicEquationsOfState.StryjekAndVera1986 import SV1986
from CubicEquationsOfState.Twu1995 import Twu1995
from CubicEquationsOfState.GasemEtAlPRmod2001 import GasemPRmod2001
from CubicEquationsOfState.GasemEtAlTwuMod2001 import GasemTwuMod2001
from CubicEquationsOfState.GasemEtAl2001 import Gasem2001
from CubicEquationsOfState.MathiasAndCopeman1983 import MathiasCopeman1983
from CubicEquationsOfState.Coquelet2004 import Coquelet2004
from EOSMixture import EOSMixture
from compounds import SubstanceProp
from typing import List

_subs = []
_k = []


def createEOSMix(substances: List[SubstanceProp], eostype: str, k=None) -> EOSMixture:

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
    elif eostype == "Mathias and Copeman (1983)":
        return MathiasCopeman1983(substances, k)
    elif eostype == "Soave (1984)":
        return Soave1984(substances, k)
    elif eostype == "Adachi, et al. (1985)":
        return Adachi1985(substances, k)
    elif eostype == "Stryjek and Vera (1986)":
        return SV1986(substances, k)
    elif eostype == "Twu, et al. (1995)":
        return Twu1995(substances, k)
    # elif eostype == "Ahlers-Gmehling (2001)":
    #     return Twu1995(substances, k)
    elif eostype == "Gasem, et al. PR modification (2001)":
        return GasemPRmod2001(substances, k)
    elif eostype == "Gasem, et al. Twu modification (2001)":
        return GasemTwuMod2001(substances, k)
    elif eostype == "Gasem, et al. (2001)":
        return Gasem2001(substances, k)
    elif eostype == "Coquelet, et al. (2004)":
        return Coquelet2004(substances, k)
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
        "Mathias and Copeman (1983)",
        "Soave (1984)",
        "Adachi, et al. (1985)",
        "Stryjek and Vera (1986)",
        "Twu, et al. (1995)",
        # "Ahlers-Gmehling (2001)",
        "Gasem, et al. PR modification (2001)",
        "Gasem, et al. Twu modification (2001)",
        "Gasem, et al. (2001)",
        "Coquelet, et al. (2004)",
    ]
    return options
