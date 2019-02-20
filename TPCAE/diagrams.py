import numpy as np
from vapor_pressure import leeKeslerVP
from units import conv_unit
import matplotlib.pyplot as plt

valid_diagrams = ["PV", "TS", "TV", "PS", "PT"]


def plot_diag(data, diag, xunit, yunit, xlnscale=False, ylnscale=False, grid=True):
    if diag not in valid_diagrams:
        raise ValueError(str(diag) + " is not a valid diagram")

    if diag == "PV":
        title = "Pressure vs. Molar volume"
        xliq = np.asarray([i.liq["V"] for i in data])
        xvap = np.asarray([i.vap["V"] for i in data])
        yvec = np.asarray([i.Pvp for i in data])

        # convert units
        xliq = conv_unit(xliq, "m3/mol", xunit)
        xvap = conv_unit(xvap, "m3/mol", xunit)
        yvec = conv_unit(yvec, "Pa", yunit)

        ylabel = "Pressure [{0}]".format(yunit)
        xlabel = "Molar volume [{0}]".format(xunit)

    elif diag == "TS":
        title = "Temperature vs. Entropy"
        xliq = np.asarray([i.liq["dS"] for i in data])
        xvap = np.asarray([i.vap["dS"] for i in data])
        yvec = np.asarray([i.T for i in data])

        # convert units
        yvec = conv_unit(yvec, "K", yunit)

        ylabel = "Temperature [{0}]".format(yunit)
        xlabel = "Entropy [{0}]".format(xunit)

    elif diag == "PS":
        title = "Pressure vs. Entropy"
        xliq = np.asarray([i.liq["dS"] for i in data])
        xvap = np.asarray([i.vap["dS"] for i in data])
        yvec = np.asarray([i.Pvp for i in data])

        # convert units
        yvec = conv_unit(yvec, "Pa", yunit)

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
        yvec = conv_unit(yvec, "K", yunit)

        ylabel = "Temperature [{0}]".format(yunit)
        xlabel = "Molar volume [{0}]".format(xunit)

    elif diag == "PT":
        title = "Pressure vs. Temperature"
        xvec = np.asarray([i.T for i in data])
        yvec = np.asarray([i.Pvp for i in data])

        # convert units
        xvec = conv_unit(xvec, "K", xunit)
        yvec = conv_unit(yvec, "Pa", yunit)

        ylabel = "Pressure [{0}]".format(yunit)
        xlabel = "Temperature [{0}]".format(xunit)

        if xlnscale:
            xvec = np.log(xvec)
            xlabel = "ln " + xlabel
        if ylnscale:
            yvec = np.log(yvec)
            ylabel = "ln " + ylabel

        fig, ax = plt.subplots()
        ax.plot(xvec, yvec)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        if grid:
            ax.grid()
        plt.show()
        return

    if xlnscale:
        xliq = np.log(xliq)
        xvap = np.log(xvap)
        xlabel = "ln " + xlabel
    if ylnscale:
        yvec = np.log(yvec)
        ylabel = "ln " + ylabel

    fig, ax = plt.subplots()
    ax.plot(xliq, yvec, label="Liquid")
    ax.plot(xvap, yvec, label="Vapor")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.set_title(title)
    if grid:
        ax.grid()
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
    Pc = compound.return_Pvp_EOS(Tf, helper_P_guess(Tf)).Pvp
    Vc = compound.return_V_given_PT(Pc, Tf)

    Tvec = np.linspace(Ti, Tf, points)

    # set first guess as antoine P, if possible
    P_guess = helper_P_guess(Tvec)

    fvec_return_Pvp_EOS = np.vectorize(compound.return_Pvp_EOS)
    Pvec = fvec_return_Pvp_EOS(Tvec, P_guess, tol=tol, k=kmax)[0]

    retvec = []

    for t, p in zip(Tvec, Pvec):
        ret = compound.all_calculations_at_P_T(p, t, _Pref, _Tref)
        retvec.append(ret)

    return retvec
