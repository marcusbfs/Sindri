import numpy as np
from PySide2 import QtCore, QtWidgets

from ui.binary_interaction_parameters_ui import Ui_FormBinaryParameters


class Window_BinaryInteractionParameters(QtWidgets.QWidget, Ui_FormBinaryParameters):
    return_k = QtCore.Signal(np.ndarray)

    def __init__(self, c, f, k, parent=None):
        super(Window_BinaryInteractionParameters, self).__init__(parent)
        self.setupUi(self)

        self.btn_ok.clicked.connect(self.clicked_ok)
        self.btn_cancel.clicked.connect(self.clicked_cancel)

        self.comps = c
        self.formulas = f
        self.n = len(c)

        self.k = k

        self.labels = self.formulas

        self.tableWidget_BinaryParameters.setRowCount(self.n)
        self.tableWidget_BinaryParameters.setColumnCount(self.n)

        self.tableWidget_BinaryParameters.setHorizontalHeaderLabels(self.formulas)
        self.tableWidget_BinaryParameters.setVerticalHeaderLabels(self.labels)

        self._displayK()

    def _displayK(self):
        for i in range(self.n):
            for j in range(self.n):
                self.tableWidget_BinaryParameters.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(self.k[i][j]))
                )

    def clicked_ok(self):
        for i in range(self.n):
            for j in range(self.n):
                try:
                    v = float(self.tableWidget_BinaryParameters.item(i, j).text())
                    tmp = v * 1.0 + 1.0
                    self.k[i][j] = v
                except:
                    continue

        self._return_k_and_close()

    def clicked_cancel(self):
        self._return_k_and_close()

    def _return_k_and_close(self):
        self.return_k.emit(self.k)
        self.close()
