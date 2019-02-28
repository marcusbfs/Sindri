from TPCAE.IdealGasPropMixtures import *

from tests.db_compound import methane
from TPCAE.units import conv_unit

a0 = methane["a0"]
a1 = methane["a1"]
a2 = methane["a2"]
a3 = methane["a3"]
a4 = methane["a4"]

T1 = 100
T2 = 150
Tref = 300
Pref = 1
P1 = conv_unit(1, "bar", "Pa")
P2 = conv_unit(1, "bar", "Pa")

ys = np.asarray([0.3, 0.7])
a0s = np.asarray([a0, a0])
a1s = np.asarray([a1, a1])
a2s = np.asarray([a2, a2])
a3s = np.asarray([a3, a3])
a4s = np.asarray([a4, a4])
Tmins = np.asarray([100, 100])
Tmaxs = np.asarray([1000, 1000])


def test_cpmixture():

    a = return_MixCp_IG(100, ys, a0s, a1s, a2s, a3s, a4s, Tmins, Tmaxs)
    np.testing.assert_allclose(33.263012, a[0], 1e-5)


def test_mixtureH_IG():

    a = return_MixH_IG(100, 150, ys, a0s, a1s, a2s, a3s, a4s)
    np.testing.assert_allclose(1644.062738, a, 1e-5)
    b = return_MixU_IG(a, ys, 100, 150)
    np.testing.assert_allclose(1228.3396295851028, b, 1e-5)


def test_mixtureS_IG():

    a = return_MixS_IG(100, 150, 1e5, 1e6, ys, a0s, a1s, a2s, a3s, a4s)
    np.testing.assert_allclose(-0.725293, a, 1e-5)


def test_mixtureG_IG():
    h = return_MixH_IG(100, 150, ys, a0s, a1s, a2s, a3s, a4s)
    s = return_MixS_IG(100, 150, 1e5, 1e6, ys, a0s, a1s, a2s, a3s, a4s)
    g = return_MixG_IG(h, T2, s)
    np.testing.assert_allclose(g, 1752.8567029319283, 1e-5)
