from TPCAE.VLE import *

from TPCAE.compounds import MixtureProp, SubstanceProp
import numpy as np
from TPCAE.Factories.EOSMixFactory import createEOSMix
from TPCAE.Factories.MixtureFactory import createMix


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

from CubicEquationsOfState.PengAndRobinson1976 import PengAndRobinson1976


def test_first_test():

    eosname = "Peng and Robinson (1976)"
    eosname = "Redlich and Kwong (1949)"

    subs = [benzene, isobutanol, cyclopentane]
    eospr1976 = createEOSMix(subs, eosname)

    p = .5e6
    t = 315
    y = [0.2, .3, 0.5]

    z = eospr1976.getZfromPT(p, t, y)
    zvap = np.max(z)
    zliq = np.min(z)

    phi_vap = np.zeros(len(eospr1976.substances))
    phi_liq = np.zeros(len(eospr1976.substances))

    for i in range(len(phi_liq)):
        phi_vap[i] = eospr1976.getPhi_i(i, y, p, t, zvap)
        phi_liq[i] = eospr1976.getPhi_i(i, y, p, t, zliq)

    print(z)
    print(phi_vap)
    print(phi_liq)

    np.testing.assert_allclose(zvap, .75689381, 1e-5)
    np.testing.assert_allclose(zliq, .01747042, 1e-5)

    np.testing.assert_allclose(.0553975, phi_liq[0], 1e-5)
    np.testing.assert_allclose(.809883, phi_vap[0], 1e-5)

    np.testing.assert_allclose(.0129818, phi_liq[1], 1e-5)
    np.testing.assert_allclose(.752854, phi_vap[1], 1e-5)

    np.testing.assert_allclose(.16218, phi_liq[2], 1e-5)
    np.testing.assert_allclose(.84289, phi_vap[2], 1e-5)

