import numpy as np

from TPCAE.Factories.EOSMixFactory import createEOSMix
from TPCAE.compounds import SubstanceProp

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

    eosname = "Peng and Robinson (1976)"
    subs = [benzene]
    y = [1.0]
    # subs = [benzene, isobutanol, cyclopentane]
    # y = [.2, .3, .5]
    eos = createEOSMix(subs, eosname)

    p = 0.5e6
    t = 315
    z = eos.getZfromPT(p, t, y)
    zvap = np.max(z)
    zliq = np.min(z)

    phi_vap = np.zeros(len(eos.substances))
    phi_liq = np.zeros(len(eos.substances))

    for i in range(len(phi_liq)):
        phi_vap[i] = eos.getPhi_i(i, y, p, t, zvap)
        phi_liq[i] = eos.getPhi_i(i, y, p, t, zliq)

    fvap = phi_vap[0] * p
    fliq = phi_liq[0] * p

    print("Z: ", z)
    print("Phi_vap: ", phi_vap)
    print("Phi_liq: ", phi_liq)
    print("f_vap: ", phi_vap * p)
    print("f_liq: ", phi_liq * p)

    np.testing.assert_allclose(zvap, 0.759411, 1e-4)
    np.testing.assert_allclose(fvap, 4.04938217e05, 1e-5)
    np.testing.assert_allclose(fliq, 2.76022341e04, 1e-5)


def test_first_pure_substance_vdW1890():

    eosname = "van der Waals (1890)"
    subs = [benzene]
    # subs = [benzene, isobutanol, cyclopentane]
    eos = createEOSMix(subs, eosname)

    p = 0.5e6
    t = 315
    y = [1.0]
    # y = [.2, .3, .5]
    z = eos.getZfromPT(p, t, y)
    zvap = np.max(z)
    zliq = np.min(z)

    phi_vap = np.zeros(len(eos.substances))
    phi_liq = np.zeros(len(eos.substances))

    for i in range(len(phi_liq)):
        phi_vap[i] = eos.getPhi_i(i, y, p, t, zvap)
        phi_liq[i] = eos.getPhi_i(i, y, p, t, zliq)

    fvap = phi_vap[0] * p
    fliq = phi_liq[0] * p

    print("Z: ", z)
    print("Phi_vap: ", phi_vap)
    print("Phi_liq: ", phi_liq)
    print("f_vap: ", phi_vap * p)
    print("f_liq: ", phi_liq * p)

    np.testing.assert_allclose(zvap, 0.869055, 1e-4)
    np.testing.assert_allclose(fvap, 4.42619581e05, 1e-5)
    np.testing.assert_allclose(fliq, 2.68466414e05, 1e-5)


def test_first_pure_substance_RK1949():

    eosname = "Redlich and Kwong (1949)"
    subs = [benzene]
    # subs = [benzene, isobutanol, cyclopentane]
    eos = createEOSMix(subs, eosname)

    p = 0.5e6
    t = 315
    y = [1.0]
    # y = [.2, .3, .5]
    z = eos.getZfromPT(p, t, y)
    zvap = np.max(z)
    zliq = np.min(z)

    phi_vap = np.zeros(len(eos.substances))
    phi_liq = np.zeros(len(eos.substances))

    for i in range(len(phi_liq)):
        phi_vap[i] = eos.getPhi_i(i, y, p, t, zvap)
        phi_liq[i] = eos.getPhi_i(i, y, p, t, zliq)

    fvap = phi_vap[0] * p
    fliq = phi_liq[0] * p

    print("Z: ", z)
    print("Phi_vap: ", phi_vap)
    print("Phi_liq: ", phi_liq)
    print("f_vap: ", phi_vap * p)
    print("f_liq: ", phi_liq * p)

    np.testing.assert_allclose(zvap, 0.789930, 1e-4)
    np.testing.assert_allclose(fvap, 4.14795536e05, 1e-5)
    np.testing.assert_allclose(fliq, 4.72348414e04, 1e-5)


def test_first_pure_substance_Soave1972():

    eosname = "Soave (1972)"
    subs = [benzene]
    # subs = [benzene, isobutanol, cyclopentane]
    eos = createEOSMix(subs, eosname)

    p = 0.5e6
    t = 315
    y = [1.0]
    # y = [.2, .3, .5]
    z = eos.getZfromPT(p, t, y)
    zvap = np.max(z)
    zliq = np.min(z)

    phi_vap = np.zeros(len(eos.substances))
    phi_liq = np.zeros(len(eos.substances))

    for i in range(len(phi_liq)):
        phi_vap[i] = eos.getPhi_i(i, y, p, t, zvap)
        phi_liq[i] = eos.getPhi_i(i, y, p, t, zliq)

    fvap = phi_vap[0] * p
    fliq = phi_liq[0] * p

    print("Z: ", z)
    print("Phi_vap: ", phi_vap)
    print("Phi_liq: ", phi_liq)
    print("f_vap: ", phi_vap * p)
    print("f_liq: ", phi_liq * p)

    np.testing.assert_allclose(zvap, 0.763462, 1e-4)
    np.testing.assert_allclose(fvap, 4.06896003e05, 1e-5)
    np.testing.assert_allclose(fliq, 2.66674564e04, 1e-5)


