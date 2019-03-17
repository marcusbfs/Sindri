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


def test_pr1976_get_pb_guess():
    eq = VLE([methane, water], eosname)
    x = [0.2, 0.8]
    p = 1e5
    t = 300

    pb = eq._getPb_guess(x, t)
    print(pb)


def test_bubble_point_pressure():
    eq = VLE([methane, ethane], eosname)
    x = [0.3, 0.7]
    p = 1e5
    t = 300

    pb, y, k = eq.getBubblePointPressure(x, t)
    print(pb)
    print(y)
    print(k)
    # assert 0


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

def test_bubblepoint2():
    # https://www.youtube.com/watch?v=0QFLng0fz68
    eq = VLE([pentane, hexane, heptane], eosname)
    x = [0.2, 0.3, 0.5]
    t = 315

    y, pb, ite = eq.getBubblePointPressure(x, t)
    ymin ,ymax = np.min(y), np.max(y)
    ymed = 1.0 - ymin - ymax
    np.testing.assert_allclose(pb, .043e6, 1e-2)
    np.testing.assert_allclose(ymin, .163, 1e-2)
    np.testing.assert_allclose(ymax, .559, 1e-2)
    np.testing.assert_allclose(ymed, .28, 1e-2)

