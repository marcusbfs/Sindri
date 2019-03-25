from TPCAE.VLE import *

from TPCAE.compounds import MixtureProp, SubstanceProp
import numpy as np

methane = SubstanceProp("methane", "CH4")
ethane = SubstanceProp("ethane", "C2H4")
water = SubstanceProp("water", "H2O")
heptane = SubstanceProp("heptane", "C7H16")
pentane = SubstanceProp("pentane", "C5H12")
hexane = SubstanceProp("hexane", "C6H14")



def test_peneloux1982():

    eosname = "Péneloux, et al. (1982)"
    eq = VLE([methane, methane], eosname)

    p = 1e5
    t = 300
    y = [.5, .5]
    i = 0

    z = eq.getZ(p, t, y)
    phi = eq.getPhi_i(i, y, p, t, np.min(z))
    print(phi)
    assert 0

def test_PR1976():

    eosname = "Peng and Robinson (1976)"
    eq = VLE([methane, methane], eosname)

    p = 1e5
    t = 300
    y = [.5, .5]
    i = 0

    z = eq.getZ(p, t, y)
    phi = eq.getPhi_i(i, y, p, t, np.min(z))
    print(phi)
    assert 0
