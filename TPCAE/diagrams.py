import numpy as np
from units import conv_unit
import matplotlib.pyplot as plt
from scipy import interpolate
from eos import EOS
from Properties import Props
from typing import List

# valid_diagrams = ["PV", "TS", "TV", "PS", "PT", "HS"]

SI_dict = {"P": "Pa", "V": "m3/mol", "T": "K", "H": "J/mol", "S": "J/molK"}

labels_dict = {
    "P": "Pressure",
    "V": "Molar volume",
    "T": "Temperature",
    "H": "Enthalpy",
    "S": "Entropy",
}

class PlotPureSubstanceDiagrams(object):
    def __init__(
        self,
        allpropsliq: List[Props],
        allpropsvap: List[Props],
        cp: Props,
        compound: str,
        eosname: str,
    ):

        self.propsliq = allpropsliq
        self.propsvap = allpropsvap
        assert len(self.propsliq) == len(self.propsvap)
        self.n = len(self.propsliq)
        self.cpoint = cp
        self.compound = compound
        self.eosname = eosname

        self.Tliq, self.Tvap = np.zeros(self.n), np.zeros(self.n)
        self.Pliq, self.Pvap = np.zeros(self.n), np.zeros(self.n)
        self.Vliq, self.Vvap = np.zeros(self.n), np.zeros(self.n)
        self.Hliq, self.Hvap = np.zeros(self.n), np.zeros(self.n)
        self.Sliq, self.Svap = np.zeros(self.n), np.zeros(self.n)
        self.Gliq, self.Gvap = np.zeros(self.n), np.zeros(self.n)
        self.Uliq, self.Uvap = np.zeros(self.n), np.zeros(self.n)
        self.Aliq, self.Avap = np.zeros(self.n), np.zeros(self.n)

        self.xliq, self.xvap = None, None
        self.yliq, self.yvap = None, None
        self.x_letter, self.y_letter = None, None
        self.xunit, self.yunit = None, None
        self.xcp, self.ycp = None, None
        self.title = None
        self.xlabel, self.ylabel = "", ""
        self.lnscale = False
        self.grid = True
        self.smooth = True

        for i in range(self.n):
            self.Tliq[i], self.Tvap[i] = self.propsliq[i].T, self.propsvap[i].T
            self.Pliq[i], self.Pvap[i] = self.propsliq[i].P, self.propsvap[i].P
            self.Vliq[i], self.Vvap[i] = self.propsliq[i].V, self.propsvap[i].V
            self.Hliq[i], self.Hvap[i] = (
                self.propsliq[i].Props.H,
                self.propsvap[i].Props.H,
            )
            self.Sliq[i], self.Svap[i] = (
                self.propsliq[i].Props.S,
                self.propsvap[i].Props.S,
            )
            self.Gliq[i], self.Gvap[i] = (
                self.propsliq[i].Props.G,
                self.propsvap[i].Props.G,
            )
            self.Uliq[i], self.Uvap[i] = (
                self.propsliq[i].Props.U,
                self.propsvap[i].Props.U,
            )
            self.Aliq[i], self.Avap[i] = (
                self.propsliq[i].Props.A,
                self.propsvap[i].Props.A,
            )

    def plotPV(self, xunit: str, yunit: str, lnscale=True, smooth=True, grid=True):
        self.x_letter, self.y_letter = "V", "P"
        self.xliq, self.yliq = self.Vliq, self.Pliq
        self.xvap, self.yvap = self.Vvap, self.Pvap
        self.xcp, self.ycp = self.cpoint.V, self.cpoint.P
        self.xunit, self.yunit = xunit, yunit

        self.lnscale = lnscale
        self.grid = grid
        self.smooth = smooth

    def plotTS(self, xunit: str, yunit: str, lnscale=False, smooth=True, grid=True):
        self.x_letter, self.y_letter = "S", "T"
        self.xliq, self.yliq = self.Sliq, self.Tliq
        self.xvap, self.yvap = self.Svap, self.Tvap
        self.xcp, self.ycp = self.cpoint.Props.S, self.cpoint.T
        self.xunit, self.yunit = xunit, yunit

        self.lnscale = lnscale
        self.grid = grid
        self.smooth = smooth

    def plotPS(self, xunit: str, yunit: str, lnscale=False, smooth=True, grid=True):
        self.x_letter, self.y_letter = "S", "P"
        self.xliq, self.yliq = self.Sliq, self.Pliq
        self.xvap, self.yvap = self.Svap, self.Pvap
        self.xcp, self.ycp = self.cpoint.Props.S, self.cpoint.P
        self.xunit, self.yunit = xunit, yunit

        self.lnscale = lnscale
        self.grid = grid
        self.smooth = smooth

    def plotHS(self, xunit: str, yunit: str, lnscale=False, smooth=True, grid=True):
        self.x_letter, self.y_letter = "S", "H"
        self.xliq, self.yliq = self.Sliq, self.Hliq
        self.xvap, self.yvap = self.Svap, self.Hvap
        self.xcp, self.ycp = self.cpoint.Props.S, self.cpoint.Props.H
        self.xunit, self.yunit = xunit, yunit

        self.lnscale = lnscale
        self.grid = grid
        self.smooth = smooth

    def plotTV(self, xunit: str, yunit: str, lnscale=True, smooth=True, grid=True):
        self.x_letter, self.y_letter = "V", "T"
        self.xliq, self.yliq = self.Vliq, self.Tliq
        self.xvap, self.yvap = self.Vvap, self.Tvap
        self.xcp, self.ycp = self.cpoint.V, self.cpoint.T
        self.xunit, self.yunit = xunit, yunit

        self.lnscale = lnscale
        self.grid = grid
        self.smooth = smooth

    def plotPT(self, xunit: str, yunit: str, lnscale=False, smooth=True, grid=True):
        self.x_letter, self.y_letter = "T", "P"
        self.xliq, self.yliq = self.Tliq, self.Pliq
        self.xvap, self.yvap = self.Tvap, self.Pvap
        self.xcp, self.ycp = self.cpoint.T, self.cpoint.P
        self.xunit, self.yunit = xunit, yunit

        self.lnscale = lnscale
        self.grid = grid
        self.smooth = smooth

    def _plot(self):
        self.title = "{}: {}\n{}".format(
            self.compound,
            "{} vs {}".format(labels_dict[self.y_letter], labels_dict[self.x_letter]),
            self.eosname,
        )
        self.xlabel = "{} [{}]".format(labels_dict[self.x_letter], self.xunit)
        self.ylabel = "{} [{}]".format(labels_dict[self.y_letter], self.yunit)

        try:
            self.xliq = conv_unit(self.xliq, SI_dict[self.x_letter], self.xunit)
            self.xvap = conv_unit(self.xvap, SI_dict[self.x_letter], self.xunit)

            self.yliq = conv_unit(self.yliq, SI_dict[self.y_letter], self.yunit)
            self.yvap = conv_unit(self.yvap, SI_dict[self.y_letter], self.yunit)

            self.xcp = conv_unit(self.xcp, SI_dict[self.x_letter], self.xunit)
            self.ycp = conv_unit(self.ycp, SI_dict[self.y_letter], self.yunit)
        except Exception as e:
            print("Error converting units in diagram\n{}".format(str(e)))
            raise

        if self.lnscale:
            try:
                self.xliq, self.xvap = np.log(self.xliq), np.log(self.xvap)
                self.yliq, self.yvap = np.log(self.yliq), np.log(self.yvap)
                self.xcp, self.ycp = np.log(self.xcp), np.log(self.ycp)
                self.xlabel = "ln " + self.xlabel
                self.ylabel = "ln " + self.ylabel
            except Exception as e:
                print("Error changing to log scale")
                print(str(e))
                raise

        if self.smooth:
            try:
                n = 100
                tliq = interpolate.splrep(
                    np.sort(self.xliq), self.yliq[self.xliq.argsort()]
                )
                self.xliq = np.linspace(np.min(self.xliq), np.max(self.xliq), n)
                self.yliq = interpolate.splev(self.xliq, tliq)

                tvap = interpolate.splrep(
                    np.sort(self.xvap), self.yvap[self.xvap.argsort()]
                )
                self.xvap = np.linspace(np.min(self.xvap), np.max(self.xvap), n)
                self.yvap = interpolate.splev(self.xvap, tvap)
            except Exception as e:
                print("Error calculating spline")
                print(str(e))
                raise

        fig, ax = plt.subplots()
        if self.grid:
            ax.grid()
        try:
            ax.plot(self.xliq, self.yliq, label="Liquid")
            ax.plot(self.xvap, self.yvap, label="Vapor")
        except Exception as e:
            print("Error plotting liquid and vapor lines\n{}".format(str(e)))
            raise
        try:
            ax.plot(self.xcp, self.ycp, label="Critical point", marker="o")
        except Exception as e:
            print("Error plotting critical point\n{}".format(str(e)))
            raise
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.title)
        ax.legend()
        plt.show()
        return


