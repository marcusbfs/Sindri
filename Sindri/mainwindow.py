from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Slot

import _devinfo
import db
from Controllers.MixtureCalculationsController import MixtureCalculationsController
from Controllers.PureSubstanceController import PureSubstanceController
from Models.MixtureModel import MixtureModel
from Models.PureSubstanceModel import PureSubstanceModel
from aboutWindow import Window_About
from databaseWindow import databaseWindow
from ui.mainwindow_ui import Ui_MainWindow
import resources.icons_rc


class mainwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.setupUi(self)
        self.dbw = databaseWindow()
        self.btn_PureSubstanceCalculations.clicked.connect(
            self.open_PureSubstanceCalculations
        )

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/images/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.setWindowIcon(icon)

        # self.setFixedSize(300, 340)

        self.btn_MixtureCalculations.clicked.connect(self.open_MixtureCalculations)
        self.btn_about.clicked.connect(self.open_AboutWindow)
        self.setWindowTitle(_devinfo.__SOFTWARE_NAME__ + " - Jump Start")

        main_logo_pixmap = QtGui.QPixmap(":/images/main_logo.png")
        self.main_logo_pixmap = main_logo_pixmap.scaledToWidth(54)

        self.label_software_version.setText("v" + _devinfo.__SOFTWARE_VERSION__)

        self.label_main_title.setStyleSheet(
            "font-weight: bold;font-size: 20px;font-family: Dubai;"
        )
        self.label_main_subtitle.setStyleSheet("font-size: 16px; font-family: Calibri;")

        # button icons
        self.btn_BancoDeDados.setIcon(
            QtGui.QIcon(QtGui.QPixmap(":/images/database_button.png"))
        )
        self.btn_about.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/about_button.png")))
        self.btn_PureSubstanceCalculations.setIcon(
            QtGui.QIcon(QtGui.QPixmap(":/images/pureSubstance_button.png"))
        )
        self.btn_MixtureCalculations.setIcon(
            QtGui.QIcon(QtGui.QPixmap(":/images/mixture_button.png"))
        )

        # Carrega foto "screenshot/database"
        self._SS_database = QtGui.QPixmap(":/images/screenshots/database.png")

        # Habilita mouseTrackingHover para os botões
        self.btn_BancoDeDados.installEventFilter(self)
        self.btn_MixtureCalculations.installEventFilter(self)
        self.btn_PureSubstanceCalculations.installEventFilter(self)
        self.btn_about.installEventFilter(self)

        # Lê arquivo html do texto "about"
        abouthtml = "texts/about.html"
        with open(abouthtml, "r") as aboutContent:
            self.textBrowser_about.setHtml(aboutContent.read())

        # Remover bordas dos frames
        self.frame_info.setStyleSheet("border: 0;")

        # Breves informações sobre os botões
        # <editor-fold desc = "buttons_info">
        self._database_information = "Add/edit substances in the database."
        # </editor-fold>

        # Seta informações principais do software
        self._initSindriMainInfo()

        # Mostra informações principais
        self._setupSindriMainInfo()


    def open_db_window(self):
        self.dbw.show()

    def eventFilter(self, sender: QtCore.QObject, event):
        """
        Filtra os eventos da janela principal.
        Parameters
        ----------
        sender: Objeto que emite o evento
        event: Evento que acontece
        """
        # Está passando mouse em cima do botão "database"?
        if event.type() == QtCore.QEvent.Enter and sender is self.btn_BancoDeDados:
            self._setupDatabaseMouseHover()
            return True

        # Tirou o mouse do botão database
        if event.type() == QtCore.QEvent.Leave and sender is self.btn_BancoDeDados:
            self._setupSindriMainInfo()
            return True

        # Tirou o mouse acima do botão "about"
        if event.type() == QtCore.QEvent.Leave and sender is self.btn_about:
            self._setupSindriMainInfo()
            return True

        # Colocou o mouse acima do botão "about"
        if event.type() == QtCore.QEvent.Enter and sender is self.btn_about:
            self._setupAboutMouseHover()
            return True

        return False

    def _setupSindriMainInfo(self):
        """
        Mostra informações principais do programa no frame "Info"
        """
        # Desabilita "about" textBrowser
        self.textBrowser_about.setVisible(False)

        # Deixa "button_info" invisível
        self.label_buttonInfo.setVisible(False)

        # Deixa SS image invisível
        self.label_SS_image.setVisible(False)

        # Coloca informações gerais visíveis
        self._enableSindriMainInfo()

    def _initSindriMainInfo(self):
        # Adiciona logo principal
        self.label_main_icon.setPixmap(self.main_logo_pixmap)

        # Informa nome do Software
        self.label_main_title.setText(_devinfo.__SOFTWARE_NAME__)

        # Descrição geral do software
        self.label_main_subtitle.setText(_devinfo.__SOFTWARE_INFO__)

        # Habilita labels de informações principais
        self._enableSindriMainInfo()

    def _setupDatabaseMouseHover(self):
        """
        Função executada ao passar o mouse sob o botão "Database"
        """
        # Desabilita labels de informações principais
        self._disableSindriMainInfo()

        # Desabilita "about" textBrowser
        self.textBrowser_about.setVisible(False)

        # Deixa button_info visível
        self.label_buttonInfo.setVisible(True)

        # Deixa SS image visível
        self.label_SS_image.setVisible(True)

        # Coloca texto correto no label
        self.label_buttonInfo.setText(self._database_information)

        frame_width = 200
        frame_height = self.frame_info.height()

        # Coloca imagem de fundo
        self.label_SS_image.setPixmap(self._SS_database.scaledToWidth(frame_width))

    def _setupAboutMouseHover(self):
        """
        Função executada ao passar o mouse sob o botão "About"
        """

        # Deixa invísivel informações principais
        self._disableSindriMainInfo()

        # Deixa invisível button info
        self.label_buttonInfo.setVisible(False)

        # Deixa SS image invisível
        self.label_SS_image.setVisible(False)

        # Deixa visível about textbrowser
        self.textBrowser_about.setVisible(True)

    def _enableSindriMainInfo(self):
        """
        Habilita os labels para mostrar informações principais
        """
        # Habilita labels utilizadas
        self.label_main_subtitle.setVisible(True)
        self.label_main_icon.setVisible(True)
        self.label_main_title.setVisible(True)

    def _disableSindriMainInfo(self):
        """
        Desabilita os labels para mostrar informações principais
        """
        # Desabilita labels utilizadas
        self.label_main_subtitle.setVisible(False)
        self.label_main_icon.setVisible(False)
        self.label_main_title.setVisible(False)

    @Slot()
    def open_PureSubstanceCalculations(self):
        self.pureSubstanceController = PureSubstanceController(PureSubstanceModel())
        self.pureSubstanceController.createMainView()

    @Slot()
    def open_MixtureCalculations(self):
        self.mixtureCalculationsController = MixtureCalculationsController(
            MixtureModel()
        )
        self.mixtureCalculationsController.createMixtureCalcView()

    @Slot()
    def open_AboutWindow(self):
        self.aboutWin = Window_About()
        self.aboutWin.show()

    def closeEvent(self, *args, **kwargs):
        db.db.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())
