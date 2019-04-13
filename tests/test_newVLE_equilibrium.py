import numpy as np

from Sindri.VLE import *
from Sindri.compounds import SubstanceProp
from Sindri.Factories.EOSMixFactory import createEOSMix

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


def test_bubblePoint():

    subs = [hexane, cyclopentane]
    vleEq = VLE(subs, eosname)
    eq = createEOSMix(subs, eosname)

    t = 300
    p = 35640.78
    x = [0.5, 0.5]

    # pressure
    y_e, pb_e, phivap, philiq, k, ite = vleEq.getBubblePointPressure(x, t)
    y_c, pb_c, phivap, philiq, k, ite = eq.getBubblePointPressure(x, t)
    np.testing.assert_allclose(pb_e, pb_c, 1e-2)

    # temperature
    y_e, tb_e, phivap, philiq, k, ite = vleEq.getBubblePointTemperature(x, p)
    y_c, tb_c, phivap, philiq, k, ite = eq.getBubblePointTemperature(x, p)
    np.testing.assert_allclose(tb_e, tb_c, 1e-2)
