import pytest
from TPCAE.diagrams import plot_diagram
from TPCAE.eos import EOS

c = EOS("Methane", "CH4", "peng_and_robinson_1976")
points = 50
Tfp = c.compound["Tfp_K"]
Tc = c.compound["Tc_K"]


def test_plot_diagram_paramaters():
    with pytest.raises(
        TypeError, match="Temperature parameter must be an array of len 2"
    ):
        plot_diagram(c, 300, 1, 1, points)

    with pytest.raises(
        TypeError, match="Temperature parameter must be an array of len 2"
    ):
        plot_diagram(c, [1], 1, 1, points)

    with pytest.raises(
        TypeError, match="Temperature parameter must be an array of len 2"
    ):
        plot_diagram(c, (1), 1, 1, points)

    # with pytest.raises(TypeError, match="Compound parameter must be a EOS object"):
    #     plot_diagram(1, (1,1), 1, 1, points)


def test_plot_diagram_values():
    c = EOS("Water", "H2O", "peng_and_robinson_1976")
    points = 500
    Tfp = c.compound["Tfp_K"]
    Tfp = 550
    Tc = c.compound["Tc_K"]
    # plot_diagram(c, [Tfp, Tc], "m3/mol","Pa", points)
