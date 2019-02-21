import numpy as np
from vapor_pressure import leeKeslerVP
from units import conv_unit
import matplotlib.pyplot as plt
from scipy import interpolate

valid_diagrams = ["PV", "TS", "TV", "PS", "PT", "HS"]


def plot_diag(
    data, diag, xunit, yunit, xlnscale=False, ylnscale=False, grid=True, smooth=False
):
    if diag not in valid_diagrams:
        raise ValueError(str(diag) + " is not a valid diagram")

    cp_data = data[1]
    data = data[0]

    if diag == "PV":
        title = "Pressure vs. Molar volume"

        xliq = np.asarray([i.liq["V"] for i in data])
        xvap = np.asarray([i.vap["V"] for i in data])
        yliq = np.asarray([i.Pvp for i in data])

        # convert units
        xliq = conv_unit(xliq, "m3/mol", xunit)
        xvap = conv_unit(xvap, "m3/mol", xunit)
        yliq = conv_unit(yliq, "Pa", yunit)
        yvap = np.copy(yliq)

        xc = conv_unit(cp_data.liq["V"], "m3/mol", xunit)
        yc = conv_unit(cp_data.Pvp, "Pa", yunit)

        ylabel = "Pressure [{0}]".format(yunit)
        xlabel = "Molar volume [{0}]".format(xunit)

    elif diag == "TS":
        title = "Temperature vs. Entropy"

        xliq = np.asarray([i.liq["dS"] for i in data])
        xvap = np.asarray([i.vap["dS"] for i in data])
        yliq = np.asarray([i.T for i in data])

        # convert units
        yliq = conv_unit(yliq, "K", yunit)
        yvap = np.copy(yliq)

        xc = cp_data.liq["dS"]
        yc = conv_unit(cp_data.T, "K", yunit)

        ylabel = "Temperature [{0}]".format(yunit)
        xlabel = "Entropy [{0}]".format(xunit)

    elif diag == "HS":
        title = "Enthalphy vs. Entropy"

        xliq = np.asarray([i.liq["dS"] for i in data])
        xvap = np.asarray([i.vap["dS"] for i in data])
        yliq = np.asarray([i.liq["dH"] for i in data])
        yvap = np.asarray([i.vap["dH"] for i in data])

        # convert units
        yliq = conv_unit(yliq, "J/mol", yunit)
        yvap = conv_unit(yvap, "J/mol", yunit)

        xc = cp_data.vap["dS"]
        yc = conv_unit(cp_data.vap["dH"], "J/mol", yunit)

        ylabel = "Enthalpy [{0}]".format(yunit)
        xlabel = "Entropy [{0}]".format(xunit)

    elif diag == "PS":
        title = "Pressure vs. Entropy"

        xliq = np.asarray([i.liq["dS"] for i in data])
        xvap = np.asarray([i.vap["dS"] for i in data])
        yvec = np.asarray([i.Pvp for i in data])

        # convert units
        yliq = conv_unit(yvec, "Pa", yunit)
        yvap = np.copy(yliq)

        yc = conv_unit(cp_data.Pvp, "Pa", yunit)
        xc = cp_data.vap["dS"]

        ylabel = "Pressure [{0}]".format(yunit)
        xlabel = "Entropy [{0}]".format(xunit)

    elif diag == "TV":
        title = "Temperature vs. Molar volume"

        xliq = np.asarray([i.liq["V"] for i in data])
        xvap = np.asarray([i.vap["V"] for i in data])
        yvec = np.asarray([i.T for i in data])

        # convert units
        xliq = conv_unit(xliq, "m3/mol", xunit)
        xvap = conv_unit(xvap, "m3/mol", xunit)
        yliq = conv_unit(yvec, "K", yunit)
        yvap = np.copy(yliq)

        yc = conv_unit(cp_data.T, "K", yunit)
        xc = conv_unit(cp_data.vap["V"], "m3/mol", xunit)

        ylabel = "Temperature [{0}]".format(yunit)
        xlabel = "Molar volume [{0}]".format(xunit)

    elif diag == "PT":
        title = "Pressure vs. Temperature"

        xvap = []
        yvap = []

        xliq = np.asarray([i.T for i in data])
        yliq = np.asarray([i.Pvp for i in data])

        # convert units
        xliq = conv_unit(xliq, "K", xunit)
        yliq = conv_unit(yliq, "Pa", yunit)

        yc = conv_unit(cp_data.P, "Pa", yunit)
        xc = conv_unit(cp_data.T, "K", xunit)

        ylabel = "Pressure [{0}]".format(yunit)
        xlabel = "Temperature [{0}]".format(xunit)

    try:
        if xlnscale:
            if np.all(xliq > 0.0) and np.all(xvap > 0):
                xliq = np.log(xliq)
                xvap = np.log(xvap)
                xc = np.log(xc)
                xlabel = "ln " + xlabel
            else:
                raise ValueError("Can't calculate log of x-axis: negative number")
        if ylnscale:
            if ylnscale and np.all(yliq > 0) and np.all(yvap > 0):
                yvap = np.log(yvap)
                yliq = np.log(yliq)
                yc = np.log(yc)
                ylabel = "ln " + ylabel
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
    if grid:
        ax.grid()

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

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    plt.show()
    return


def gen_data(compound, Ti_f, _Pref, _Tref, points):
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

    return (retvec, critical_point)
