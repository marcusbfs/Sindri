import numpy as np

from Sindri.compounds import MixtureProp, SubstanceProp
from Sindri.eos import EOS

methane = SubstanceProp("methane", "CH4")
water = SubstanceProp("water", "H2O")


def test_vanderwalls_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "van der Waals (1890)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 0.005463
    zvap_expected = 0.9885
    vliq_expected = 0.00006813
    vvap_expected = 0.01233

    np.testing.assert_allclose(zliq_expected, zliq, 1e-2)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-2)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-2)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-2)


def test_redlich_and_kwong_1949_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Redlich and Kwong (1949)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.759408e-03
    zvap_expected = 0.985316
    vliq_expected = 4.688618e-05
    vvap_expected = 0.012289

    np.testing.assert_allclose(zliq_expected, zliq, 1e-3)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-3)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-3)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-3)


def test_wilson_1964_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Wilson (1964)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.765280e-03
    zvap_expected = 0.985347
    vliq_expected = 4.695941e-05
    vvap_expected = 0.012289

    np.testing.assert_allclose(zliq_expected, zliq, 1e-3)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-3)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-3)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-3)


def test_soave_1972_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Soave (1972)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.794867e-03
    zvap_expected = 0.985498
    vliq_expected = 4.732842e-05
    vvap_expected = 0.012291

    np.testing.assert_allclose(zliq_expected, zliq, 1e-3)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-3)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-3)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-3)


def test_peneloux_et_al_1982_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Péneloux, et al. (1982)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.710726e-03
    zvap_expected = 0.985443
    vliq_expected = 4.627903e-05
    vvap_expected = 0.012290

    np.testing.assert_allclose(zliq_expected, zliq, 1e-3)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-3)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-3)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-3)


def test_patel_and_teja_1982_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Patel and Teja (1982)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.710877e-03
    zvap_expected = 0.985335
    vliq_expected = 4.628092e-05
    vvap_expected = 0.012289

    np.testing.assert_allclose(zliq_expected, zliq, 1e-3)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-3)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-3)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-3)


def test_adachi_et_al_1983_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Adachi, et al. (1983)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.716104e-03
    zvap_expected = 0.985009
    vliq_expected = 4.634611e-05
    vvap_expected = 0.012285

    np.testing.assert_allclose(zliq_expected, zliq, 1e-3)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-3)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-3)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-3)


def test_soave_1984_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Soave (1984)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.745608e-03
    zvap_expected = 0.985554
    vliq_expected = 4.671407e-05
    vvap_expected = 0.012292

    np.testing.assert_allclose(zliq_expected, zliq, 1e-3)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-3)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-3)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-3)


def test_adachi_et_al_1985_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Adachi, et al. (1985)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.751563e-03
    zvap_expected = 0.985276
    vliq_expected = 4.678834e-05
    vvap_expected = 0.012288

    np.testing.assert_allclose(zliq_expected, zliq, 1e-3)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-3)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-3)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-3)


def test_twu_et_al_1995_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Twu, et al. (1995)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.340153e-03
    zvap_expected = 0.984468
    vliq_expected = 4.165737e-05
    vvap_expected = 0.012278

    np.testing.assert_allclose(zliq_expected, zliq, 1e-3)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-3)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-3)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-3)


def test_ahlers_gmehling_2001_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Ahlers-Gmehling (2001)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.246340e-03
    zvap_expected = 0.984434
    vliq_expected = 4.048736e-05
    vvap_expected = 0.012278

    np.testing.assert_allclose(zliq_expected, zliq, 1e-1)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-1)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-1)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-1)


def test_gasem_et_al_pr_2001_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Gasem, et al. PR modification (2001)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.337294e-03
    zvap_expected = 0.984450
    vliq_expected = 4.162171e-05
    vvap_expected = 0.012278

    np.testing.assert_allclose(zliq_expected, zliq, 1e-3)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-3)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-3)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-3)


def test_gasem_et_al_twu_2001_z_and_v():
    k = [[0, 0], [0, 0]]
    sglmethae = MixtureProp([methane, methane], [0.3, 0.7])
    eosname = "Gasem, et al. Twu modificaton (2001)"
    eos = EOS(sglmethae, k, eosname)

    T, P = 150, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    zliq_expected = 3.342205e-03
    zvap_expected = 0.984478
    vliq_expected = 4.168295e-05
    vvap_expected = 0.012278

    np.testing.assert_allclose(zliq_expected, zliq, 1e-3)
    np.testing.assert_allclose(zvap_expected, zvap, 1e-3)
    np.testing.assert_allclose(vliq_expected, vliq, 1e-3)
    np.testing.assert_allclose(vvap_expected, vvap, 1e-3)
