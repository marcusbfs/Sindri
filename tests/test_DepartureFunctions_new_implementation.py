import numpy as np

from TPCAE.Factories.EOSMixFactory import createEOSMix
from TPCAE.compounds import SubstanceProp, MixtureProp
from TPCAE.CubicEOS import CubicEOS
from TPCAE.eos import EOS
from TPCAE.constants import R_IG

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


def test_first_pure_substance_PR1976():

    subs = [methane]
    y = [1.0]

    eosname = "Peng and Robinson (1976)"
    mix = MixtureProp(subs, [1.0])
    eoseq = EOS(mix, [[0]], eosname)

    eos = createEOSMix(subs, eosname)

    p = 1e5
    t = 150
    pref = 1e5
    tref = 300

    zs = eoseq.getZfromPT(p, t)
    zliq = np.min(zs)
    zvap = np.max(zs)
    vliq, vvap = zliq * R_IG * t / p, zvap * R_IG * t / p

    v_allProps = eoseq.getAllProps(tref, t, pref, p)

    zs = eos.getZfromPT(p, t, y)
    zliq = np.min(zs)
    zvap = np.max(zs)
    vliq, vvap = zliq * R_IG * t / p, zvap * R_IG * t / p

    calc_allProps = eos.getAllProps(y, tref, t, pref, p)

    i = 0
    j = 1
    # assert U
    np.testing.assert_allclose(calc_allProps[i].Props.U, v_allProps[i].Props.U, 1e-5)
    np.testing.assert_allclose(calc_allProps[j].Props.U, v_allProps[j].Props.U, 1e-5)
    # assert H
    np.testing.assert_allclose(calc_allProps[i].Props.H, v_allProps[i].Props.H, 1e-5)
    np.testing.assert_allclose(calc_allProps[j].Props.H, v_allProps[j].Props.H, 1e-5)
    # assert S
    np.testing.assert_allclose(calc_allProps[i].Props.S, v_allProps[i].Props.S, 1e-5)
    np.testing.assert_allclose(calc_allProps[j].Props.S, v_allProps[j].Props.S, 1e-5)
    # assert G
    np.testing.assert_allclose(calc_allProps[i].Props.G, v_allProps[i].Props.G, 1e-5)
    np.testing.assert_allclose(calc_allProps[j].Props.G, v_allProps[j].Props.G, 1e-5)
    # assert A
    np.testing.assert_allclose(calc_allProps[i].Props.A, v_allProps[i].Props.A, 1e-5)
    np.testing.assert_allclose(calc_allProps[j].Props.A, v_allProps[j].Props.A, 1e-5)
