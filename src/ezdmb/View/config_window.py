# pylint: disable=no-name-in-module
import sys

from PySide6.QtCore import QRect, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QGridLayout,
    QLayout,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSizePolicy,
    QWidget,
)

from ezdmb.Utility.bundle_utility import export_bundle, import_bundle
from ezdmb.Utility.icon_utility import getIcon, getWindowIcon
from ezdmb.Utility.shortcut_utility import setCloseOnEscKey
from ezdmb.View.config_widget import config_widget


class config_window(QMainWindow):
    def __init__(self, config, showAboutWindow, showQuickstartWindow):
        super(self.__class__, self).__init__()
        self.config = config
        self.setupUi(showAboutWindow, showQuickstartWindow)
        setCloseOnEscKey(self)

    def setupUi(self, showAboutWindow, showQuickstartWindow):
        self.setObjectName("self")
        self.setWindowIcon(getWindowIcon())
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )

        self.centralWidget: QWidget = QWidget(self)
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setMinimumSize(QSize(800, 240))
        self.centralWidget.setObjectName("centralWidget")

        self.gridLayout_2 = QGridLayout(self.centralWidget)
        self.gridLayout_2.setContentsMargins(11, 0, 11, 0)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.config_widget = config_widget(self.centralWidget, self.config)
        self.config_widget.setSizePolicy(sizePolicy)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.addWidget(
            self.config_widget, 0, 0, 1, 1
        )
        self.setCentralWidget(self.centralWidget)

        self.menuBar: QMenuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 800, 29))
        self.menuBar.setObjectName("menuBar")
        self.setMenuBar(self.menuBar)

        self.menuFile: QMenu = QMenu(self.menuBar)
        self.menuFile.setTitle("File")
        self.menuFile.setObjectName("menuFile")

        self.exportBundleAction: QAction = QAction(
            parent=self,
            icon=getIcon("export.svg"),
        )
        self.exportBundleAction.setText("&Export Content Bundle")
        self.exportBundleAction.setObjectName("exportBundleAction")
        self.exportBundleAction.triggered.connect(lambda: export_bundle(self.config))
        self.menuFile.addAction(self.exportBundleAction)

        self.importBundleAction: QAction = QAction(
            parent=self,
            icon=getIcon("import.svg"),
        )
        self.importBundleAction.setText("&Import Content Bundle")
        self.importBundleAction.setObjectName("importBundleAction")
        self.importBundleAction.triggered.connect(lambda: import_bundle(self.config))
        self.menuFile.addAction(self.importBundleAction)

        self.exitAction: QAction = QAction(
            parent=self,
            icon=getIcon("close.svg"),
        )
        self.exitAction.setText("E&xit")
        self.exitAction.setObjectName("exitAction")
        self.exitAction.triggered.connect(lambda: sys.exit())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.exitAction)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.menuHelp: QMenu = QMenu(self.menuBar)
        self.menuHelp.setTitle("Help")
        self.menuHelp.setObjectName("menuHelp")

        self.showQuickstartAction: QAction = QAction(
            parent=self,
            icon=getIcon("quickstart.svg"),
        )
        self.showQuickstartAction.setText("&Quickstart")
        self.showQuickstartAction.setObjectName("quickstartAction")
        self.showQuickstartAction.triggered.connect(showQuickstartWindow)
        self.menuHelp.addAction(self.showQuickstartAction)

        self.showAboutAction: QAction = QAction(
            parent=self,
            icon=getIcon("about.svg"),
        )
        self.showAboutAction.setText("&About")
        self.showAboutAction.setObjectName("aboutAction")
        self.showAboutAction.triggered.connect(showAboutWindow)
        self.menuHelp.addAction(self.showAboutAction)
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.setWindowTitle("Configuration")
