from PySide2 import QtWidgets

from ui.db_addAlias_ui import Ui_Form_AddAlias


class AddAliasView(QtWidgets.QWidget, Ui_Form_AddAlias):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        from Controllers.AddAliasController import AddAliasController

        self.controller: AddAliasController = controller

        self.btn_ok.clicked.connect(self.ok_clicked)
        self.btn_cancel.clicked.connect(self.cancel_clicked)

    def ok_clicked(self):
        self.controller.ok_clicked()

    def cancel_clicked(self):
        self.controller.cancel_clicked()
