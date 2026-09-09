# pylint: disable=no-name-in-module
import sys

from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QAction, QKeySequence
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
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

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
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)

        self.config_widget = config_widget(self.centralWidget, self.config)
        self.config_widget.setSizePolicy(sizePolicy)
        self.gridLayout_2.addWidget(
            self.config_widget, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.setCentralWidget(self.centralWidget)

        self.menuBar: QMenuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 800, 29))
        self.menuBar.setObjectName("menuBar")
        self.setMenuBar(self.menuBar)

        self.menuFile: QMenu = QMenu(self.menuBar)
        self.menuFile.setTitle("File")
        self.menuFile.setObjectName("menuFile")

        self.exitAction: QAction = QAction(
            parent=self,
            icon=getIcon("close.svg"),
            shortcut=QKeySequence(Qt.Key.Key_Control | Qt.Key.Key_X),
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
            icon=getIcon("library_add.svg"),
            shortcut=QKeySequence(Qt.Key.Key_Control | Qt.Key.Key_Q),
        )
        self.showQuickstartAction.setText("&Quickstart")
        self.showQuickstartAction.setObjectName("quickstartAction")
        self.showQuickstartAction.triggered.connect(showQuickstartWindow)
        self.menuHelp.addAction(self.showQuickstartAction)

        self.showAboutAction: QAction = QAction(
            parent=self,
            icon=getIcon("about.svg"),
            shortcut=QKeySequence(Qt.Key.Key_Control | Qt.Key.Key_A),
        )
        self.showAboutAction.setText("&About")
        self.showAboutAction.setObjectName("aboutAction")
        self.showAboutAction.triggered.connect(showAboutWindow)
        self.menuHelp.addAction(self.showAboutAction)

        self.menuBar.addAction(self.menuHelp.menuAction())

        self.setWindowTitle("Configuration")
