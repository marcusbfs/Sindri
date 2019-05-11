from PySide2 import QtCore, QtWidgets, QtGui

from Models.PureSubstanceModel import PureSubstanceModel
from ui.pure_substance_diagrams_ui import Ui_Form_PureSubstanceDiagrams


class PureSubstanceDiagramsView(QtWidgets.QWidget, Ui_Form_PureSubstanceDiagrams):
    def __init__(self, controller, model: PureSubstanceModel, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/images/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.setWindowIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/images/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.setWindowIcon(icon)

        self.model = model
        from Controllers.PureSubstanceController import PureSubstanceController

        self.controller: PureSubstanceController = controller

        self.checkBox_smooth.setChecked(True)
        self.checkBox_grid.setChecked(True)

        # validators
        from validators import getDoubleValidatorRegex, getPositiveIntValidator

        doublevalidator = getDoubleValidatorRegex(self)
        positiveIntvalidator = getPositiveIntValidator()
        self.le_Tf.setValidator(doublevalidator)
        self.le_Ti.setValidator(doublevalidator)
        self.le_points.setValidator(positiveIntvalidator)

        self.points = 20
        self.data_is_gen = False
        self.le_points.setText(str(self.points))

        # connections
        self.btn_gen.clicked.connect(self.gen)
        self.btn_plot.clicked.connect(self.plot)
        self.comboBox_diagram.currentTextChanged.connect(self.update_axis)
        self.comboBox_diagram.currentTextChanged.connect(self.comboBox_diagram_changed)
        self.checkBox_isotherms.stateChanged.connect(self.isothermsStateChanged)

    @QtCore.Slot()
    def gen(self):
        self.controller.genDiagrams()

    @QtCore.Slot()
    def plot(self):
        self.controller.plotDiagrams()

    @QtCore.Slot()
    def update_axis(self):
        self.controller.updateAxisDiagrams()

    @QtCore.Slot()
    def comboBox_diagram_changed(self, state):
        self.controller.diagram_combobox_changed()

    @QtCore.Slot()
    def isothermsStateChanged(self, state):
        self.controller.diagrams_isothermStateChanged(state)

    def initialTrange(self, Ti=None, Tf=None):
        if Ti is not None:
            self.le_Ti.setText(str(Ti))
        if Tf is not None:
            self.le_Tf.setText(str(Tf))
