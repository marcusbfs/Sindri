from PySide2 import QtCore, QtWidgets

import db
from ui.db_substanceProperties_ui import Ui_Form_db_substanceProperties
from validators import getDoubleValidatorRegex


class Form_AddSubstanceProperties(QtWidgets.QWidget, Ui_Form_db_substanceProperties):
    signal = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super(Form_AddSubstanceProperties, self).__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint
        )

        self.setWindowTitle("Adding substance")

        self.columnHeaders = [
            "Formula",
            "Name",
            "`CAS #`",
            "`Mol. Wt.`",
            "`Tfp, K`",
            "`Tb, K`",
            "`Tc, K`",
            "`Pc, bar`",
            "`Vc, cm3/mol`",
            "`Zc = PcVc/RTc`",
            "Omega",
            "`Trange, K`",
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
            "`Pvpmin, bar`",
            "`Tmin, K`",
            "`Pvpmax, bar`",
            "`Tmax, K`",
        ]
        self.colLen = len(self.columnHeaders)
        self.substance_added = False
        self.disableConfirmButton()

        # connections
        self.le_name.textChanged.connect(self.disableConfirmButton)
        self.le_formula.textChanged.connect(self.disableConfirmButton)
        self.le_CAS.textChanged.connect(self.disableConfirmButton)

        doublevalidator = getDoubleValidatorRegex(self)
        # general
        self.le_MM.setValidator(doublevalidator)
        self.le_Tb.setValidator(doublevalidator)
        self.le_Tfp.setValidator(doublevalidator)
        self.le_Tc.setValidator(doublevalidator)
        self.le_Pc.setValidator(doublevalidator)
        self.le_Vc.setValidator(doublevalidator)
        self.le_Zc.setValidator(doublevalidator)
        self.le_omega.setValidator(doublevalidator)
        # cp
        self.le_a0.setValidator(doublevalidator)
        self.le_a1.setValidator(doublevalidator)
        self.le_a2.setValidator(doublevalidator)
        self.le_a3.setValidator(doublevalidator)
        self.le_a4.setValidator(doublevalidator)
        self.le_CpTmin.setValidator(doublevalidator)
        self.le_CpTmax.setValidator(doublevalidator)
        # antoine
        self.le_AntoineA.setValidator(doublevalidator)
        self.le_AntoineB.setValidator(doublevalidator)
        self.le_AntoineC.setValidator(doublevalidator)
        self.le_AntoineTmin.setValidator(doublevalidator)
        self.le_AntoineTmax.setValidator(doublevalidator)

    def confirm_clicked(self):

        try:

            # insert general properties substances
            name = self.returnNULLifEmptyString(self.le_name)
            formula = self.returnNULLifEmptyString(self.le_formula)
            cas = self.returnNULLifEmptyString(self.le_CAS)
            tfp_k = self.returnNULLifEmptyFloat(self.le_Tfp)
            tb_k = self.returnNULLifEmptyFloat(self.le_Tb)
            tc_k = self.returnNULLifEmptyFloat(self.le_Tc)
            pc_bar = self.returnNULLifEmptyFloat(self.le_Pc)
            vc_cm3_per_mol = self.returnNULLifEmptyFloat(self.le_Vc)
            zc = self.returnNULLifEmptyFloat(self.le_Zc)
            omega = self.returnNULLifEmptyFloat(self.le_omega)
            molar_weigth = self.returnNULLifEmptyFloat(self.le_MM)

            query = (
                "INSERT INTO substance (name,formula,cas,tfp_k,tb_k,tc_k,pc_bar,vc_cm3_per_mol,zc,omega,molar_weigth)"
                + "VALUES(?,?,?,?,?,?,?,?,?,?,?)"
            )
            db.cursor.execute(
                query,
                (
                    name,
                    formula,
                    cas,
                    tfp_k,
                    tb_k,
                    tc_k,
                    pc_bar,
                    vc_cm3_per_mol,
                    zc,
                    omega,
                    molar_weigth,
                ),
            )

            query = (
                "SELECT substance_id FROM substance WHERE name='"
                + name
                + "' AND formula='"
                + formula
                + "' AND cas='"
                + cas
                + "'"
            )
            db.cursor.execute(query)
            substance_id = int(db.cursor.fetchone()[0])

            cp_eq_type = 1
            cp_tmin = self.returnNULLifEmptyFloat(self.le_CpTmin)
            cp_tmax = self.returnNULLifEmptyFloat(self.le_CpTmax)
            cp_a0 = self.returnNULLifEmptyFloat(self.le_a0)
            cp_a1 = self.returnNULLifEmptyFloat(self.le_a1)
            cp_a2 = self.returnNULLifEmptyFloat(self.le_a2)
            cp_a3 = self.returnNULLifEmptyFloat(self.le_a3)
            cp_a4 = self.returnNULLifEmptyFloat(self.le_a4)

            query = (
                "insert into cp_correlations (substance_id,eq_type,cp_tmin,cp_tmax,cp_a0,cp_a1,cp_a2,cp_a3,cp_a4)"
                + "values(?,?,?,?,?,?,?,?,?)"
            )
            db.cursor.execute(
                query,
                (
                    substance_id,
                    cp_eq_type,
                    cp_tmin,
                    cp_tmax,
                    cp_a0,
                    cp_a1,
                    cp_a2,
                    cp_a3,
                    cp_a4,
                ),
            )

            antoine_eq_type = 1
            antoine_a = self.returnNULLifEmptyFloat(self.le_AntoineA)
            antoine_b = self.returnNULLifEmptyFloat(self.le_AntoineB)
            antoine_c = self.returnNULLifEmptyFloat(self.le_AntoineC)
            tmin_k = self.returnNULLifEmptyFloat(self.le_AntoineTmin)
            tmax_k = self.returnNULLifEmptyFloat(self.le_AntoineTmax)

            query = (
                "insert into antoine_correlations (substance_id,eq_type,antoine_a,antoine_b,antoine_c,tmin_k,tmax_k)"
                + "values(?,?,?,?,?,?,?)"
            )
            db.cursor.execute(
                query,
                (
                    substance_id,
                    antoine_eq_type,
                    antoine_a,
                    antoine_b,
                    antoine_c,
                    tmin_k,
                    tmax_k,
                ),
            )

            self.substance_added = True

        except Exception as e:
            QtWidgets.QMessageBox.about(self, "Error adding substance", str(e))
            return -1

        self.close()

    def isFloat(self, s):
        try:
            float(s) * 1.0 + 1.0
            return True
        except:
            return False

    def cancel_clicked(self):
        self.close()

    def closeEvent(self, QCloseEvent):
        self.signal.emit(self.substance_added)

    def isNameFormulaAndCasValid(self) -> bool:
        return (
            len(self.le_name.text()) > 0
            and len(self.le_formula.text()) > 0
            and len(self.le_CAS.text()) > 0
        )

    def disableConfirmButton(self):
        if self.isNameFormulaAndCasValid():
            self.btn_edit_confirm.setDisabled(False)
        else:
            self.btn_edit_confirm.setDisabled(True)

    def returnNULLifEmptyString(self, le):
        if le.text() == "":
            return None
        return le.text()

    def returnNULLifEmptyFloat(self, le):
        if le.text() == "":
            return None
        return float(le.text())

    def returnNULLifEmptyInteger(self, le):
        if le.text() == "":
            return None
        return int(le.text())
