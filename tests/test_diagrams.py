import pytest

from TPCAE.diagrams import *
from TPCAE.PureSubstance import PureSubstance

c = PureSubstance("Methane", "CH4", "peng_and_robinson_1976")
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


def test_gen_data():

    c = PureSubstance("Water", "H2O", "peng_and_robinson_1976")
    points = 30
    Tfp = c.compound["Tfp_K"]
    # Tfp = 550
    Tc = c.compound["Tc_K"]
    gen_data(c, [Tfp, Tc], Pref, Tref, points)


def test_gen_data_with_isotherms():

    c = PureSubstance("Methane", "CH4", "peng_and_robinson_1976")
    points = 50
    Tfp = c.compound["Tfp_K"]
    Tc = c.compound["Tc_K"]
    a = gen_data(c, [Tfp, Tc], Pref, Tref, points, isotherms=[120, 150, 190])
    # plot_diag(a,"PV","m3/mol","bar", xlnscale=True, ylnscale=True)
