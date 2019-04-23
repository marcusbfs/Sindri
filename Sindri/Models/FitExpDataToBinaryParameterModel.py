import numpy as np
from scipy.optimize import least_squares

from Models.MixtureModel import MixtureModel


class FitExpDataToBinaryParameterModel:
    def __init__(
        self,
        model: MixtureModel,
        isovar: float,
        diagtype: str,
        x_exp,
        y_exp,
        data_exp,
        initial_k: float = 0.0,
    ):

        self.model = model
        self.isovar = isovar
        self.diagtype = diagtype  # 'isothermal' or 'isobaric'
        self.x_exp = np.atleast_1d(x_exp)
        self.y_exp = np.atleast_1d(y_exp)
        self.data_exp = np.atleast_1d(data_exp)
        self.initial_k = initial_k

        if np.allclose(0, self.x_exp[0], 1e-5):
            self.x_exp = self.x_exp[1:]
            self.y_exp = self.y_exp[1:]
            self.data_exp = self.data_exp[1:]

        if np.allclose(1, self.x_exp[-1], 1e-5):
            self.x_exp = self.x_exp[:-1]
            self.y_exp = self.y_exp[:-1]
            self.data_exp = self.data_exp[:-1]

        self.n_exp = len(self.x_exp)

    def fitBinaryInteractionParameter(self):

        if self.diagtype == "isothermal":
            objective_function = self._objectiveFunction_isothermal
        elif self.diagtype == "isobaric":
            objective_function = self._objectiveFunction_isobaric
        else:
            raise ValueError("Diagtype isn't either 'isothermal' or 'isobaric'")

        ans = least_squares(objective_function, self.initial_k, method="lm")
        ret = ans.x[0]
        return ret

    def _objectiveFunction_isothermal(self, k: float):
        # paper: https://www.sciencedirect.com/science/article/pii/009813549500001I
        self._setK(k)

        p_exp = self.data_exp

        x1_exp = self.x_exp
        x2_exp = 1.0 - x1_exp

        y1_exp = self.y_exp
        y2_exp = 1.0 - y1_exp
        t = self.isovar

        s = 0.0
        for i in range(self.n_exp):
            zls = self.model.system.getZfromPT(p_exp[i], t, [x1_exp[i], x2_exp[i]])
            zl = np.min(zls)
            phi_liq_0 = self.model.system.getPhi_i(
                0, [x1_exp[i], x2_exp[i]], p_exp[i], t, zl
            )
            phi_liq_1 = self.model.system.getPhi_i(
                1, [x1_exp[i], x2_exp[i]], p_exp[i], t, zl
            )

            zvs = self.model.system.getZfromPT(p_exp[i], t, [y1_exp[i], y2_exp[i]])
            zv = np.max(zvs)
            phi_vap_0 = self.model.system.getPhi_i(
                0, [y1_exp[i], y2_exp[i]], p_exp[i], t, zv
            )
            phi_vap_1 = self.model.system.getPhi_i(
                1, [y1_exp[i], y2_exp[i]], p_exp[i], t, zv
            )

            k0_exp = y1_exp[i] / x1_exp[i]
            k1_exp = y2_exp[i] / x2_exp[i]
            k0_calc = phi_liq_0 / phi_vap_0
            k1_calc = phi_liq_1 / phi_vap_1

            s += ((np.log(k0_exp) - np.log(k0_calc)) / np.log(k0_exp)) ** 2
            s += ((np.log(k1_exp) - np.log(k1_calc)) / np.log(k1_exp)) ** 2
            # s += ((np.log(k0_exp) - np.log(k0_calc)) ) ** 2
            # s += ((np.log(k1_exp) - np.log(k1_calc)) ) ** 2

        return s

    def _objectiveFunction_isobaric(self, k: float):
        # paper: https://www.sciencedirect.com/science/article/pii/009813549500001I
        self._setK(k)

        t_exp = self.data_exp

        x1_exp = self.x_exp
        x2_exp = 1.0 - x1_exp

        y1_exp = self.y_exp
        y2_exp = 1.0 - y1_exp
        p = self.isovar

        s = 0.0
        for i in range(self.n_exp):
            zls = self.model.system.getZfromPT(p, t_exp[i], [x1_exp[i], x2_exp[i]])
            zl = np.min(zls)
            phi_liq_0 = self.model.system.getPhi_i(
                0, [x1_exp[i], x2_exp[i]], p, t_exp[i], zl
            )
            phi_liq_1 = self.model.system.getPhi_i(
                1, [x1_exp[i], x2_exp[i]], p, t_exp[i], zl
            )

            zvs = self.model.system.getZfromPT(p, t_exp[i], [y1_exp[i], y2_exp[i]])
            zv = np.max(zvs)
            phi_vap_0 = self.model.system.getPhi_i(
                0, [y1_exp[i], y2_exp[i]], p, t_exp[i], zv
            )
            phi_vap_1 = self.model.system.getPhi_i(
                1, [y1_exp[i], y2_exp[i]], p, t_exp[i], zv
            )

            k0_exp = y1_exp[i] / x1_exp[i]
            k1_exp = y2_exp[i] / x2_exp[i]
            k0_calc = phi_liq_0 / phi_vap_0
            k1_calc = phi_liq_1 / phi_vap_1

            s += ((np.log(k0_exp) - np.log(k0_calc)) / np.log(k0_exp)) ** 2
            s += ((np.log(k1_exp) - np.log(k1_calc)) / np.log(k1_exp)) ** 2

        return s

    def _setK(self, v: float):
        n = self.model.getNumberOfSubstancesInSystem()
        k = np.zeros((n, n), dtype=np.float64)
        k[0][1] = v
        k[1][0] = v
        self.model.setBinaryInteractionsParameters(k)
