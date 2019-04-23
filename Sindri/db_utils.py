import db


class Compound:
    def __init__(self, cdict):
        self._cdict = cdict

    def getName(self):
        return self._testString(self._cdict["Name"])

    def getFormula(self):
        return self._testString(self._cdict["Formula"])

    def getCAS(self):
        return self._testString(self._cdict["CAS"])

    def getMolWt(self):
        return self._testValue(self._cdict["Mol. Wt."])

    def getTfp(self):
        return self._testValue(self._cdict["Tfp_K"])

    def getTb(self):
        return self._testValue(self._cdict["Tb_K"])

    def getTc(self):
        return self._testValue(self._cdict["Tc_K"])

    def getPc(self):
        return self._testValue(self._cdict["Pc_bar"]) * 1e5

    def getVc(self):
        return self._testValue(self._cdict["Vc_cm3/mol"]) / 100 ** 3

    def getZc(self):
        return self._testValue(self._cdict["Zc"])

    def getOmega(self):
        return self._testValue(self._cdict["omega"])

    def getTcpMin(self):
        return self._testValue(self._cdict["Tcpmin_K"])

    def getTcpMax(self):
        return self._testValue(self._cdict["Tcpmax_K"])

    def geta0(self):
        return self._testValue(self._cdict["a0"])

    def geta1(self):
        return self._testValue(self._cdict["a1"])

    def geta2(self):
        return self._testValue(self._cdict["a2"])

    def geta3(self):
        return self._testValue(self._cdict["a3"])

    def geta4(self):
        return self._testValue(self._cdict["a4"])

    def getCpCoeffs(self):
        return self.geta0(), self.geta1(), self.geta2(), self.geta3(), self.geta4()

    def hasAllCpCoeffs(self):
        try:
            a = self.geta0() + 1.0
            a = self.geta1() + 1.0
            a = self.geta2() + 1.0
            a = self.geta3() + 1.0
            a = self.geta4() + 1.0
            return True
        except:
            return False

    def hasAntoine(self):
        if self.getAntoineA() and self.getAntoineB() and self.getAntoineC():
            return True
        return False

    def getAntoineCoeffs(self):
        return (
            self.getAntoineA(),
            self.getAntoineB(),
            self.getAntoineC(),
            self.getAntoineTmin(),
            self.getAntoineTmax(),
        )

    def getCpIG(self):
        return self._testValue(self._cdict["CpIG"])

    def getCpliq(self):
        return self._testValue(self._cdict["Cpliq"])

    def getAntoineA(self):
        return self._testValue(self._cdict["ANTOINE_A"])

    def getAntoineB(self):
        return self._testValue(self._cdict["ANTOINE_B"])

    def getAntoineC(self):
        return self._testValue(self._cdict["ANTOINE_C"])

    def getAntoinePvmin(self):
        return self._testValue(self._cdict["Pvmin_bar"]) * 1e5

    def getAntoinePvmax(self):
        return self._testValue(self._cdict["Pvmax_bar"]) * 1e5

    def getAntoineTmin(self):
        return self._testValue(self._cdict["Tmin_K"])

    def getAntoineTmax(self):
        return self._testValue(self._cdict["Tmax_K"])

    def _testValue(self, val):
        try:
            val = float(val)
            _tmp = val + 1.0
            ret = val
        except:
            ret = False
        return ret

    def _testString(self, s):
        if len(s) > 0:
            return s
        else:
            return False


def get_compound_properties(name, formula):
    """
    Search for 'name' and 'formula' in the database and returns a dictionary of the result.

    Parameters
    ----------
    name : str
        Name of the compound to be searched.
    formula : str
        Formula of the compound to be searched.

    Returns
    -------
    compound_dict : dict
        A dictionary containing the correspondent values for the substance in the database.
        The dictionary has the following keys:
            "Formula",
            "Name",
            "CAS",
            "Mol. Wt.",
            "Tfp_K",
            "Tb_K",
            "Tc_K",
            "Pc_bar",
            "Vc_cm3/mol",
            "Zc",
            "omega",
            "Tcpmin_K",
            "Tcpmax_K",
            "a0",
            "a1",
            "a2",
            "a3",
            "a4",
            "CpIG",
            "Cpliq",
            "ANTOINE_A",
            "ANTOINE_B",
            "ANTOINE_C",
            "Pvmin_bar",
            "Tmin_K",
            "Pvmax_bar",
            "Tmax_K"
        If the compound has no value on a specific key, the value stored is '""' or 'None'.

    """
    db.init()  # verificar problemas com isso aqui
    table_name = "v_all_properties_including_correlations"
    query = (
        "SELECT * FROM "
        + table_name
        + " WHERE formula LIKE '%"
        + formula
        + "%'"
        + " AND name LIKE '%"
        + name
        + "%'"
    )
    db.cursor.execute(query)
    results = db.cursor.fetchall()
    res = results[0]

    dict_names = [
        "Formula",
        "Name",
        "CAS",
        "Mol. Wt.",
        "Tfp_K",
        "Tb_K",
        "Tc_K",
        "Pc_bar",
        "Vc_cm3/mol",  # 8
        "Zc",
        "omega",  # 10
        "Tcpmin_K",  # 11
        "Tcpmax_K",  # 11
        "a0",  # 12
        "a1",
        "a2",
        "a3",
        "a4",  # 16
        "CpIG",
        "Cpliq",
        "ANTOINE_A",
        "ANTOINE_B",
        "ANTOINE_C",
        "Pvmin_bar",
        "Tmin_K",
        "Pvmax_bar",
        "Tmax_K",
    ]

    res2 = []
    for i in range(len(res)):
        if i == 11:
            tmin = None
            tmax = None
            if res[i] and "-" in res[i]:
                temps = res[i].split("-")
                tmin = float(temps[0])
                tmax = float(temps[1])

            res2.append(tmin)
            res2.append(tmax)
        else:
            res2.append(res[i])

    mydict = dict(zip(dict_names, res2))
    return Compound(mydict)
