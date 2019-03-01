from collections import namedtuple

import numpy as np

import IdealGasPropertiesPureSubstance as IGPROP
from constants import R_IG
from db_utils import get_compound_properties
from eos import EOS
from units import conv_unit
from vapor_pressure import ambroseWaltonVP, antoineVP, leeKeslerVP


class PureSubstance(EOS):
    """
    This class is used for calculations of a pure substance properties using a Cubic Equation of State.
    """

    def __init__(self, name, formula, eos):
        """ Initialize the Pure Substance class.

        Parameters
        ----------
        name : str
            Name of the compound. This compound is going to be extracted from the database.
        formula : str
            Formula of the compound. This compound is going to be extracted from the database.
        eos : str
            Name of the cubic equation of state. This name must be equal one of the values from
            the 'eos_options' dictionary.

        """
        self.compound = [get_compound_properties(name, formula)]
        self.k = [[0], [0]]
        self.y = [1.0]
        EOS.__init__(self, self.compound, self.y, self.k, eos)

    def return_Pvp_EOS(self, _T, initialP, tol=10 * np.finfo(float).eps, k=50):
        """ Return the vapor pressure estimated at '_T', using the cubic equation of state.

        Estimates the vapor pressure by applying the liquid-vapor equilibrium condition: in this condition, the
        fugacity value of both states must be equal (fL = fV). This function returns the pressure value that
        satisfies this condition, given a tolerance. The fugacity values are calculated using the departure functions
        given by Poling (2002).

        Parameters
        ----------
        _T : float
            given temperature, in Kelvin, to estimate the vapor pressure..
        initialP : float
            initial pressure guess, in bar.
        tol : float, optional
            maximum tolerance for the error.
        k : int, optional
            maximum iterations value.

        Returns
        -------
        Pvp_EOS : namedtuple of (float, int, str or None)
            Pvp_EOS.Pvp : float
                The vapor pressure calculated, in Pascal.
            Pvp_EOS.iter : int
                The number of iterations needed to calculate Pvp_EOS.Pvp.
            Pvp_EOS.msg : str or None
                Returns a warning message if the calcualtes exceeds the maximum iterations value. Else, returns None.

        """
        _P = initialP

        PvpEOS = namedtuple("Pvp_EOS", ["Pvp", "iter", "msg"])

        for i in range(1, k + 1):
            Zs = self.return_Z_given_PT(_P, _T)
            Zl = np.min(Zs)
            Zv = np.max(Zs)
            Vl = Zl * R_IG * _T / _P
            Vv = Zv * R_IG * _T / _P

            fL = _P * np.e ** self.helper_Pvp_f(Vl, Zl, _T)
            fV = _P * np.e ** self.helper_Pvp_f(Vv, Zv, _T)
            _P = _P * fL / fV
            error = fL / fV - 1.0
            if np.abs(error) < tol:
                return PvpEOS(_P, i, None)

        return PvpEOS(_P, k, str(k) + " (max iterations)")

    def all_calculations_at_P_T(self, _P, _T, _Pref, _Tref):

        try:
            ideal_ret, liq_ret, vap_ret, log, supercritical = self.return_delta_prop(
                _P, _T, _Pref, _Tref
            )
            has_ideal = True
        except:
            has_ideal = False

        Zliq = liq_ret[0]
        Vliq = liq_ret[1]
        Zvap = vap_ret[0]
        Vvap = vap_ret[1]

        f_liq = self.return_fugacity(_P, _T, Vliq, Zliq)
        f_vap = self.return_fugacity(_P, _T, Vvap, Zvap)

        Pvp_AW = ambroseWaltonVP(
            conv_unit(self.compound["Pc_bar"], "bar", "Pa"),
            _T / self.compound["Tc_K"],
            self.compound["omega"],
        )

        Pvp_LK = leeKeslerVP(
            conv_unit(self.compound["Pc_bar"], "bar", "Pa"),
            _T / self.compound["Tc_K"],
            self.compound["omega"],
        )

        if not supercritical:
            try:
                PvpTuple = self.return_Pvp_EOS(_T, Pvp_AW, k=100)
                Pvp = PvpTuple.Pvp
                Pvpmsg = PvpTuple.msg
                Pvpiter = PvpTuple.iter
                if Pvpmsg is not None:
                    log += "Iterations for vapor pressure: {0:s}\n".format(str(Pvpmsg))
                else:
                    log += "Iterations for vapor pressure: {0:s}\n".format(str(Pvpiter))
            except:
                # TODO como lidar quando o fluido se encontra no estado critico?
                raise ValueError("Error calculating vapor pressure from EOS")

            log += "Pvp Ambrose-Walton relative error: {0:.5f}\n".format(
                IGPROP.abs_rel_err(Pvp, Pvp_AW)
            )
            log += "Pvp Lee-Kesler relative error: {0:.5f}\n".format(
                IGPROP.abs_rel_err(Pvp, Pvp_LK)
            )

            try:
                Pvp_Antoine = antoineVP(
                    _T,
                    self.compound["ANTOINE_A"],
                    self.compound["ANTOINE_B"],
                    self.compound["ANTOINE_C"],
                    self.compound["Tmin_K"],
                    self.compound["Tmax_K"],
                )
                log += "Pvp Antoine relative error: {0:.5f}\n".format(
                    IGPROP.abs_rel_err(Pvp, Pvp_Antoine.Pvp)
                )
                if Pvp_Antoine.msg is not None:
                    log += "WARNING Antoine's temperature range: {0:s}\n".format(
                        Pvp_Antoine.msg
                    )

            except:
                Pvp_Antoine = None
                log += "WARNING couldn't compute pressure vapor using Antoine's equation: missing equation parameters\n"

            Pvp_dict = {
                "EOS": Pvp,
                "AmbroseWalton": Pvp_AW,
                "LeeKesler": Pvp_LK,
                "Antoine": Pvp_Antoine,
            }
        else:  # if state is supercritical
            log += "Couldn't compute vapor pressure (maybe the current fluid is in supercritical state?)\n"
            Pvp = Pvp_AW
            Pvp_dict = 0

        state = IGPROP.return_fluidState(
            _P,
            conv_unit(self.compound["Pc_bar"], "bar", "Pa"),
            _T,
            self.compound["Tc_K"],
            Pvp,
            delta=1e-4,
        )

        if ideal_ret is not None:

            ideal_dict = {
                "Cp": ideal_ret[0],
                "dH": ideal_ret[1],
                "dS": ideal_ret[2],
                "dG": ideal_ret[3],
                "dU": ideal_ret[4],
                "dA": ideal_ret[5],
            }
        else:
            ideal_dict = None

        liq_dict = {
            "Z": liq_ret[0],
            "V": liq_ret[1],
            "rho": liq_ret[2],
            "dH": liq_ret[3],
            "dS": liq_ret[4],
            "dG": liq_ret[5],
            "dU": liq_ret[6],
            "dA": liq_ret[7],
            "f": f_liq,
            "P": _P,
            "T": _T,
        }

        vap_dict = {
            "Z": vap_ret[0],
            "V": vap_ret[1],
            "rho": vap_ret[2],
            "dH": vap_ret[3],
            "dS": vap_ret[4],
            "dG": vap_ret[5],
            "dU": vap_ret[6],
            "dA": vap_ret[7],
            "f": f_vap,
            "P": _P,
            "T": _T,
        }
        prop = namedtuple(
            "prop",
            [
                "T",
                "P",
                "Tref",
                "Pref",
                "ideal",
                "liq",
                "vap",
                "Pvp",
                "state",
                "log",
                "name",
            ],
        )

        retprop = prop(
            _T,
            _P,
            _Tref,
            _Pref,
            ideal_dict,
            liq_dict,
            vap_dict,
            Pvp_dict,
            state,
            log,
            self.compound["Name"],
        )
        return retprop

    def critical_point_calculation(self, _Pref, _Tref):
        _Tc = self.compound["Tc_K"]
        _Pc_guess = ambroseWaltonVP(
            conv_unit(self.compound["Pc_bar"], "bar", "Pa"), 1.0, self.compound["omega"]
        )
        _Pc = self.return_Pvp_EOS(_Tc, _Pc_guess, k=100).Pvp
        return self.all_calculations_at_P_T(_Pc, _Tc, _Pref, _Tref)
