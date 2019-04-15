from PySide2 import QtCore, QtWidgets, QtGui

from Models.PureSubstanceModel import PureSubstanceModel
from ui.pure_substance_diagrams_ui import Ui_Form_PureSubstanceDiagrams


class PureSubstanceDiagramsView(QtWidgets.QWidget, Ui_Form_PureSubstanceDiagrams):
    def __init__(
        self,
        # controller: PureSubstanceController,
        controller,
        model: PureSubstanceModel,
        parent=None,
    ):
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

        self.points = 30
        self.data_is_gen = False
        self.le_points.setText(str(self.points))
        # self.le_isotherms.setText("120 150 190")  # TODO remove this line after testing

        # connections
        # self.le_Ti.textChanged.connect(self.changed_Trange)
        # self.le_points.textChanged.connect(self.changed_Trange)
        # self.le_isotherms.textChanged.connect(self.changed_Trange)
        self.btn_gen.clicked.connect(self.gen)
        self.btn_plot.clicked.connect(self.plot)
        self.comboBox_diagram.currentTextChanged.connect(self.update_axis)
        self.checkBox_isotherms.stateChanged.connect(self.isothermsStateChanged)

        # set initial and final temperatures to freezing and critical point

        self.Ti = 0
        self.Tf = 1

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
    def changed_Trange(self):
        self.data_is_gen = False

    @QtCore.Slot()
    def isothermsStateChanged(self, state):
        self.controller.diagrams_isothermStateChanged(state)

    def initialTrange(self, Ti=None, Tf=None):
        if Ti is not None:
            self.le_Ti.setText(str(Ti))
        if Tf is not None:
            self.le_Tf.setText(str(Tf))
