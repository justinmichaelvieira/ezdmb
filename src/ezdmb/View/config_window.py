# pylint: disable=no-name-in-module
import sys

from PySide6.QtCore import QRect, QSize, Qt
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

        self.centralWidget = QWidget(self)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        # sizePolicy.setHeightForWidth(
        #     self.centralWidget.sizePolicy().hasHeightForWidth()
        # )
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setMinimumSize(QSize(800, 240))
        self.centralWidget.setObjectName("centralWidget")

        self.gridLayout_2 = QGridLayout(self.centralWidget)
        self.gridLayout_2.setContentsMargins(11, 0, 11, 0)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)

        self.config_widget = config_widget(self.centralWidget, self.config)
        self.config_widget.setSizePolicy(sizePolicy)
        self.gridLayout_2.addWidget(self.config_widget, 0, 0, 1, 1, alignment=Qt.AlignTop)
        self.setCentralWidget(self.centralWidget)

        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 800, 29))
        self.menuBar.setObjectName("menuBar")
        self.setMenuBar(self.menuBar)

        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setTitle("File")
        self.menuFile.setObjectName("menuFile")

        self.exitAction = QAction(
            self, icon=getIcon("close.svg"), shortcut=Qt.CTRL | Qt.Key_X
        )
        self.exitAction.setText("E&xit")
        self.exitAction.setObjectName("exitAction")
        self.exitAction.triggered.connect(lambda: sys.exit())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.exitAction)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setTitle("Help")
        self.menuHelp.setObjectName("menuHelp")

        self.showQuickstartAction = QAction(
            self, icon=getIcon("library_add.svg"), shortcut=Qt.CTRL | Qt.Key_Q
        )
        self.showQuickstartAction.setText("&Quickstart")
        self.showQuickstartAction.setObjectName("quickstartAction")
        self.showQuickstartAction.triggered.connect(showQuickstartWindow)
        self.menuHelp.addAction(self.showQuickstartAction)

        self.showAboutAction = QAction(
            self, icon=getIcon("about.svg"), shortcut=Qt.CTRL | Qt.Key_A
        )
        self.showAboutAction.setText("&About")
        self.showAboutAction.setObjectName("aboutAction")
        self.showAboutAction.triggered.connect(showAboutWindow)
        self.menuHelp.addAction(self.showAboutAction)

        self.menuBar.addAction(self.menuHelp.menuAction())

        self.setWindowTitle("Configuration")
