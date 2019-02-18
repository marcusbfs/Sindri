from TPCAE.eos import EOS
from tests.db_compound import methane
from pytest import approx

eos_name = "peng_and_robinson_1976"
m = EOS(methane["Name"], methane["Formula"], eos_name)


def test_eos_class_initialization_and_compound_set():
    assert methane == m.compound


def test_return_Z_given_P_T_using_peng_robinson():
    # calculated using http://people.ds.cam.ac.uk/pjb10/thermo/pure.html
    z = min(m.return_Z_given_PT(1e5, 100))  # 1 bar, 100 K (liquid methane)
    assert approx(z, 1e-4) == 0.003899


def test_change_eos_Z_given_PT_using_soave_1972():
    # calculated using http://people.ds.cam.ac.uk/pjb10/thermo/pure.html
    m.change_eos('soave_1972')
    z = min(m.return_Z_given_PT(1e5, 100))  # 1 bar, 100 k (liquid methane)
    assert approx(z, 1e-4) == 0.004393


def test_return_V_given_PT_using_soave_1972():
    # calculated using http://people.ds.cam.ac.uk/pjb10/thermo/pure.html
    m.change_eos('soave_1972')
    v = min(m.return_V_given_PT(1e5, 100))  # 1 bar, 100 k (liquid methane)
    assert approx(v, 1e-3) == 0.00003653


def test_return_PvpEOS_given_PT_using_peng_and_robinson_1976():
    m.change_eos('peng_and_robinson_1976')
    Pvpret = m.return_Pvp_EOS(100, .3 * 1e5, tol=1e-8)
    Pvp = Pvpret.Pvp * 1e-5
    assert approx(Pvp, 1e-3) == 0.3482


def test_return_PvpEOS_maxiterations_given_PT_using_peng_and_robinson_1976():
    m.change_eos('peng_and_robinson_1976')
    _k = 2
    Pvpret = m.return_Pvp_EOS(100, .3 * 1e5, tol=1e-8, k=_k)
    assert Pvpret.iter == _k
    _k = 3
    Pvpret = m.return_Pvp_EOS(100, .3 * 1e5, tol=1e-8, k=_k)
    assert Pvpret.iter == _k


# TODO verify if returns dict correct keys


def test_return_deltaH_using_peng_and_robinson_1976():
    import TPCAE.IdealGasPropertiesPureSubstance as IGPROP
    # compared to http://courses.me.metu.edu.tr/courses/me351/Methane%20tables%20for%20Q1-a.pdf
    m.change_eos('peng_and_robinson_1976')
    Tref = 125  # K
    Pref = 100e3  # Pa
    Zref = max(m.return_Z_given_PT(Pref, Tref))  # vapor state
    Vref = max(m.return_V_given_PT(Pref, Tref))  # vapor state

    T1 = 150  # K
    P1 = 100e3  # Pa
    Z1 = max(m.return_Z_given_PT(P1, T1))  # vapor state
    V1 = max(m.return_V_given_PT(P1, T1))  # vapor state

    T2 = 225  # K
    P2 = 100e3  # Pa
    Z2 = max(m.return_Z_given_PT(P2, T2))  # vapor state
    V2 = max(m.return_V_given_PT(P2, T2))  # vapor state

    dH_IG1 = IGPROP.return_deltaH_IG(Tref, T1, methane["a0"], methane["a1"], methane["a2"], methane["a3"],
                                     methane["a4"])
    dHR1 = m.return_delta_ResProperties(Pref, Tref, Vref, Zref, P1, T1, V1, Z1)["HR"]

    dH_IG2 = IGPROP.return_deltaH_IG(Tref, T2, methane["a0"], methane["a1"], methane["a2"], methane["a3"],
                                     methane["a4"])
    dHR2 = m.return_delta_ResProperties(Pref, Tref, Vref, Zref, P2, T2, V2, Z2)["HR"]

    state1 = dH_IG1 - dHR1
    state2 = dH_IG2 - dHR2

    delta_state = (state2 - state1) / methane["Mol. Wt."]

    table_val = 464.99 - 306.77
    print(delta_state, table_val)

    assert approx(delta_state, 10) == table_val
