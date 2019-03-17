import numpy as np

from TPCAE.compounds import MixtureProp, SubstanceProp
from TPCAE.eos import EOS

methane = SubstanceProp("methane", "CH4")
water = SubstanceProp("ethane", "C2H4")
eosname = "Peng and Robinson (1976)"
k2 = [[0,0], [0,0]]


def test_interface():
    mix = MixtureProp([methane, water], [.3, .7])
    eoseq = EOS(mix, k2, eosname)
    eoseq.getPhi_i(0, 1e5, 300, 4e-3, .98)



def test_initial_bubble_pressure_guess():
    mix = MixtureProp([methane, water], [.3, .7])
    eoseq = EOS(mix, k2, eosname)
    x = [.2, .8]
    t = 300
    pb = eoseq._getPb_initial_guess(t, x)
    print(pb)
    assert 0


def test_getbubblepointpressure():
    mix = MixtureProp([methane, water], [.3, .7])
    eoseq = EOS(mix, k2, eosname)
    x = [.2, .8]
    t = 300
    eoseq.getBubblePointPressure(t, x)
    assert 0
