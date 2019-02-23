import numpy as np
from vapor_pressure import leeKeslerVP
from units import conv_unit
import matplotlib.pyplot as plt
from scipy import interpolate

valid_diagrams = ["PV", "TS", "TV", "PS", "PT", "HS"]

SI_units_dict = {"P": "Pa", "V": "m3/mol", "T": "K", "dH": "J/mol"}

labels_dict = {
    "P": "Pascal",
    "V": "Molar volume",
    "T": "Temperature",
    "dH": "Enthalpy",
    "dS": "Entropy",
}

titles_dict = {
    "PV": "Pressure vs. Molar volume",
    "PS": "Pressure vs. Entropy",
    "PT": "Pressure vs. Temperature",
    "TV": "Temperature vs. Molar volume",
    "TS": "Temperature vs. Entropy",
    "HS": "Enthalpy vs. Entropy",
}

prop_dict = {"P": "P", "V": "V", "T": "T", "H": "dH", "S": "dS"}


def plot_diag(
    data,
    diag,
    xunit,
    yunit,
    xlnscale=False,
    ylnscale=False,
    grid=True,
    smooth=False,
    isotherms=False,
):
    if diag not in valid_diagrams:
        raise ValueError(str(diag) + " is not a valid diagram")

    isotherms_data = data[2]
    cp_data = data[1]
    data = data[0]
    has_isotherms = True if (len(isotherms_data) > 0 and isotherms) else False

    ys = prop_dict[diag[0]]
    xs = prop_dict[diag[1]]
    points = len(data)
    title = data[0].name + ": " + titles_dict[diag]
    xlabel = labels_dict[xs] + " [{0}]".format(xunit)
    ylabel = labels_dict[ys] + " [{0}]".format(yunit)

    xliq = np.zeros(points)
    yliq = np.zeros(points)
    xvap = np.zeros(points)
    yvap = np.zeros(points)

    for i in range(points):
        xliq[i] = data[i].liq[xs]
        yliq[i] = data[i].liq[ys]
        xvap[i] = data[i].vap[xs]
        yvap[i] = data[i].vap[ys]

    xc = cp_data.liq[xs]
    yc = cp_data.liq[ys]

    # isotherms
    xliq_iso = []
    yliq_iso = []
    xvap_iso = []
    yvap_iso = []
    if has_isotherms:
        for isotherm in isotherms_data:
            p = len(isotherm)
            xliq_tmp = np.zeros(p)
            yliq_tmp = np.zeros(p)
            xvap_tmp = np.zeros(p)
            yvap_tmp = np.zeros(p)

            for i in range(p):
                xliq_tmp[i] = isotherm[i].liq[xs]
                yliq_tmp[i] = isotherm[i].liq[ys]
                xvap_tmp[i] = isotherm[i].vap[xs]
                yvap_tmp[i] = isotherm[i].vap[ys]
            xliq_iso.append(xliq_tmp)
            yliq_iso.append(yliq_tmp)
            xvap_iso.append(xvap_tmp)
            yvap_iso.append(yvap_tmp)

    # convert units
    if xs != "dS":
        xliq = conv_unit(xliq, SI_units_dict[xs], xunit)
        xliq = conv_unit(xliq, SI_units_dict[xs], xunit)
        xvap = conv_unit(xvap, SI_units_dict[xs], xunit)
        xc = conv_unit(xc, SI_units_dict[xs], xunit)
        if has_isotherms:
            for i in range(len(xliq_iso)):
                xliq_iso[i] = conv_unit(xliq_iso[i], SI_units_dict[xs], xunit)
                xvap_iso[i] = conv_unit(xvap_iso[i], SI_units_dict[xs], xunit)

    if ys != "dS":
        yliq = conv_unit(yliq, SI_units_dict[ys], yunit)
        yvap = conv_unit(yvap, SI_units_dict[ys], yunit)
        yc = conv_unit(yc, SI_units_dict[ys], yunit)
        if has_isotherms:
            for i in range(len(yliq_iso)):
                yliq_iso[i] = conv_unit(yliq_iso[i], SI_units_dict[ys], yunit)
                yvap_iso[i] = conv_unit(yvap_iso[i], SI_units_dict[ys], yunit)

    try:
        if xlnscale:
            if np.all(xliq > 0.0) and np.all(xvap > 0):
                xliq = np.log(xliq)
                xvap = np.log(xvap)
                xc = np.log(xc)
                xlabel = "ln " + xlabel
                if has_isotherms:
                    xliq_iso = np.log(xliq_iso)
                    xvap_iso = np.log(xvap_iso)

            else:
                raise ValueError("Can't calculate log of x-axis: negative number")
        if ylnscale:
            if ylnscale and np.all(yliq > 0) and np.all(yvap > 0):
                yvap = np.log(yvap)
                yliq = np.log(yliq)
                yc = np.log(yc)
                ylabel = "ln " + ylabel
                if has_isotherms:
                    yliq_iso = np.log(yliq_iso)
                    yvap_iso = np.log(yvap_iso)
            else:
                raise ValueError("Can't calculate log of y-axis: negative number")
    except Exception as e:
        print("error calculating log scale")
        print(str(e))
        raise

    if smooth:

        n = 100

        try:
            if len(xliq) > 0 and len(yliq) > 0:
                # must sort x vector
                tliq = interpolate.splrep(np.sort(xliq), yliq[xliq.argsort()])
                xliq = np.linspace(np.min(xliq), np.max(xliq), n)
                yliq = interpolate.splev(xliq, tliq)

            if len(xvap) > 0 and len(yvap) > 0:
                tvap = interpolate.splrep(np.sort(xvap), yvap[xvap.argsort()])
                xvap = np.linspace(np.min(xvap), np.max(xvap), n)
                yvap = interpolate.splev(xvap, tvap)
        except Exception as e:
            print("error calculating spline")
            print(str(e))
            raise

    fig, ax = plt.subplots()

    try:
        if len(xliq) > 0 and len(yliq) > 0:
            ax.plot(xliq, yliq, label="Liquid")
        if len(xvap) > 0 and len(yvap) > 0:
            ax.plot(xvap, yvap, label="Vapor")
    except Exception as e:
        print("error plotting curve")
        print(str(e))
        raise

    try:
        ax.plot(xc, yc, label="Critical point", marker="o")
    except Exception as e:
        print("error plotting critical point")
        print(str(e))
        raise

    if has_isotherms:
        try:
            for t, xl, yl, xv, yv in zip(
                isotherms_data, xliq_iso, yliq_iso, xvap_iso, yvap_iso
            ):
                ax.plot(xl, yl, label=str(t[0].T) + " liq", linestyle="--")
                ax.plot(xv, yv, label=str(t[0].T) + " vap", linestyle="--")
        except Exception as e:
            raise

    if grid:
        ax.grid()

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    plt.show()
    return


