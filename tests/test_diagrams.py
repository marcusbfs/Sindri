from Sindri.compounds import MixtureProp, SubstanceProp
from Sindri.diagrams import *
from Sindri.eos import EOS

methane = SubstanceProp("methane", "CH4")
water = SubstanceProp("water", "H2O")

dblmethae = MixtureProp([methane, methane], [0.3, 0.7])
sglmethae = MixtureProp([methane], [1.0])


def test_gen_data_and_plot():
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
    eosname = "Peng and Robinson (1976)"
    eos = EOS(sglmethae, k, eosname)

    ti_f = [methane.Tfp, methane.Tc]
    Pref = 1e5
    Tref = 300
    points = 30
    gen_data_results = gen_data(eos, ti_f, Pref, Tref, points)
    rl, rv, cp, pv_isotherms = list(gen_data_results)
    # diagrams = PlotPureSubstanceDiagrams(
    #     rl, rv, cp, methane.Name, eos.getEOSDisplayName()
    # )
    # diagrams.plotPS("J/molK", "Pa")
    # diagrams._plot()
