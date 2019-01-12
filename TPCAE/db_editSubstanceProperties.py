from PySide2 import QtCore, QtWidgets
from ui.db_substanceProperties_ui import Ui_Form_db_substanceProperties
import db


class Form_EditSubstanceProperties(QtWidgets.QWidget, Ui_Form_db_substanceProperties):
    signal_changes_made = QtCore.Signal(bool)

    def __init__(self, parent=None, hl_row=None):
        super(Form_EditSubstanceProperties, self).__init__(parent)
        self.setupUi(self)

        self.hl_row = hl_row
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.changes_made = False

        # Connect buttons
        self.connect(self.le_name, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_formula, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_CAS, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_MM, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_Tfp, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_Tb, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_Tc, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_Pc, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_Vc, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_Zc, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_omega, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_a0, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_a1, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_a2, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_a3, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_a4, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_CpTmin, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_CpTmax, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_AntoineA, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_AntoineB, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_AntoineC, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_AntoineTmin, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)
        self.connect(self.le_AntoineTmax, QtCore.SIGNAL("textChanged(QString)"), self.lineEdit_changed)

        self.Formula = self.hl_row[0]
        self.Name = self.hl_row[1]
        self.CAS = self.hl_row[2]
        self.MM = self.hl_row[3]
        self.Tfp = self.hl_row[4]
        self.Tb = self.hl_row[5]
        self.Tc = self.hl_row[6]
        self.Pc = self.hl_row[7]
        self.Vc = self.hl_row[8]
        self.Zc = self.hl_row[9]
        self.omega = self.hl_row[10]

        self.r = self.extract_Cp_Tminmax(self.hl_row[11])
        self.CpTmin = self.r[0]
        self.CpTmax = self.r[1]
        self.a0 = self.hl_row[12]
        self.a1 = self.hl_row[13]
        self.a2 = self.hl_row[14]
        self.a3 = self.hl_row[15]
        self.a4 = self.hl_row[16]

        self.AntoineA = self.hl_row[19]
        self.AntoineB = self.hl_row[20]
        self.AntoineC = self.hl_row[21]
        self.AntoineTmin = self.hl_row[23]
        self.AntoineTmax = self.hl_row[25]

        self.setWindowTitle("Edit substance - " + str(self.Name))

        self.columnHeaders = ['Formula', 'Name', '`CAS #`', '`Mol. Wt.`', '`Tfp, K`', '`Tb, K`', '`Tc, K`', '`Pc, bar`',
                              '`Vc, cm3/mol`', '`Zc = PcVc/RTc`', 'Omega', '`Trange, K`', 'a0', 'a1', 'a2', 'a3', 'a4',
                              'CpIG', 'Cpliq', 'ANTOINE_A', 'ANTOINE_B', 'ANTOINE_C', '`Pvpmin, bar`', '`Tmin, K`',
                              '`Pvpmax, bar`', '`Tmax, K`']
        self.colLen = len(self.columnHeaders)

        self.load_entries()

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
        if '-' in s:
            return s.split('-')
        else:
            return ["", ""]

    def confirm_clicked(self):
        if self.changes_made:

            edit_confirm_msg = "Save editions?"
            choice = QtWidgets.QMessageBox.question(self, "Saving changes",
                                                    edit_confirm_msg,
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)

            if choice == QtWidgets.QMessageBox.Yes:
                query_WHERE = " WHERE Formula LIKE '%" + self.Formula + "%'" + \
                              " AND Name LIKE '%" + self.Name + "%'" + \
                              " AND `CAS #` LIKE '%" + self.CAS + "%'"

                query_ID = "UPDATE database SET " + self.columnHeaders[0] + " = '" + self.le_formula.text() + "'" + \
                           ", " + self.columnHeaders[1] + " = '" + self.le_name.text() + "'" + \
                           ", " + self.columnHeaders[2] + " = '" + self.le_CAS.text() + "'" + \
                           query_WHERE

                query_GENERAL = "update database set " + self.columnHeaders[3] + "='" + self.le_MM.text() + "'" + \
                                ", " + self.columnHeaders[4] + " = '" + self.le_Tfp.text() + "'" + \
                                ", " + self.columnHeaders[5] + " = '" + self.le_Tb.text() + "'" + \
                                ", " + self.columnHeaders[6] + " = '" + self.le_Tc.text() + "'" + \
                                ", " + self.columnHeaders[7] + " = '" + self.le_Pc.text() + "'" + \
                                ", " + self.columnHeaders[8] + " = '" + self.le_Vc.text() + "'" + \
                                ", " + self.columnHeaders[9] + " = '" + self.le_Zc.text() + "'" + \
                                ", " + self.columnHeaders[10] + " = '" + self.le_omega.text() + "'" + \
                                query_WHERE

                if self.isFloat(self.le_CpTmin.text()) and self.isFloat(self.le_CpTmax.text()):
                    Trange = self.le_CpTmin.text() + "-" + self.le_CpTmax.text()
                else:
                    Trange = ""

                query_CP = "update database set " + self.columnHeaders[11] + "='" + Trange + "'" + \
                           ", " + self.columnHeaders[12] + " = '" + self.le_a0.text() + "'" + \
                           ", " + self.columnHeaders[13] + " = '" + self.le_a1.text() + "'" + \
                           ", " + self.columnHeaders[14] + " = '" + self.le_a2.text() + "'" + \
                           ", " + self.columnHeaders[15] + " = '" + self.le_a3.text() + "'" + \
                           ", " + self.columnHeaders[16] + " = '" + self.le_a4.text() + "'" + \
                           query_WHERE

                query_ANTOINE = "update database set " + self.columnHeaders[19] + "='" + self.le_AntoineA.text() + "'" + \
                                ", " + self.columnHeaders[20] + " = '" + self.le_AntoineB.text() + "'" + \
                                ", " + self.columnHeaders[21] + " = '" + self.le_AntoineC.text() + "'" + \
                                ", " + self.columnHeaders[23] + " = '" + self.le_AntoineTmin.text() + "'" + \
                                ", " + self.columnHeaders[25] + " = '" + self.le_AntoineTmax.text() + "'" + \
                                query_WHERE

                try:
                    db.cursor.execute(query_ID)
                    db.cursor.execute(query_GENERAL)
                    db.cursor.execute(query_CP)
                    db.cursor.execute(query_ANTOINE)
                    self.close()
                except:
                    msg = QtWidgets.QMessageBox.about(self, "Error", "Could not save changes")

    def isFloat(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def lineEdit_changed(self):
        self.changes_made = True

    def cancel_clicked(self):
        self.changes_made = False
        self.close()

    def closeEvent(self, QCloseEvent):
        self.signal_changes_made.emit(self.changes_made)
