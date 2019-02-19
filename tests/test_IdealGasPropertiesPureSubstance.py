from TPCAE.IdealGasPropertiesPureSubstance import (
    return_fluidState,
    return_Cp,
    return_deltaH_IG,
    return_deltaS_IG,
    return_deltaA_IG,
    return_deltaG_IG,
    return_deltaU_IG,
    abs_rel_err,
)
from pytest import approx
from tests.db_compound import methane

a0 = methane["a0"]
a1 = methane["a1"]
a2 = methane["a2"]
a3 = methane["a3"]
a4 = methane["a4"]


def test_return_fluidState_verified_from_internet_values():
    state = return_fluidState(
        1.0, methane["Pc_bar"], 298.15, methane["Tc_K"], 10.1, delta=1e-8
    )
    assert state == "superheated steam"


def test_return_Cp_validation_with_methane():
    cp = return_Cp(
        298.16,
        methane["a0"],
        methane["a1"],
        methane["a2"],
        methane["a3"],
        methane["a4"],
        methane["Tcpmin_K"],
        methane["Tcpmax_K"],
    )
    assert approx(cp.Cp, 1e-5) == 35.7780112


def test_return_deltaH_IG():
    dH_IG = return_deltaH_IG(300, 340, a0, a1, a2, a3, a4)
    assert approx(dH_IG, 1e-5) == 1467.8392


def test_return_deltaS_IG():
    dS_IG = return_deltaS_IG(300, 340, 1, 2, a0, a1, a2, a3, a4)
    assert approx(dS_IG, 1e-5) == -1.1724269


def test_return_deltaG_IG():
    dH_IG = return_deltaH_IG(300, 340, a0, a1, a2, a3, a4)
    dS_IG = return_deltaS_IG(300, 340, 1, 2, a0, a1, a2, a3, a4)
    dG_IG = return_deltaG_IG(dH_IG, 340, dS_IG)
    print(dG_IG)
    assert approx(dG_IG, 1e-5) == 1866.4644


def test_return_deltaU_IG():
    dH_IG = return_deltaH_IG(300, 340, a0, a1, a2, a3, a4)
    dS_IG = return_deltaS_IG(300, 340, 1, 2, a0, a1, a2, a3, a4)
    dG_IG = return_deltaG_IG(dH_IG, 340, dS_IG)
    dU_IG = return_deltaU_IG(dG_IG, 340, dS_IG)
    print(dU_IG)
    assert approx(dU_IG, 1e-5) == 1467.8392601


def test_return_deltaA_IG():
    dH_IG = return_deltaH_IG(300, 340, a0, a1, a2, a3, a4)
    dS_IG = return_deltaS_IG(300, 340, 1, 2, a0, a1, a2, a3, a4)
    dG_IG = return_deltaG_IG(dH_IG, 340, dS_IG)
    dU_IG = return_deltaU_IG(dG_IG, 340, dS_IG)
    dA_IG = return_deltaA_IG(dU_IG, 340, dS_IG)
    print(dA_IG)
    assert approx(dA_IG, 1e-5) == 1866.46441


def test_abs_err_zero_value():
    x = abs_rel_err(0, 1)
    assert approx(x, 1e-5) == 1


def test_abs_err():
    x = abs_rel_err(0.5, 0.7)
    assert approx(x, 1e-5) == 0.4
