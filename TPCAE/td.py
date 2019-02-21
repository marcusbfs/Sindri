import pytest

from diagrams import *
from eos import EOS

c = EOS("Methane", "CH4", "peng_and_robinson_1976")
points = 50
Tfp = c.compound["Tfp_K"]
Tc = c.compound["Tc_K"]
Tref = 150
Pref = 1e5


def test_plot_diagram_paramaters():
    with pytest.raises(
        TypeError, match="Temperature parameter must be an array of len 2"
    ):
        gen_data(c, 300, 1, 1, points)

    with pytest.raises(
        TypeError, match="Temperature parameter must be an array of len 2"
    ):
        gen_data(c, [1], 1, 1, points)

    with pytest.raises(
        TypeError, match="Temperature parameter must be an array of len 2"
    ):
        gen_data(c, (1), 1, 1, points)

    # with pytest.raises(TypeError, match="Compound parameter must be a EOS object"):
    #     plot_diagram(1, (1,1), 1, 1, points)
#
#
def test_gen_data():
    from time import time
    c = EOS("Water", "H2O", "peng_and_robinson_1976")
    points = 30
    Tfp = c.compound["Tfp_K"]
     # Tfp = 550
    Tc = c.compound["Tc_K"]
    s1 = time()
    gen_data(c, [Tfp, Tc],Pref, Tref ,points)
    s2 = time()
    print("{0:.4f} sec".format(s2-s1))
    # assert 0



test_gen_data()