from PySide2 import QtCore, QtWidgets

import db
from ui.db_substanceProperties_ui import Ui_Form_db_substanceProperties


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

    def confirm_clicked(self):

        if self.isFloat(self.le_CpTmin.text()) and self.isFloat(self.le_CpTmax.text()):
            Trange = self.le_CpTmin.text() + "-" + self.le_CpTmax.text()
        else:
            Trange = ""

        query = "insert into database values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        items = (
            self.le_formula.text(),
            self.le_name.text(),
            self.le_CAS.text(),
            self.le_MM.text(),
            self.le_Tfp.text(),
            self.le_Tb.text(),
            self.le_Tc.text(),
            self.le_Pc.text(),
            self.le_Vc.text(),
            self.le_Zc.text(),
            self.le_omega.text(),
            Trange,
            self.le_a0.text(),
            self.le_a1.text(),
            self.le_a2.text(),
            self.le_a3.text(),
            self.le_a4.text(),
            "",
            "",
            self.le_AntoineA.text(),
            self.le_AntoineC.text(),
            self.le_AntoineB.text(),
            "",
            self.le_AntoineTmin.text(),
            "",
            self.le_AntoineTmax.text(),
        )

        db.cursor.execute(query, items)
        self.substance_added = True
        self.close()

    def isFloat(self, s):
        try:
            float(s)
            return True
        except ValueError:
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
