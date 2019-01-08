from PyQt5 import QtCore, QtGui, QtWidgets
from ui.db_substanceProperties_ui import Ui_Form_db_substanceProperties


class Form_SubstanceProperties(QtWidgets.QWidget, Ui_Form_db_substanceProperties):
    def __init__(self, parent=None):
        super(Form_SubstanceProperties, self).__init__(parent)
        self.setupUi(self)




