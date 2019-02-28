from TPCAE.mixtures import *
from TPCAE.eos import *
from TPCAE.db_utils import get_compound_properties

pentane = get_compound_properties("pentane", "C5H12")
hexane = get_compound_properties("hexane", "C6H14")

mix = [pentane, hexane]
y = [0.5, 0.5]
k = [[0.0, 0.01], [0.01, 0.0]]
# k = [[0.01, .0],
#      [.0,0.01]]
eos = "peng_and_robinson_1976"

m = Mixture(mix, y, k, eos)

methane = get_compound_properties("methane", "CH4")
puremix = Mixture([methane], [1], [[0]], eos)


def test_return_delta_prop():
    ret = m.return_delta_prop(1e5, 150, 1e5, 100)
    print(ret)
    # assert 0


def test_check_Z_return_mixture_one_compound_PR():
    z = puremix.return_Z_given_PT(1e5, 129)
    ret_zmax = np.max(z)
    ret_zmin = np.min(z)
    exp_zmax = 0.977305
    exp_zmin = 3.394805e-03
    np.testing.assert_allclose(ret_zmax, exp_zmax, 1e-5)
    np.testing.assert_allclose(ret_zmin, exp_zmin, 1e-5)


def test_check_IGdelta_mixture_one_compound():
    cp, h, s, g, u, a, msgs = puremix.return_delta_IG(1e5, 150, 1e5, 300)
    np.testing.assert_allclose(cp, 32.669700, 1e-5)
    np.testing.assert_allclose(h, -5060.944937, 1e-5)
    np.testing.assert_allclose(s, -23.263196, 1e-5)
    np.testing.assert_allclose(g, -1571.465529, 1e-5)
    np.testing.assert_allclose(u, -3813.775611, 1e-5)
    np.testing.assert_allclose(a, -324.296203, 1e-5)


def test_check_delta_mixProp_one_compound():
    ideal_ret, liq_ret, vap_ret, log, supercritical = puremix.return_delta_mixProp(
        1e5, 150, 1e5, 300
    )
    print(ideal_ret)
    print(liq_ret)
    print(vap_ret)
    print(log)
    assert 0
