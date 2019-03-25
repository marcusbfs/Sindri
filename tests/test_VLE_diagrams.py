from TPCAE.VLE import *
import numpy as np

from TPCAE.compounds import MixtureProp, SubstanceProp

methane = SubstanceProp("methane", "CH4")
ethane = SubstanceProp("ethane", "C2H4")
water = SubstanceProp("water", "H2O")
heptane = SubstanceProp("heptane", "C7H16")
pentane = SubstanceProp("pentane", "C5H12")
hexane = SubstanceProp("hexane", "C6H14")



def test_isobaricPlot():


    k = [[0, 0], [0, 0]]
    eosname = "Peng and Robinson (1976)"
    eq = VLE([pentane, heptane], eosname)
    p = 1e5

    eq.isobaricBinaryMixturePlot(p, Tunit="ºC", Punit="bar")

def test_isothermalPlot():


    k = [[0, 0], [0, 0]]
    eosname = "Peng and Robinson (1976)"
    eq = VLE([pentane, hexane], eosname)
    t = 298.7

    eq.isothermalBinaryMixturePlot(t, Tunit="ºC", Punit="bar")
