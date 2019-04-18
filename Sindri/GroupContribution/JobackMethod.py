import numpy as np
from typing import List


class GroupContributionJoback:
    def __init__(
        self,
        id: str,
        tfpk: float,
        tbk: float,
        tck: float,
        pck: float,
        vck: float,
        hfk: float,
        gfk: float,
        hvk: float,
        hmk: float,
        CpAk: float,
        CpBk: float,
        CpCk: float,
        CpDk: float,
    ):
        self.id = id
        self.tfpk = tfpk
        self.tbk = tbk
        self.tck = tck
        self.pck = pck
        self.vck = vck
        self.hfk = hfk
        self.gfk = gfk
        self.hvk = hvk
        self.hmk = hmk
        self.CpAk = CpAk
        self.CpBk = CpBk
        self.CpCk = CpCk
        self.CpDk = CpDk


class JobackMethod:
    def __init__(
        self, groups: List[str], q: List[int], natoms: int, Tb_exp: float = None
    ):

        self.groups = groups
        self.quantities = q
        self.n = len(self.groups)
        self.Tb_exp = Tb_exp
        self.natoms = natoms

        _CH3 = GroupContributionJoback(
            "CH3 (1)",
            -5.10,
            23.58,
            0.0141,
            -0.0012,
            65,
            -76.45,
            -43.96,
            567,
            217,
            19.500,
            -8.08e-03,
            1.53e-04,
            -9.67e-08,
        )

        _CH2_ = GroupContributionJoback(
            "CH2 (2)",
            11.27,
            22.88,
            0.0189,
            0.0000,
            56,
            -20.64,
            8.42,
            532,
            619,
            -0.909,
            9.50e-02,
            -5.44e-05,
            1.19e-08,
        )

        CH_ds_2 = GroupContributionJoback(
            "CH(ds) (2)",
            8.13,
            26.73,
            0.0082,
            0.0011,
            41,
            2.09,
            11.30,
            608,
            263,
            -2.140,
            5.74e-02,
            -1.64e-06,
            -1.59e-08,
        )

        C_ds_3 = GroupContributionJoback(
            "C(ds) (3)",
            37.02,
            31.01,
            0.0143,
            0.0008,
            32,
            46.43,
            54.05,
            731,
            572,
            -8.250,
            1.01e-01,
            -1.42e-04,
            6.78e-08,
        )
        ACHO_1 = GroupContributionJoback(
            "ACHO (1)",
            82.83,
            76.34,
            0.0240,
            0.0184,
            -25,
            -221.65,
            -197.37,
            2987,
            1073,
            -2.810,
            1.11e-01,
            -1.16e-04,
            4.94e-08,
        )

        self.groups_db: List[GroupContributionJoback] = [
            _CH3,
            _CH2_,
            CH_ds_2,
            C_ds_3,
            ACHO_1,
        ]

        self.groups_data: List[GroupContributionJoback] = []

        for g in self.groups:
            for gdb in self.groups_db:
                if g == gdb.id:
                    self.groups_data.append(gdb)
                    break

    def setTb_K(self, tb_K: float):
        self.Tb_exp = tb_K

    def getTb_K(self) -> float:
        if self.Tb_exp is None:
            s = 0.0
            for g, na in zip(self.groups_data, self.quantities):
                s += na * g.tbk
            return 198.0 + s
        return self.Tb_exp

    def getTc_K(self) -> float:
        s = 0.0
        for g, na in zip(self.groups_data, self.quantities):
            s += na * g.tck
        return self.getTb_K() / (0.584 + s * (0.965 - s))

    def getPc_bar(self) -> float:
        s = 0.0
        for g, na in zip(self.groups_data, self.quantities):
            s += na * g.pck
        return 1.0 / (0.113 + 0.0032 * self.natoms - s) ** 2

    def getVc_cm3_per_mol(self) -> float:
        s = 0.0
        for g, na in zip(self.groups_data, self.quantities):
            s += na * g.vck
        return 17.5 + s

    def getZc(self) -> float:
        return (
            self.getPc_bar()
            * 1e5
            * self.getVc_cm3_per_mol()
            * 1e-6
            / (8.314 * self.getTc_K())
        )


if __name__ == "__main__":

    # test = JobackMethod(
    #     ["CH3 (1)", "CH2 (2)", "CH(ds) (2)", "ACHO (1)", "C(ds) (3)"], [1, 1, 4, 1, 2], 19
    # )
    test = JobackMethod(["CH3 (1)"], [2], 8)
    # test.setTb_K(184.55)
    print("Tc K:", test.getTc_K())
    print("Pc bar:", test.getPc_bar())
    print("Vc cm3/mol", test.getVc_cm3_per_mol())
    print("Zc", test.getZc())
