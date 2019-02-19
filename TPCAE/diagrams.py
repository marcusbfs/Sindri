import numpy as np
from vapor_pressure import leeKeslerVP
from units import conv_unit
import matplotlib.pyplot as plt


def plot_diagram(compound, Ti_f, V_unit, P_unit, points, ln_scale=False):
    if not isinstance(Ti_f, list):
        raise TypeError("Temperature parameter must be an array of len 2")

    if len(Ti_f) != 2:
        raise TypeError("Temperature parameter must be an array of len 2")

    def helper_P_guess(_T):
        fh = lambda x: leeKeslerVP(
            conv_unit(compound.compound["Pc_bar"], "bar", "Pa"),
            x / compound.compound["Tc_K"],
            compound.compound["omega"],
        )
        fvec = np.vectorize(fh)
        return fvec(_T)

    tol = 1e-5
    kmax = 20

    Ti = Ti_f[0]
    Tf = Ti_f[1]
    Pc = compound.return_Pvp_EOS(Tf, helper_P_guess(Tf)).Pvp
    Vc = compound.return_V_given_PT(Pc, Tf)

    Tvec = np.linspace(Ti, Tf, points)

    # set first guess as antoine P, if possible
    P_guess = helper_P_guess(Tvec)

    fvec_return_Pvp_EOS = np.vectorize(compound.return_Pvp_EOS)
    Pvec = fvec_return_Pvp_EOS(Tvec, P_guess, tol=tol, k=kmax)[0]

    Vliq_vec = []
    Vvap_vec = []

    _Pref = 1e5
    _Tref = 273.16

    from time import time

    calc_beg = time()
    for t, p in zip(Tvec, Pvec):
        ret = compound.all_calculations_at_P_T(p, t, _Pref, _Tref)
        Vliq_vec.append(ret.liq["V"])
        Vvap_vec.append(ret.vap["V"])

    calc_end = time()

    calc_time = calc_end - calc_beg

    print("{0:.5f} sec".format(calc_time))

    Vliq_vec = np.asarray(Vliq_vec)
    Vvap_vec = np.asarray(Vvap_vec)

    fig, ax = plt.subplots()
    ax.plot(Vliq_vec, Pvec, label="liq")
    ax.plot(Vvap_vec, Pvec, label="vap")
    ax.plot(Vc, Pc, marker="o", markersize=3)
    ax.legend()
    plt.show()
