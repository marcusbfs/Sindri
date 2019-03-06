from TPCAE.compounds import SubstanceProp, MixtureProp
import numpy as np


def test_creation_substance():
    methane = SubstanceProp("methane", "CH4")
    np.testing.assert_allclose(methane.Tc, 190.56, 1e-3)


def test_creation_mixture():
    m = SubstanceProp("methane", "CH4")
    mix = MixtureProp([m, m], [0.5, 0.5])


def test_hasCp_but_only_a0():
    ar = SubstanceProp("argon", "Ar")
    assert ar.hasCp()
    np.testing.assert_allclose(ar.a0, 2.5, 1e-3)
    np.testing.assert_allclose(ar.a1, 0, 1e-3)


def test_get_each_prop():
    ig = SubstanceProp("methane", "CH4")
    assert ig.hasCp()
    Tref, T, Pref, P = 300, 150, 1e5, 1e5
    np.testing.assert_allclose(32.669700, ig.getCp(T), 1e-3)
    np.testing.assert_allclose(-5060.944, ig.getH(Tref, T), 1e-3)
    np.testing.assert_allclose(-23.263196, ig.getS(Tref, T, Pref, P), 1e-3)
    np.testing.assert_allclose(-1571.465529, ig.getG(Tref, T, Pref, P), 1e-3)
    np.testing.assert_allclose(-3813.775611, ig.getU(Tref, T), 1e-3)
    np.testing.assert_allclose(-324.296203, ig.getA(Tref, T, Pref, P), 1e-3)


def test_get_each_prop_from_getIGprops():
    ig = SubstanceProp("methane", "CH4")
    assert ig.hasCp()
    Tref, T, Pref, P = 300, 150, 1e5, 1e5
    props = ig.getIGProps(Tref, T, Pref, P)
    np.testing.assert_allclose(32.669700, props.Cp, 1e-3)
    np.testing.assert_allclose(-5060.944937, props.H, 1e-3)
    np.testing.assert_allclose(-23.263196, props.S, 1e-3)
    np.testing.assert_allclose(-1571.465529, props.G, 1e-3)
    np.testing.assert_allclose(-3813.775611, props.U, 1e-3)
    np.testing.assert_allclose(-324.296203, props.A, 1e-3)


def test_each_Pvp():
    ig = SubstanceProp("methane", "CH4")
    Tref, T, Pref, P = 300, 150, 1e5, 1e5
    Pvp = 10.268
    assert ig.hasAntoine()
    np.testing.assert_allclose(Pvp, ig.getPvpAntoine(T) * 1e-5, 1e-3)
    np.testing.assert_allclose(Pvp, ig.getPvpAW(T) * 1e-5, 1e-1)
    np.testing.assert_allclose(Pvp, ig.getPvpLK(T) * 1e-5, 1e-1)


def test_getPvps():
    ig = SubstanceProp("methane", "CH4")
    Tref, T, Pref, P = 300, 150, 1e5, 1e5
    Pvps = ig.getPvps(T)
    Pvp = 10.268
    np.testing.assert_allclose(Pvp, Pvps.Antoine * 1e-5, 1e-3)
    np.testing.assert_allclose(Pvp, Pvps.AW * 1e-5, 1e-1)
    np.testing.assert_allclose(Pvp, Pvps.LK * 1e-5, 1e-1)


def test_mixture_same_compound():
    ig = SubstanceProp("methane", "CH4")
    mix = MixtureProp([ig, ig], [0.3, 0.7])
    Tref, T, Pref, P = 300, 150, 1e5, 1e5
    assert mix.hasCp()
    np.testing.assert_allclose(32.6697, mix.getCp(T), 1e-3)


def test_get_each_prop_for_mixture():
    ig = SubstanceProp("methane", "CH4")
    mix = MixtureProp([ig, ig], [0.3, 0.7])
    assert mix.hasCp()
    assert mix.checkCpRange(150)
    Tref, T, Pref, P = 300, 150, 1e5, 1e5
    np.testing.assert_allclose(32.669700, mix.getCp(T), 1e-3)
    np.testing.assert_allclose(-5060.944, mix.getH(Tref, T), 1e-3)
    np.testing.assert_allclose(-3813.775611, mix.getU(Tref, T), 1e-3)
    np.testing.assert_allclose(-18.1842, mix.getS(Tref, T, Pref, P), 1e-3)
    np.testing.assert_allclose(-2333.316749, mix.getG(Tref, T, Pref, P), 1e-3)
    np.testing.assert_allclose(-1086.147423, mix.getA(Tref, T, Pref, P), 1e-3)


def test_MixOfOne_get_each_prop_from_getIGprops():
    igtmp = SubstanceProp("methane", "CH4")
    ig = MixtureProp([igtmp], [1.0])
    Tref, T, Pref, P = 300, 150, 1e5, 1e5
    props = ig.getIGProps(Tref, T, Pref, P)
    np.testing.assert_allclose(32.669700, props.Cp, 1e-3)
    np.testing.assert_allclose(-5060.944937, props.H, 1e-3)
    np.testing.assert_allclose(-23.263196, props.S, 1e-3)
    np.testing.assert_allclose(-1571.465529, props.G, 1e-3)
    np.testing.assert_allclose(-3813.775611, props.U, 1e-3)
    np.testing.assert_allclose(-324.296203, props.A, 1e-3)


def test_getMolWt():
    one = SubstanceProp("methane", "CH4")
    np.testing.assert_allclose(16.043, one.MolWt, 1e-3)
    two = MixtureProp([one, one], [0.3, 0.7])
    mw = two.getMolWt()
    np.testing.assert_allclose(mw, 16.043, 1e-3)
