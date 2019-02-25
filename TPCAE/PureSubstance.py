from collections import namedtuple

import numpy as np
import sympy as sp
from numba import njit, cfunc, types, double
from scipy import LowLevelCallable
from scipy.integrate import quad

import IdealGasPropertiesPureSubstance as IGPROP
from constants import R_IG
from eos import EOS
from polyEqSolver import solve_cubic
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
        EOS.__init__(self, name, formula, eos)
        self.initialize_functions()

    # TODO put this function in EOS class? maybe it'll be better for mixture calculations
    def initialize_functions(self):

        self.b = np.real(self.b)
        self.delta = np.real(self.delta)
        self.epsilon = np.real(self.epsilon)

        self.Z_V_T = None
        self.dZ_VT_dT = None
        self.numfunc_P_given_VT = None

        self.return_Z_V_T()
        self.return_diff_Z_V_T_dT()

        # create numerical functions
        self.numf_Z_VT = njit()(
            sp.lambdify([self.V, self.T], self.Z_V_T, modules="numpy")
        )
        self.numf_dZdT_VT = njit()(
            sp.lambdify([self.V, self.T], sp.diff(self.Z_V_T, self.T), modules="numpy")
        )
        self.numf_theta_T = njit()(sp.lambdify([self.T], self.theta, modules="numpy"))
        self.numf_P_VT = njit()(
            sp.lambdify(
                [self.V, self.T], self.Z_V_T * self.T * R_IG / self.V, modules="numpy"
            )
        )

        # this ain't pretty but hey, it works fast!
        self.tmp_cfunc = None
        c_sig = types.double(types.intc, types.CPointer(types.double))
        exec(
            "self.tmp_cfunc = lambda n, data: {:s}".format(
                str((1 - self.Z_V_T) / self.V)
                .replace("V", "data[0]")
                .replace("T", "data[1]")
            )
        )
        qf = cfunc(c_sig)(self.tmp_cfunc)
        self.qnf = LowLevelCallable(qf.ctypes)

        self.helper_Pvp_f = (
            lambda hv, hz, _T: hz
            - 1.0
            - np.log(hz)
            - quad(self.qnf, hv, np.inf, args=(_T,))[0]
        )

        exec(
            "self.tmp_cfunc2 = lambda n, data: {:s}".format(
                str(self.T * sp.diff(self.Z_V_T, self.T) / self.V)
                .replace("V", "data[0]")
                .replace("T", "data[1]")
            )
        )
        tf = cfunc(c_sig)(self.tmp_cfunc2)
        self.numf_UR = LowLevelCallable(tf.ctypes)

    def return_Z_V_T(self):
        """
        Creates the symbolic equation:
            Z = V / (V - b) - ((theta / (R_IG * T)) * V) / (V**2 + delta * V + epsilon)

        Returns
        -------
        self.Z_V_T : sympy symbolic expression.

        """
        if self.Z_V_T is None:
            self.Z_V_T = self.V / (self.V - self.b) - (
                self.theta / (R_IG * self.T)
            ) * self.V / (self.V ** 2 + self.delta * self.V + self.epsilon)

    def return_Z_given_PT(self, _P, _T):
        """ Return the positive roots (Z) of the cubic equation.

        parameters
        ----------
        _P : float
            pressure, pa.
        _T : float
            temperature, k.

        Returns
        -------
        ans : array, float
            Returns an array of the real roots of the cubic equation of state. The minimum value of this array
            corresponds to the vapor state, while the maximum value corresponds to the liquid state.

        """

        Bl = self.b * _P / (R_IG * _T)
        deltal = self.delta * _P / (R_IG * _T)
        thetal = self.numf_theta_T(_T) * _P / (R_IG * _T) ** 2
        epsilonl = self.epsilon * (_P / (R_IG * _T)) ** 2
        a = 1.0
        b = deltal - Bl - 1.0
        c = thetal + epsilonl - deltal * (Bl + 1.0)
        d = -(epsilonl * (Bl + 1.0) + Bl * thetal)

        coefs = (a, b, c, d)

        ans = np.asarray(solve_cubic(*coefs))
        return ans[ans > 0]

    def return_V_given_PT(self, _P, _T):
        """ Return the positive roots (V) of the cubic equation.

        Parameters
        ----------
        _P : float
            pressure, Pa.
        _T : float
            temperature, K.

        Returns
        -------
        ans : array, float
            Returns an array of the real roots of the cubic equation of state. The minimum value of this array
            corresponds to the vapor state, while the maximum value corresponds to the liquid state.

        """
        ans = self.return_Z_given_PT(_P, _T) * R_IG * _T / _P
        self.Vval = ans
        return ans

    def return_P_given_VT(self, _V, _T):
        """ Return the values of '_P' given '_V' and '_T' using the cubic equation of state.

        Parameters
        ----------
        _V : float
            molar volume, m3/mol.
        _T : float
            temperature, Kelvin.

        Returns
        -------
        _P : float
            pressure at '_T' and '_V', Pascal.

        """
        _P = self.numf_P_VT(_V, _T)
        return _P

    def return_diff_Z_V_T_dT(self):
        if self.dZ_VT_dT is None:
            self.return_Z_V_T()
            self.dZ_VT_dT = sp.diff(self.Z_V_T, self.T)

    def return_departureProperties(self, _P, _T, _V, _Z):
        """
        Returns the enthalpy, entropy, Gibbs energy, internal energy, Helmholtz energy and fugacity at
        '_P' and '_T', utilizing departure functions from Poling (2002). All values are in the S.I. units.

        Parameters
        ----------
        _P : float
            pressure, Pa.
        _T : float
            temperature, K.
        _V : float
            molar volume, m3/mol.
        _Z : float
            compressibility factor, adimensional.

        Returns
        -------
        dict_ans : dictionary, float
            Returns a dictionary with the values of thermodynamics properties calculated using the departure
            functions. The dictionary keys are: 'HR', 'SR', 'GR', 'UR', 'AR', 'f'.

        """

        # calculate UR
        UR_RT = quad(self.numf_UR, _V, np.inf, args=(_T,))[0]
        UR = UR_RT * _T * R_IG
        # calculate AR
        AR_RT = quad(self.qnf, _V, np.inf, args=(_T,))[0] + np.log(_Z)
        # AR_RT = quad(self.numf_integratePvp, _V, np.inf, args=(_T,))[0] + np.log(_Z)
        AR = AR_RT * _T * R_IG
        # calculate HR
        HR_RT = UR_RT + 1.0 - _Z
        HR = HR_RT * R_IG * _T
        # calculate SR
        SR_R = UR_RT - AR_RT
        SR = SR_R * R_IG
        # calculate GR
        GR_RT = AR_RT + 1 - _Z
        GR = GR_RT * R_IG * _T

        fugacity = _P * np.exp(-GR_RT)

        dict_ans = {"HR": HR, "SR": SR, "GR": GR, "UR": UR, "AR": AR, "f": fugacity}
        return dict_ans

    def return_delta_ResProperties(self, _Pref, _Tref, _Vref, _Zref, _P, _T, _V, _Z):
        ref = self.return_departureProperties(_Pref, _Tref, _Vref, _Zref)
        proc = self.return_departureProperties(_P, _T, _V, _Z)
        delta = np.array(list(proc.values())) - np.array(list(ref.values()))
        dict_delta = dict(zip(ref.keys(), delta))
        dict_delta["f"] = proc["f"]
        return dict_delta

    def return_Pvp_EOS(self, _T, initialP, tol=1e-4, k=50):
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

        log = ""

        try:  # Calculate Z
            Zs = self.return_Z_given_PT(_P, _T)
            Zliq = np.min(Zs)
            Zvap = np.max(Zs)

            Zsref = self.return_Z_given_PT(_Pref, _Tref)
            Zliqref = np.min(Zsref)
            Zvapref = np.max(Zsref)

        except Exception as e:
            print(str(e))
            raise ValueError("Error calculating Z")

        state = IGPROP.return_fluidState(
            _P,
            conv_unit(self.compound["Pc_bar"], "bar", "Pa"),
            _T,
            self.compound["Tc_K"],
            1e5,
            delta=1e-4,
        )

        supercritical = True if state == "supercritical fluid" else False

        Vliq = Zliq * R_IG * _T / _P
        Vvap = Zvap * R_IG * _T / _P
        Vliqref = Zliqref * R_IG * _Tref / _Pref
        Vvapref = Zvapref * R_IG * _Tref / _Pref
        rholiq = self.compound["Mol. Wt."] * 1e-3 / Vliq
        rhovap = self.compound["Mol. Wt."] * 1e-3 / Vvap

        if (
            self.compound["a0"] is not None
            and self.compound["a1"] is not None
            and self.compound["a2"] is not None
            and self.compound["a3"] is not None
            and self.compound["a4"] is not None
        ):
            has_cp = True
        else:
            has_cp = False

        try:
            dProp_liq = self.return_delta_ResProperties(
                _Pref, _Tref, Vliqref, Zliqref, _P, _T, Vliq, Zliq
            )
            dProp_vap = self.return_delta_ResProperties(
                _Pref, _Tref, Vvapref, Zvapref, _P, _T, Vvap, Zvap
            )
        except:
            raise ValueError("Error evaluating departure functions")

        if has_cp:
            a0 = self.compound["a0"]
            a1 = self.compound["a1"]
            a2 = self.compound["a2"]
            a3 = self.compound["a3"]
            a4 = self.compound["a4"]
            Tmin = self.compound["Tcpmin_K"]
            Tmax = self.compound["Tcpmax_K"]

            try:
                IGprop = IGPROP.return_IdealGasProperties(
                    _Tref, _T, _Pref, _P, a0, a1, a2, a3, a4, Tmin, Tmax
                )
            except:
                raise ValueError("Error calculating ideal properties")

            ideal_dict = {
                "Cp": IGprop["Cp_IG"],
                "dH": IGprop["dH_IG"],
                "dS": IGprop["dS_IG"],
                "dG": IGprop["dG_IG"],
                "dU": IGprop["dU_IG"],
                "dA": IGprop["dA_IG"],
            }

            if IGprop["msg"] is not None:
                log += "WARNING Cp temperature range: {0:s}\n".format(IGprop["msg"])

            dH_liq = IGprop["dH_IG"] - dProp_liq["HR"]
            dS_liq = IGprop["dS_IG"] - dProp_liq["SR"]
            dG_liq = IGprop["dG_IG"] - dProp_liq["GR"]
            dU_liq = IGprop["dU_IG"] - dProp_liq["UR"]
            dA_liq = IGprop["dA_IG"] - dProp_liq["AR"]

            dH_vap = IGprop["dH_IG"] - dProp_vap["HR"]
            dS_vap = IGprop["dS_IG"] - dProp_vap["SR"]
            dG_vap = IGprop["dG_IG"] - dProp_vap["GR"]
            dU_vap = IGprop["dU_IG"] - dProp_vap["UR"]
            dA_vap = IGprop["dA_IG"] - dProp_vap["AR"]
        else:
            ideal_dict = None
            dH_liq = None
            dS_liq = None
            dG_liq = None
            dU_liq = None
            dA_liq = None

            dH_vap = None
            dS_vap = None
            dG_vap = None
            dU_vap = None
            dA_vap = None

        f_liq = dProp_liq["f"]
        f_vap = dProp_vap["f"]

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
                PvpTuple = self.return_Pvp_EOS(_T, Pvp_AW, tol=1e-5, k=100)
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

        liq_dict = {
            "Z": Zliq,
            "V": Vliq,
            "rho": rholiq,
            "dH": dH_liq,
            "dS": dS_liq,
            "dG": dG_liq,
            "dU": dU_liq,
            "dA": dA_liq,
            "f": f_liq,
            "P": _P,
            "T": _T,
        }

        vap_dict = {
            "Z": Zvap,
            "V": Vvap,
            "rho": rhovap,
            "dH": dH_vap,
            "dS": dS_vap,
            "dG": dG_vap,
            "dU": dU_vap,
            "dA": dA_vap,
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
        _Pc = self.return_Pvp_EOS(_Tc, _Pc_guess, tol=1e-6, k=100).Pvp
        return self.all_calculations_at_P_T(_Pc, _Tc, _Pref, _Tref)

    def change_eos(self, new_eos):
        """ Change and update the cubic equation of state used by this class.

        This function updates the variables 'self.Z_V_T' and 'self.Z_P_T' using the new cubic equation of state
        paramaters.

        Parameters
        ----------
        new_eos : str
            New cubic equation of state name. This name must be a valid value from the 'eos_options' dictionary.

        """
        self.eos = new_eos.lower()
        self.initialize()
        self.initialize_functions()
