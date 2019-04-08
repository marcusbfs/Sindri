import numpy as np
from PySide2 import QtCore, QtWidgets

from ui.binary_interaction_parameters_ui import Ui_FormBinaryParameters


class EditBinaryInteractionParametersView(QtWidgets.QWidget, Ui_FormBinaryParameters):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        from Controllers.EditBinaryInteractionParametersController import (
            EditBinaryInteractionParametersController,
        )

        self.controller: EditBinaryInteractionParametersController = controller

        self.btn_ok.clicked.connect(self.clicked_ok)
        self.btn_cancel.clicked.connect(self.clicked_cancel)

    def clicked_ok(self):
        self.controller.okClicked()

    def clicked_cancel(self):
        self.controller.cancelClicked()
