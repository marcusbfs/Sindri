from PySide2 import QtWidgets

from ui.db_addUNIFACsubgroup_ui import Ui_Form_addUNIFACsubgroup


class AddUNIFACsubgroupView(QtWidgets.QWidget, Ui_Form_addUNIFACsubgroup):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        from Controllers.AddUNIFACsubgroupController import AddUNIFACsubgroupController

        self.controller: AddUNIFACsubgroupController = controller

        self.btn_addUNIFACsubgroup_confirm.clicked.connect(self.ok_clicked)
        self.btn_addUNIFACsubgroup_cancel.clicked.connect(self.cancel_clicked)

    def ok_clicked(self):
        self.controller.ok_clicked()

    def cancel_clicked(self):
        self.controller.cancel_clicked()