def gen_data(
    eoseq: EOS, Ti_f: float, _Pref: float, _Tref: float, points: int, isotherms=[]
):
    if not isinstance(Ti_f, list):
        raise TypeError("Temperature parameter must be an array of len 2")

    if len(Ti_f) != 2:
        raise TypeError("Temperature parameter must be an array of len 2")

    def helper_P_guess(_T):
        fh = lambda x: eoseq.mix.substances[0].getPvpAW(x)
        fvec = np.vectorize(fh)
        return fvec(_T)

    Ti = Ti_f[0]
    Tf = Ti_f[1]
    Tvec = np.linspace(Ti, Tf, points)

    # set first guess as antoine P, if possible
    P_guess = helper_P_guess(Tvec)

    fvec_return_Pvp_EOS = np.vectorize(eoseq.getPvp)
    Pvec = fvec_return_Pvp_EOS(Tvec, P_guess)[0]

    retliq = []
    retvap = []

    for t, p in zip(Tvec, Pvec):
        rl, rv = eoseq.getAllProps(_Tref, t, _Pref, p)
        retliq.append(rl)
        retvap.append(rv)

    Tc, Pc = eoseq.mix.substances[0].Tc, eoseq.mix.substances[0].Pc
    critical_point = eoseq.getAllProps(_Tref, Tc, _Pref, Pc)[0]

    return (retliq, retvap, critical_point)
