from PySide2 import QtCore, QtGui, QtWidgets
from ui.db_substanceProperties_ui import Ui_Form_db_substanceProperties


class Form_EditSubstanceProperties(QtWidgets.QWidget, Ui_Form_db_substanceProperties):
    def __init__(self, parent=None, hl_row=None):
        super(Form_EditSubstanceProperties, self).__init__(parent)
        self.setupUi(self)

        self.hl_row = hl_row
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        self.setWindowTitle("Edit substance - " + str(self.hl_row[1]))
        self.load_entries()

    def load_entries(self):
        self.le_formula.setText(str(self.hl_row[0]))
        self.le_name.setText(str(self.hl_row[1]))
        self.le_CAS.setText(str(self.hl_row[2]))
        self.le_MM.setText(str(self.hl_row[3]))
        self.le_Tfp.setText(str(self.hl_row[4]))
        self.le_Tb.setText(str(self.hl_row[5]))
        self.le_Tc.setText(str(self.hl_row[6]))
        self.le_Pc.setText(str(self.hl_row[7]))
        self.le_Vc.setText(str(self.hl_row[8]))
        self.le_Zc.setText(str(self.hl_row[9]))
        self.le_omega.setText(str(self.hl_row[10]))

        r = self.extract_Cp_Tminmax(self.hl_row[11])
        self.le_CpTmin.setText(r[0])
        self.le_CpTmax.setText(r[1])
        self.le_a0.setText(self.hl_row[12])
        self.le_a1.setText(self.hl_row[13])
        self.le_a2.setText(self.hl_row[14])
        self.le_a3.setText(self.hl_row[15])
        self.le_a4.setText(self.hl_row[16])

        self.le_AntoineA.setText((self.hl_row[19]))
        self.le_AntoineB.setText((self.hl_row[20]))
        self.le_AntoineC.setText((self.hl_row[21]))
        self.le_AntoineTmin.setText((self.hl_row[23]))
        self.le_AntoineTmax.setText((self.hl_row[25]))

    def extract_Cp_Tminmax(self, s):
        if '-' in s:
            return s.split('-')
        else:
            return ["", ""]

    def edit_confirm(self):
        pass

    def edit_cancel(self):
        self.close()
