from TPCAE.VLE import *

from TPCAE.compounds import MixtureProp, SubstanceProp
import numpy as np

methane = SubstanceProp("methane", "CH4")
ethane = SubstanceProp("ethane", "C2H4")
water = SubstanceProp("water", "H2O")
heptane = SubstanceProp("heptane", "C7H16")
pentane = SubstanceProp("pentane", "C5H12")
hexane = SubstanceProp("hexane", "C6H14")

eosname = "Peng and Robinson (1976)"
k2 = [[0, 0], [0, 0]]

def test_inconsistency():
    k = [[0, 0], [0, 0]]
    eosname = "Peng and Robinson (1976)"
    eq = VLE([pentane, hexane], eosname)
    x = [0.01, .99]
    t = 298.7

    y, p, i = eq.getBubblePointPressure(x, t)
    print(y)
    print(p)
    assert 0

def test_pr1976():
    eq = VLE([methane], eosname)
    p = 1e5
    t = 150
    y = [1]

    z = eq.getZ(p, t, y)
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
    z = eq.getZ(p, t, y)
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

    y, pb, ite = eq.getBubblePointPressure(x, t)
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

    x, pd, ite = eq.getDewPointPressure(y, t)
    xmin, xmax = np.min(x), np.max(x)
    xmed = 1.0 - xmin - xmax
    print(pd)

    assert abs(np.sum(x) - 1) < 1e-8
    np.testing.assert_allclose(pd, 0.043e6, 1e-2)
    np.testing.assert_allclose(xmin, 0.2, 1e-8)
    np.testing.assert_allclose(xmax, 0.5, 1e-8)
    np.testing.assert_allclose(xmed, 0.3, 1e-8)


def test_bubblepoint_temperature_validate_from_youtube():
    # https://www.youtube.com/watch?v=0QFLng0fz68
    eq = VLE([pentane, hexane, heptane], eosname)
    x = [0.2, 0.3, 0.5]
    p = 42803.8018747439

    y, tb, ite = eq.getBubblePointTemperature(x, p)
    ymin, ymax = np.min(y), np.max(y)
    ymed = 1.0 - ymin - ymax
    print(tb)

    assert abs(np.sum(y) - 1) < 1e-8
    np.testing.assert_allclose(tb, 315, 1e-8)
    np.testing.assert_allclose(ymin, 0.163, 1e-2)
    np.testing.assert_allclose(ymax, 0.559, 1e-2)
    np.testing.assert_allclose(ymed, 0.28, 1e-2)


def test_dewpoint_temperature_validate_from_youtube():
    # https://www.youtube.com/watch?v=0QFLng0fz68
    eq = VLE([pentane, hexane, heptane], eosname)
    y = [0.55543853, 0.28222737, 0.1623341]
    p = 42803.8018747439

    x, td, ite = eq.getDewPointTemperature(y, p)
    xmin, xmax = np.min(x), np.max(x)
    xmed = 1.0 - xmin - xmax
    print(td)

    assert abs(np.sum(x) - 1) < 1e-8
    np.testing.assert_allclose(td, 315, 1e-8)
    np.testing.assert_allclose(xmin, 0.2, 1e-8)
    np.testing.assert_allclose(xmax, 0.5, 1e-8)
    np.testing.assert_allclose(xmed, 0.3, 1e-8)

def test_flash_temperature_validate_from_youtube():
    # https://www.youtube.com/watch?v=0QFLng0fz68
    eq = VLE([pentane, hexane, heptane], eosname)
    z = [.5, .3, .2]
    t = 315
    p = 42803.8018747439
    ret = eq.getFlash(z, p, t)
