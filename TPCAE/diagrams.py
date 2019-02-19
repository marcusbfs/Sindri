import numpy as np
from eos import EOS
from antoineVP import antoineVP
import matplotlib.pyplot as plt


def plot_PV_diagram(compound, Ti_f, V_unit, P_unit, points, ln_scale=False):
    if not isinstance(Ti_f, list):
        raise TypeError("Temperature parameter must be an array of len 2")

    if len(Ti_f) != 2:
        raise TypeError("Temperature parameter must be an array of len 2")

    Ti = Ti_f[0]
    Tf = Ti_f[1]

    Tvec = np.linspace(Ti, Tf, points)

    tol = 1e-5
    kmax = 20

    # set first guess as antoine P, if possible
    if compound.compound["ANTOINE_A"] is not None:
        A = compound.compound["ANTOINE_A"]
        B = compound.compound["ANTOINE_B"]
        C = compound.compound["ANTOINE_C"]
        Tmin = compound.compound["Tmin_K"]
        Tmax = compound.compound["Tmax_K"]
        fvec_antoineVP = np.vectorize(antoineVP)
        P_guess = fvec_antoineVP(Tvec, A, B, C, Tmin, Tmax)[0] * 1e5
    else:
        P_guess = np.full(points, 1e5)

    fvec_return_Pvp_EOS = np.vectorize(compound.return_Pvp_EOS)
    Pvec = fvec_return_Pvp_EOS(Tvec, P_guess, tol=tol, k=kmax)[0]

    Vliq_vec = []
    Vvap_vec = []
    for t, p in zip(Tvec, Pvec):
        Vs = compound.return_V_given_PT(p, t)
        # Vliq_vec.append(np.min(Vs))
        # Vvap_vec.append(np.max(Vs))
        if t <= compound.compound["Tc_K"] and p <= compound.compound["Pc_bar"] * 1e5:
            Vliq_vec.append(np.min(Vs))
            Vvap_vec.append(0.0)
        else:
            Vliq_vec.append(0.0)
            Vvap_vec.append(np.max(Vs))

    Vliq_vec = np.array([Vliq_vec])[0]
    Vvap_vec = np.array([Vvap_vec])[0]

    fig, ax = plt.subplots()
    ax.plot(Vliq_vec, Pvec, label="liq")
    ax.plot(Vvap_vec, Pvec, label="vap")
    ax.plot(
        compound.compound["Vc_cm3/mol"] / 100 ** 3,
        compound.compound["Pc_bar"] * 1e5,
        marker="o",
        markersize=3,
    )
    ax.legend()
    plt.show()
