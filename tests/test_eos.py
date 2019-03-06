from TPCAE.compounds import MixtureProp, SubstanceProp
from TPCAE.eos import EOS
import numpy as np
from TPCAE.Properties import DeltaProp

methane = SubstanceProp("methane", "CH4")
water = SubstanceProp("water", "H2O")

dblmethae = MixtureProp([methane, methane], [0.3, 0.7])
sglmethae = MixtureProp([methane], [1.0])


def test_class_constructor():
    k = [[0, 0], [0, 0]]
    eosname = "Peng and Robinson (1976)"
    eos = EOS(dblmethae, k, eosname)


def test_Props_for_single_compound_peng_and_robinson():
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
    eosname = "Peng and Robinson (1976)"
    eos = EOS(sglmethae, k, eosname)
    P, T = 1e5, 150
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zmin, zmax = np.min(zs), np.max(zs)
    vmin, vmax = np.min(vs), np.max(vs)
    PvpAW = eos.mix.substances[0].getPvpAW(T)
    pvp_expected = 10.47 * 1e5  # Pa
    pvp_returned = eos.getPvp(T, PvpAW)[0]

    assert eosname == eos.getEOSDisplayName()
    np.testing.assert_allclose(0.9845, zmax, 1e-2)
    np.testing.assert_allclose(0.003341, zmin, 1e-2)
    np.testing.assert_allclose(0.01228, vmax, 1e-2)
    np.testing.assert_allclose(0.00004167, vmin, 1e-2)
    np.testing.assert_allclose(P, eos.getP(vmax, T), 1e-3)
    np.testing.assert_allclose(P, eos.getP(vmin, T), 1e-3)
    np.testing.assert_allclose(pvp_expected, pvp_returned, 1e-3)

    # check equilibrium
    P, T = pvp_returned, 150
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zmin, zmax = np.min(zs), np.max(zs)
    vmin, vmax = np.min(vs), np.max(vs)
    fl = eos.getFugacity(P, T, vmin, zmin)
    fv = eos.getFugacity(P, T, vmax, zmax)
    np.testing.assert_allclose(fl, fv, 1e-3)

    # check all properties #
    Tref, T, Pref, P = 300, 150, 1e5, 2e5
    assert methane.hasCp()
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)
    zsref = eos.getZfromPT(Pref, Tref)
    vsref = eos.getVfromPT(Pref, Tref)

    zliq, zvap, vliq, vvap = np.min(zs), np.max(zs), np.min(vs), np.max(vs)
    zliqref, zvapref, vliqref, vvapref = (
        np.min(zsref),
        np.max(zsref),
        np.min(vsref),
        np.max(vsref),
    )

    igprop = methane.getIGProps(Tref, T, Pref, P)
    ddp_liq = eos.getDeltaDepartureProps(Pref, Tref, vliqref, zliqref, P, T, vliq, zliq)
    ddp_vap = eos.getDeltaDepartureProps(Pref, Tref, vvapref, zvapref, P, T, vvap, zvap)
    pliq = igprop.subtract(ddp_liq)
    pvap = igprop.subtract(ddp_vap)

    expected_pliq = DeltaProp(
        32.669700, -1.224694e04, -89.121399, 1114.993043, -9766.360987, 3595.576453
    )
    expected_pvap = DeltaProp(
        32.669700, -5141.843232, -29.385790, -740.247025, -3860.999697, 540.596510
    )
    assert pliq.isEqual(expected_pliq)
    assert pvap.isEqual(expected_pvap)

    p2liq, p2vap = eos.getCpHSGUA(Tref, T, Pref, P)
    assert p2liq.isEqual(expected_pliq)
    assert p2vap.isEqual(expected_pvap)


def test_check_fugacity_single_substance():
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
    eosname = "Peng and Robinson (1976)"
    eos = EOS(sglmethae, k, eosname)

    T, Tref = 150, 300
    P, Pref = 2e5, 1e5
    zs = eos.getZfromPT(P, T)
    vs = eos.getVfromPT(P, T)

    zliq, zvap = np.min(zs), np.max(zs)
    vliq, vvap = np.min(vs), np.max(vs)

    fl = eos.getFugacity(P, T, vliq, zliq)
    fv = eos.getFugacity(P, T, vvap, zvap)

    np.testing.assert_allclose(fl, 8.58224011e5, 1e-3)
    np.testing.assert_allclose(fv, 1.93892612e5, 1e-3)


def test_get_AllProps_single_subs():
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
    eosname = "Peng and Robinson (1976)"
    eos = EOS(sglmethae, k, eosname)

    T, Tref = 150, 300
    P, Pref = 2e5, 1e5
    pliq, pvap = eos.getAllProps(Tref, T, Pref, P)

    expected_pliq = DeltaProp(
        32.669700, -1.224694e04, -89.121399, 1114.993043, -9766.360987, 3595.576453
    )
    expected_pvap = DeltaProp(
        32.669700, -5141.843232, -29.385790, -740.247025, -3860.999697, 540.596510
    )

    assert expected_pliq.isEqual(pliq.Props)
    assert expected_pvap.isEqual(pvap.Props)


def test_vanderwalls_z_and_v():
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
    k = [[0]]
    sglmethae = MixtureProp([methane], [1.0])
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
