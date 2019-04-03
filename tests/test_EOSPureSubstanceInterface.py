import numpy as np

from TPCAE.compounds import SubstanceProp, MixtureProp
from EOSPureSubstanceInterface import EOSPureSubstanceInterface
from eos import EOS

methane = SubstanceProp("methane", "CH4")
ethane = SubstanceProp("ethane", "C2H4")
water = SubstanceProp("water", "H2O")
heptane = SubstanceProp("heptane", "C7H16")
pentane = SubstanceProp("pentane", "C5H12")
hexane = SubstanceProp("hexane", "C6H14")
benzene = SubstanceProp("benzene", "C6H6")
isobutanol = SubstanceProp("2-methyl-1-propanol (isobutanol)", "C4H10O")
cyclopentane = SubstanceProp("cyclopentane", "C5H10")

eosname = "Peng and Robinson (1976)"
k2 = [[0, 0], [0, 0]]


def test_EOSPuresubstancesInterface_PR1976():

    eosname = "Peng and Robinson (1976)"
    subs = [methane]
    y = [1.0]
    k = [[0]]
    p = 1e5
    t = 150


    # test Z
    eos_PSI = EOSPureSubstanceInterface(subs, eosname)
    eos_old = EOS(MixtureProp(subs, [1.0]), k, eosname)

    zsPSI = eos_PSI.getZfromPT(p, t)
    zs_old = eos_old.getZfromPT(p, t)

    np.testing.assert_allclose(np.min(zs_old), np.min(zsPSI), 1e-5)
    np.testing.assert_allclose(np.max(zs_old), np.max(zsPSI), 1e-5)

    # test pvp
    pvp_aw = subs[0].getPvpAW(t)
    pvp_old = eos_old.getPvp(t, pvp_aw)[0]
    pvp_PSI = eos_PSI.getPvp(t, pvp_aw)[0]
    np.testing.assert_allclose(pvp_PSI, pvp_old, 1e-5)
