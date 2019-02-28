import numpy as np
import sympy as sp

from eos import EOS
import IdealGasPropMixtures as IGMix
from constants import R_IG


class Mixture(EOS):
    def __init__(self, compounds, y, k, eos):

        EOS.__init__(self, compounds, y, k, eos)

        self.a0 = np.zeros(self.n)
        self.a1 = np.zeros(self.n)
        self.a2 = np.zeros(self.n)
        self.a3 = np.zeros(self.n)
        self.a4 = np.zeros(self.n)
        self.Tcpmin = np.zeros(self.n)
        self.Tcpmax = np.zeros(self.n)
        for i in range(self.n):
            self.a0[i] = self.compounds[i]["a0"]
            self.a1[i] = self.compounds[i]["a1"]
            self.a2[i] = self.compounds[i]["a2"]
            self.a3[i] = self.compounds[i]["a3"]
            self.a4[i] = self.compounds[i]["a4"]
            self.Tcpmin[i] = self.compounds[i]["Tcpmin_K"]
            self.Tcpmax[i] = self.compounds[i]["Tcpmax_K"]

    def return_delta_IG(self, _P, _T, _Pref, _Tref):
        Cp, msgs = IGMix.return_MixCp_IG(
            _T,
            self.y,
            self.a0,
            self.a1,
            self.a2,
            self.a3,
            self.a4,
            self.Tcpmin,
            self.Tcpmax,
        )
        H = IGMix.return_MixH_IG(
            _Tref, _T, self.y, self.a0, self.a1, self.a2, self.a3, self.a4
        )
        S = IGMix.return_MixS_IG(
            _Tref, _T, _Pref, _P, self.y, self.a0, self.a1, self.a2, self.a3, self.a4
        )
        U = IGMix.return_MixU_IG(H, self.y, _Tref, _T)
        G = IGMix.return_MixG_IG(H, _T, S)
        A = IGMix.return_MixA_IG(U, _T, S)
        return Cp, H, S, G, U, A, msgs

    def return_delta_mixProp(self, _P, _T, _Pref, _Tref):

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
            raise ValueError("Error calculating Z\n" + str(e))

        # state = IGPROP.return_fluidState(
        #     _P,
        #     conv_unit(self.compound["Pc_bar"], "bar", "Pa"),
        #     _T,
        #     self.compound["Tc_K"],
        #     1e5,
        #     delta=1e-4,
        # )

        state = "placeholder"  # TODO how to deal with this
        supercritical = True if state == "supercritical fluid" else False

        Vliq = Zliq * R_IG * _T / _P
        Vvap = Zvap * R_IG * _T / _P
        Vliqref = Zliqref * R_IG * _Tref / _Pref
        Vvapref = Zvapref * R_IG * _Tref / _Pref
        rholiq = self.compound["Mol. Wt."] * 1e-3 / Vliq
        rhovap = self.compound["Mol. Wt."] * 1e-3 / Vvap

        try:
            cp, h, s, g, u, a, msgs = self.return_delta_IG(_P, _T, _Pref, _Tref)
            for m in msgs:
                if m is not None:
                    log += "WARNING Cp temperature range: {0:s}\n".format(m)
        except Exception as e:
            print(str(e))
            raise ValueError(
                "Error calculating ideal properties: maybe one compound have no Cp?"
            )

        try:
            dProp_liq = self.return_delta_ResProperties(
                _Pref, _Tref, Vliqref, Zliqref, _P, _T, Vliq, Zliq
            )
            dProp_vap = self.return_delta_ResProperties(
                _Pref, _Tref, Vvapref, Zvapref, _P, _T, Vvap, Zvap
            )
        except Exception as e:
            print(str(e))
            raise ValueError("Error evaluating departure functions")

        dH_liq = h - dProp_liq["HR"]
        dS_liq = s - dProp_liq["SR"]
        dG_liq = g - dProp_liq["GR"]
        dU_liq = u - dProp_liq["UR"]
        dA_liq = a - dProp_liq["AR"]

        dH_vap = h - dProp_vap["HR"]
        dS_vap = s - dProp_vap["SR"]
        dG_vap = g - dProp_vap["GR"]
        dU_vap = u - dProp_vap["UR"]
        dA_vap = a - dProp_vap["AR"]

        ideal_ret = [cp, h, s, g, u, a]

        liq_ret = [Zliq, Vliq, rholiq, dH_liq, dS_liq, dG_liq, dU_liq, dA_liq, _P, _T]
        vap_ret = [Zvap, Vvap, rhovap, dH_vap, dS_vap, dG_vap, dU_vap, dA_vap, _P, _T]

        return ideal_ret, liq_ret, vap_ret, log, supercritical