def test_first_pure_substance_Wilson1964():

    eosname = "Wilson (1964)"
    subs = [benzene]
    # subs = [benzene, isobutanol, cyclopentane]
    eos = createEOSMix(subs, eosname)

    p = 0.5e6
    t = 315
    y = [1.0]
    # y = [.2, .3, .5]
    z = eos.getZfromPT(p, t, y)
    zvap = np.max(z)
    zliq = np.min(z)

    phi_vap = np.zeros(len(eos.substances))
    phi_liq = np.zeros(len(eos.substances))

    for i in range(len(phi_liq)):
        phi_vap[i] = eos.getPhi_i(i, y, p, t, zvap)
        phi_liq[i] = eos.getPhi_i(i, y, p, t, zliq)

    fvap = phi_vap[0] * p
    fliq = phi_liq[0] * p

    print("Z: ", z)
    print("Phi_vap: ", phi_vap)
    print("Phi_liq: ", phi_liq)
    print("f_vap: ", phi_vap * p)
    print("f_liq: ", phi_liq * p)

    np.testing.assert_allclose(zvap, 0.774546, 1e-4)
    np.testing.assert_allclose(fvap, 4.10128953e05, 1e-5)
    np.testing.assert_allclose(fliq, 3.36971456e04, 1e-5)


def test_first_pure_substance_Penelou82():

    eosname = "Péneloux, et al. (1982)"
    subs = [benzene]
    # subs = [benzene, isobutanol, cyclopentane]
    eos = createEOSMix(subs, eosname)

    p = 0.5e6
    t = 315
    y = [1.0]
    # y = [.2, .3, .5]
    z = eos.getZfromPT(p, t, y)
    zvap = np.max(z)
    zliq = np.min(z)

    phi_vap = np.zeros(len(eos.substances))
    phi_liq = np.zeros(len(eos.substances))

    for i in range(len(phi_liq)):
        phi_vap[i] = eos.getPhi_i(i, y, p, t, zvap)
        phi_liq[i] = eos.getPhi_i(i, y, p, t, zliq)

    fvap = phi_vap[0] * p
    fliq = phi_liq[0] * p

    print("Z: ", z)
    print("Phi_vap: ", phi_vap)
    print("Phi_liq: ", phi_liq)
    print("f_vap: ", phi_vap * p)
    print("f_liq: ", phi_liq * p)

    np.testing.assert_allclose(zvap, 0.76180662, 1e-4)
    np.testing.assert_allclose(fvap, 406223.03952859, 1e-5)
    np.testing.assert_allclose(fliq, 26623.35123666, 1e-5)


def test_first_pure_substance_PatelAndTeja1982():

    eosname = "Patel and Teja (1982)"
    subs = [benzene]
    # subs = [benzene, isobutanol, cyclopentane]
    eos = createEOSMix(subs, eosname)

    p = 0.5e6
    t = 315
    y = [1.0]
    # y = [.2, .3, .5]
    z = eos.getZfromPT(p, t, y)
    zvap = np.max(z)
    zliq = np.min(z)

    phi_vap = np.zeros(len(eos.substances))
    phi_liq = np.zeros(len(eos.substances))

    for i in range(len(phi_liq)):
        phi_vap[i] = eos.getPhi_i(i, y, p, t, zvap)
        phi_liq[i] = eos.getPhi_i(i, y, p, t, zliq)

    fvap = phi_vap[0] * p
    fliq = phi_liq[0] * p

    print("Z: ", z)
    print("Phi_vap: ", phi_vap)
    print("Phi_liq: ", phi_liq)
    print("f_vap: ", phi_vap * p)
    print("f_liq: ", phi_liq * p)

    np.testing.assert_allclose(zvap, 0.760510, 1e-4)
    np.testing.assert_allclose(fvap, 4.05451153e05, 1e-5)
    np.testing.assert_allclose(fliq, 2.74252319e04, 1e-5)


def test_first_pure_substance_Adachi1983():

    eosname = "Adachi, et al. (1983)"
    subs = [benzene]
    # subs = [benzene, isobutanol, cyclopentane]
    eos = createEOSMix(subs, eosname)

    p = 0.5e6
    t = 315
    y = [1.0]
    # y = [.2, .3, .5]
    z = eos.getZfromPT(p, t, y)
    zvap = np.max(z)
    zliq = np.min(z)

    phi_vap = np.zeros(len(eos.substances))
    phi_liq = np.zeros(len(eos.substances))

    for i in range(len(phi_liq)):
        phi_vap[i] = eos.getPhi_i(i, y, p, t, zvap)
        phi_liq[i] = eos.getPhi_i(i, y, p, t, zliq)

    fvap = phi_vap[0] * p
    fliq = phi_liq[0] * p

    print("Z: ", z)
    print("Phi_vap: ", phi_vap)
    print("Phi_liq: ", phi_liq)
    print("f_vap: ", phi_vap * p)
    print("f_liq: ", phi_liq * p)

    np.testing.assert_allclose(zvap, 0.760526, 1e-4)
    np.testing.assert_allclose(fvap, 4.05358883e05, 1e-5)
    np.testing.assert_allclose(fliq, 2.77327856e04, 1e-5)
