from PySide2 import QtCore, QtWidgets

import db
from ui.db_substanceProperties_ui import Ui_Form_db_substanceProperties
from validators import getDoubleValidatorRegex


class Form_EditSubstanceProperties(QtWidgets.QWidget, Ui_Form_db_substanceProperties):
    signal_changes_made = QtCore.Signal(bool)

    def __init__(self, parent=None, hl_row=None):
        super(Form_EditSubstanceProperties, self).__init__(parent)
        self.setupUi(self)

        self.hl_row = hl_row
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint
        )
        self.changes_made = False

        # Connect buttons
        self.connect(
            self.le_name, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_formula,
            QtCore.SIGNAL("textChanged(QString)"),
            self.lineEdit_changed,
        )
        self.connect(
            self.le_CAS, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_MM, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_Tfp, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_Tb, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_Tc, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_Pc, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_Vc, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_Zc, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_omega, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_a0, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_a1, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_a2, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_a3, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_a4, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_CpTmin, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_CpTmax, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed
        )
        self.connect(
            self.le_AntoineA,
            QtCore.SIGNAL("textChanged(QString)"),
            self.lineEdit_changed,
        )
        self.connect(
            self.le_AntoineB,
            QtCore.SIGNAL("textChanged(QString)"),
            self.lineEdit_changed,
        )
        self.connect(
            self.le_AntoineC,
            QtCore.SIGNAL("textChanged(QString)"),
            self.lineEdit_changed,
        )
        self.connect(
            self.le_AntoineTmin,
            QtCore.SIGNAL("textChanged(QString)"),
            self.lineEdit_changed,
        )
        self.connect(
            self.le_AntoineTmax,
            QtCore.SIGNAL("textChanged(QString)"),
            self.lineEdit_changed,
        )

        self.Formula = self.hl_row[0]
        self.Name = self.hl_row[1]
        self.CAS = self.hl_row[2]
        self.MM = self.hl_row[3] if self.hl_row[3] != "None" else ""
        self.Tfp = self.hl_row[4] if self.hl_row[4] != "None" else ""
        self.Tb = self.hl_row[5] if self.hl_row[5] != "None" else ""
        self.Tc = self.hl_row[6] if self.hl_row[6] != "None" else ""
        self.Pc = self.hl_row[7] if self.hl_row[7] != "None" else ""
        self.Vc = self.hl_row[8] if self.hl_row[8] != "None" else ""
        self.Zc = self.hl_row[9] if self.hl_row[9] != "None" else ""
        self.omega = self.hl_row[10] if self.hl_row[10] != "None" else ""

        self.r = self.extract_Cp_Tminmax(self.hl_row[11])
        self.CpTmin = self.r[0] if self.r[0] != "None" else ""
        self.CpTmax = self.r[1] if self.r[1] != "None" else ""
        self.a0 = self.hl_row[12] if self.hl_row[12] != "None" else ""
        self.a1 = self.hl_row[13] if self.hl_row[13] != "None" else ""
        self.a2 = self.hl_row[14] if self.hl_row[14] != "None" else ""
        self.a3 = self.hl_row[15] if self.hl_row[15] != "None" else ""
        self.a4 = self.hl_row[16] if self.hl_row[16] != "None" else ""

        self.AntoineA = self.hl_row[19] if self.hl_row[19] != "None" else ""
        self.AntoineB = self.hl_row[20] if self.hl_row[20] != "None" else ""
        self.AntoineC = self.hl_row[21] if self.hl_row[21] != "None" else ""
        self.AntoineTmin = self.hl_row[23] if self.hl_row[23] != "None" else ""
        self.AntoineTmax = self.hl_row[25] if self.hl_row[25] != "None" else ""

        query = (
            "SELECT substance_id FROM substance WHERE name='"
            + self.Name
            + "' AND formula='"
            + self.Formula
            + "' AND cas='"
            + self.CAS
            + "'"
        )
        db.cursor.execute(query)
        self.substance_id_int = int(db.cursor.fetchone()[0])

        self.setWindowTitle("Edit substance - " + str(self.Name))

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

        self.load_entries()

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

    def load_entries(self):
        self.le_formula.setText(self.Formula)
        self.le_name.setText(self.Name)
        self.le_CAS.setText(self.CAS)
        self.le_MM.setText(self.MM)
        self.le_Tfp.setText(self.Tfp)
        self.le_Tb.setText(self.Tb)
        self.le_Tc.setText(self.Tc)
        self.le_Pc.setText(self.Pc)
        self.le_Vc.setText(self.Vc)
        self.le_Zc.setText(self.Zc)
        self.le_omega.setText(self.omega)

        self.le_CpTmin.setText(self.CpTmin)
        self.le_CpTmax.setText(self.CpTmax)
        self.le_a0.setText(self.a0)
        self.le_a1.setText(self.a1)
        self.le_a2.setText(self.a2)
        self.le_a3.setText(self.a3)
        self.le_a4.setText(self.a4)

        self.le_AntoineA.setText(self.AntoineA)
        self.le_AntoineB.setText(self.AntoineB)
        self.le_AntoineC.setText(self.AntoineC)
        self.le_AntoineTmin.setText(self.AntoineTmin)
        self.le_AntoineTmax.setText(self.AntoineTmax)
        self.changes_made = False

    def extract_Cp_Tminmax(self, s):
        if "-" in s:
            return s.split("-")
        else:
            return ["", ""]

    def confirm_clicked(self):
        if self.changes_made:
            edit_confirm_msg = "Save editions?"
            choice = QtWidgets.QMessageBox.question(
                self,
                "Saving changes",
                edit_confirm_msg,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No,
            )

            if choice == QtWidgets.QMessageBox.Yes:
                try:
                    self.updateSubstanceValues()
                    self.updateCpCorrelationsValues()
                    self.updateAntoineCorrelationsValues()
                    self.close()
                except:
                    msg = QtWidgets.QMessageBox.about(
                        self, "Error", "Could not save changes"
                    )

    def isFloat(self, s):
        try:
            float(s) * 1.0 + 1
            return True
        except:
            return False

    def lineEdit_changed(self):
        self.changes_made = True

    def cancel_clicked(self):
        self.changes_made = False
        self.close()

    def closeEvent(self, QCloseEvent):
        self.signal_changes_made.emit(self.changes_made)

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

    def updateCpCorrelationsValues(self):
        cp_tmin = self.returnNULLifEmptyFloat(self.le_CpTmin)
        cp_tmax = self.returnNULLifEmptyFloat(self.le_CpTmax)
        cp_a0 = self.returnNULLifEmptyFloat(self.le_a0)
        cp_a1 = self.returnNULLifEmptyFloat(self.le_a1)
        cp_a2 = self.returnNULLifEmptyFloat(self.le_a2)
        cp_a3 = self.returnNULLifEmptyFloat(self.le_a3)
        cp_a4 = self.returnNULLifEmptyFloat(self.le_a4)

        query = """UPDATE cp_correlations SET cp_tmin=?,
        cp_tmax=?,
        cp_a0=?,
        cp_a1=?,
        cp_a2=?,
        cp_a3=?,
        cp_a4=? WHERE substance_id=?"""
        db.cursor.execute(
            query,
            (
                cp_tmin,
                cp_tmax,
                cp_a0,
                cp_a1,
                cp_a2,
                cp_a3,
                cp_a4,
                self.substance_id_int,
            ),
        )

    def updateAntoineCorrelationsValues(self):
        antoine_a = self.returnNULLifEmptyFloat(self.le_AntoineA)
        antoine_b = self.returnNULLifEmptyFloat(self.le_AntoineB)
        antoine_c = self.returnNULLifEmptyFloat(self.le_AntoineC)
        tmin_k = self.returnNULLifEmptyFloat(self.le_AntoineTmin)
        tmax_k = self.returnNULLifEmptyFloat(self.le_AntoineTmax)

        query = """UPDATE antoine_correlations SET antoine_a=?,
                 antoine_b=?,
                 antoine_c=?,
                 tmin_k=?,
                 tmax_k=? WHERE substance_id=?"""
        db.cursor.execute(
            query,
            (antoine_a, antoine_b, antoine_c, tmin_k, tmax_k, self.substance_id_int),
        )

    def updateSubstanceValues(self):
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

        query = """UPDATE substance SET name=?,
        formula=?,
        cas=?,
        tfp_k=?,
        tb_k=?,
        tc_k=?,
        pc_bar=?,
        vc_cm3_per_mol=?,
        zc=?,
        omega=?,
        molar_weigth=? WHERE substance_id=?
        """
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
                self.substance_id_int,
            ),
        )

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
