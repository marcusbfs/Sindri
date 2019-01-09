from PyQt5 import QtCore, QtGui, QtWidgets
from ui.db_substanceProperties_ui import Ui_Form_db_substanceProperties


class Form_EditSubstanceProperties(QtWidgets.QWidget, Ui_Form_db_substanceProperties):
    def __init__(self, hl_row=None, parent=None):
        super(Form_EditSubstanceProperties, self).__init__(parent)
        self.setupUi(self)

        self.hl_row = hl_row

        self.le_formula.setText(str(self.hl_row[0]))
        self.le_name.setText(str(self.hl_row[1]))
        self.le_CAS.setText(str(self.hl_row[2]))

    # def get_hl_row(self, hl_row):




