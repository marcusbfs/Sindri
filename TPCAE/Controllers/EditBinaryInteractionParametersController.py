from Views.EditBinaryInteractionParametersView import (
    EditBinaryInteractionParametersView,
)
from Models.MixtureModel import MixtureModel
from PySide2 import QtWidgets


class EditBinaryInteractionParametersController:
    def __init__(self, model: MixtureModel):

        self.binInteractionObservers = []

        self.model = model
        self.binInteractionView = EditBinaryInteractionParametersView(self)

    def createBinInteractionView(self):

        self.n = self.model.getNumberOfSubstancesInSystem()
        self.k = self.model.getBinaryInteractionsParameters()

        formulas = []
        for i in range(self.n):
            formulas.append(self.model.getSubstancesInSystems()[i].Formula)

        self.binInteractionView.tableWidget_BinaryParameters.setRowCount(self.n)
        self.binInteractionView.tableWidget_BinaryParameters.setColumnCount(self.n)
        self.binInteractionView.tableWidget_BinaryParameters.setHorizontalHeaderLabels(
            formulas
        )
        self.binInteractionView.tableWidget_BinaryParameters.setVerticalHeaderLabels(
            formulas
        )

        for i in range(self.n):
            for j in range(self.n):
                self.binInteractionView.tableWidget_BinaryParameters.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(self.k[i][j]))
                )
        self.binInteractionView.show()

    def okClicked(self):
        for i in range(self.n):
            for j in range(self.n):
                try:
                    v = float(
                        self.binInteractionView.tableWidget_BinaryParameters.item(
                            i, j
                        ).text()
                    )
                    tmp = v * 1.0 + 1.0
                    self.k[i][j] = v
                except:
                    continue
        self.notifyBinInteractionObservers()
        self.binInteractionView.close()

    def cancelClicked(self):
        self.binInteractionView.close()

    def registerBinInteractionObserver(self, o):
        self.binInteractionObservers.append(o)

    def notifyBinInteractionObservers(self):
        for o in self.binInteractionObservers:
            o.updateBinInteraction()

    def getK(self):
        return self.k

    def setZeroClicked(self):
        for i in range(self.n):
            for j in range(self.n):
                self.binInteractionView.tableWidget_BinaryParameters.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str("0.0"))
                )