def gen_data(compound, Ti_f, _Pref, _Tref, points, isotherms=[]):
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
    Tvec = np.linspace(Ti, Tf, points)

    # set first guess as antoine P, if possible
    P_guess = helper_P_guess(Tvec)

    fvec_return_Pvp_EOS = np.vectorize(compound.return_Pvp_EOS)
    Pvec = fvec_return_Pvp_EOS(Tvec, P_guess, tol=tol, k=kmax)[0]

    retvec = []

    for t, p in zip(Tvec, Pvec):
        ret = compound.all_calculations_at_P_T(p, t, _Pref, _Tref)
        retvec.append(ret)

    critical_point = compound.critical_point_calculation(_Pref, _Tref)

    isotherms = np.atleast_1d(isotherms)
    Pmin = np.min(Pvec)
    Pmax = np.max(Pvec)
    isothermsvec = []
    if len(isotherms) > 0:
        for t in isotherms:
            Psat = fvec_return_Pvp_EOS(t, helper_P_guess(t))[0]
            Vsat = compound.return_V_given_PT(Psat, t)
            tmpt = []
            for d in retvec:
                ret = compound.all_calculations_at_P_T(d.P, t, _Pref, _Tref)

                # if (ret.liq["V"] <= d.liq["V"]) and (ret.vap["V"] >= d.vap["V"]):
                if True:
                    tmpt.append(ret)
            isothermsvec.append(tmpt)

    # t = 120
    # vs = compound.return_V_given_PT(Pmin, t)
    # v, P = gen_PV_isotherm(compound, np.min(vs), np.max(vs),t, 30)
    # isothermsvec = (v, P)

    return (retvec, critical_point, isothermsvec)


def gen_PV_isotherm(compound, vi, vf, T, points, xlnscale=True, ylnscale=True):
    vi = 1.1e-4
    vf = 7.08e-4
    T = 360
    v = np.geomspace(vi, vf, points)
    P = np.zeros(points)
    for i in range(points):
        P[i] = compound.numf_P_VT(v[i], T)

    print(v)
    print(P)

    plt.plot(v, P)
    plt.show()

    return v, P
