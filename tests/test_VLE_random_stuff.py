import numpy as np

# from TPCAE.VLE import *
from TPCAE.Factories.EOSMixFactory import createEOSMix as VLE
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


def test_phi_i_vrau():
    eosname = "Peng and Robinson (1976)"
    eq = VLE([benzene, isobutanol, cyclopentane], eosname)
    x = [0.2, 0.3, 0.5]
    t = 315
    p = 0.5e6
    zs = eq.getZfromPT(p, t, x)
    zvap = np.max(zs)
    zliq = np.min(zs)
    phi_vap = eq.getPhi_i(0, x, p, t, zvap)
    phi_liq = eq.getPhi_i(0, x, p, t, zliq)
    print(zvap, zliq)
    print(phi_vap, phi_liq)
    y, pb, phivap, philiq, k, ite = eq.getBubblePointPressure(x, t)
    print("Pb: ", pb)
    print("y: ", y)
    print("Ite: ", ite)


def test_inconsistency():
    k = [[0, 0], [0, 0]]
    eosname = "Peng and Robinson (1976)"
    eq = VLE([pentane, hexane], eosname)
    x = [0.01, 0.99]
    t = 298.7

    y, p, phivap, philiq, k, ite = eq.getBubblePointPressure(x, t)
    print(y)
    print(p)


def test_pr1976():
    eq = VLE([methane], eosname)
    p = 1e5
    t = 150
    y = [1]

    z = eq.getZfromPT(p, t, y)
    zmax, zmin = np.max(z), np.min(z)
    np.testing.assert_allclose(0.9845, zmax, 1e-2)
    np.testing.assert_allclose(0.003341, zmin, 1e-2)

    phivap = eq.getPhi_i(0, y, p, t, zmax)
    philiq = eq.getPhi_i(0, y, p, t, zmin)

    print(phivap, philiq)
    np.testing.assert_allclose(p * phivap, 0.98469390 * 1e5, 1e-3)
    np.testing.assert_allclose(p * philiq, 8.55359508 * 1e5, 1e-3)

    eq = VLE([methane, methane], eosname)
    y = [0.3, 0.7]
    z = eq.getZfromPT(p, t, y)
    zmax, zmin = np.max(z), np.min(z)
    np.testing.assert_allclose(0.9845, zmax, 1e-2)
    np.testing.assert_allclose(0.003341, zmin, 1e-2)


# def test_flash_three_subs():
#     eq = VLE([pentane, hexane, heptane], eosname)
#     z = [0.2, 0.3, 0.5]
#     p = 1e5
#     t = 315
#
#     x, y, v = eq.getFlash(z, p, t)
#     print(v)
#     print(y)
#     print(x)
#     # assert 0


def test_bubblepoint_pressure_validate_from_youtube():
    # https://www.youtube.com/watch?v=0QFLng0fz68
    eq = VLE([pentane, hexane, heptane], eosname)
    x = [0.2, 0.3, 0.5]
    t = 315

    y, pb, pv, pl, k, ite = eq.getBubblePointPressure(x, t)
    ymin, ymax = np.min(y), np.max(y)
    ymed = 1.0 - ymin - ymax
    print(pb)

    assert abs(np.sum(y) - 1) < 1e-8
    np.testing.assert_allclose(pb, 0.043e6, 1e-2)
    np.testing.assert_allclose(ymin, 0.163, 1e-2)
    np.testing.assert_allclose(ymax, 0.559, 1e-2)
    np.testing.assert_allclose(ymed, 0.28, 1e-2)


def test_dewpoint_pressure_validate_from_youtube():
    # https://www.youtube.com/watch?v=0QFLng0fz68
    eq = VLE([pentane, hexane, heptane], eosname)
    y = [0.55543853, 0.28222737, 0.1623341]
    t = 315

    x, pd, pv, pl, k, ite = eq.getDewPointPressure(y, t)
    xmin, xmax = np.min(x), np.max(x)
    xmed = 1.0 - xmin - xmax
    print(pd)

    assert abs(np.sum(x) - 1) < 1e-8
    np.testing.assert_allclose(pd, 0.043e6, 1e-2)
    np.testing.assert_allclose(xmin, 0.2, 1e-3)
    np.testing.assert_allclose(xmax, 0.5, 1e-3)
    np.testing.assert_allclose(xmed, 0.3, 1e-3)


def test_bubblepoint_temperature_validate_from_youtube():
    # https://www.youtube.com/watch?v=0QFLng0fz68
    eq = VLE([pentane, hexane, heptane], eosname)
    x = [0.2, 0.3, 0.5]
    p = 42803.8018747439

    y, tb, pv, pl, k, ite = eq.getBubblePointTemperature(x, p)
    ymin, ymax = np.min(y), np.max(y)
    ymed = 1.0 - ymin - ymax
    print(tb)

    assert abs(np.sum(y) - 1) < 1e-8
    np.testing.assert_allclose(tb, 315, 1e-3)
    np.testing.assert_allclose(ymin, 0.163, 1e-2)
    np.testing.assert_allclose(ymax, 0.559, 1e-2)
    np.testing.assert_allclose(ymed, 0.28, 1e-2)


def test_dewpoint_temperature_validate_from_youtube():
    # https://www.youtube.com/watch?v=0QFLng0fz68
    eq = VLE([pentane, hexane, heptane], eosname)
    y = [0.55543853, 0.28222737, 0.1623341]
    p = 42803.8018747439

    x, td, pv, pl, k, ite = eq.getDewPointTemperature(y, p)
    xmin, xmax = np.min(x), np.max(x)
    xmed = 1.0 - xmin - xmax

    # TODO check
    print(x)
    print(ite)
    assert abs(np.sum(x) - 1) < 1e-8
    np.testing.assert_allclose(td, 315, 1e-3)
    np.testing.assert_allclose(xmin, 0.2, 1e-4)
    np.testing.assert_allclose(xmax, 0.5, 1e-4)
    np.testing.assert_allclose(xmed, 0.3, 1e-4)


def test_flash_temperature_validate_from_youtube():
    # https://www.youtube.com/watch?v=0QFLng0fz68
    eq = VLE([pentane, hexane, heptane], eosname)
    z = [0.5, 0.3, 0.2]
    t = 315
    p = 42803.8018747439
    ret = eq.getFlash(z, p, t)
