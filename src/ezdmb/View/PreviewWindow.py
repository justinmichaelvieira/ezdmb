# pylint: disable=no-name-in-module
import sys
from PySide6.QtCore import QSize, Qt, QRect, Slot
from PySide6.QtGui import QFont, QPixmap, QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QSizePolicy,
    QGridLayout,
    QGroupBox,
    QLabel,
    QFrame,
    QLayout,
    QMenuBar,
    QMenu,
    QHBoxLayout,
)

from ezdmb.Utility.IconUtility import getIcon, getWindowIcon
from ezdmb.Utility.ShortcutUtility import setCloseOnEscKey
from ezdmb.View import MenuContentViewUtility


class PreviewWindow(QMainWindow):
    def __init__(self, config, showConfig, showAboutWindow, showQuickstartWindow):
        super(self.__class__, self).__init__()
        self.setupUi(showConfig, showAboutWindow, showQuickstartWindow)
        self.contentUtil = MenuContentViewUtility.MenuContentViewUtility(
            config,
            self.headerLabel,
            "PreviewWindow",
            self.onRefresh,
        )
        setCloseOnEscKey(self)

    @Slot(QPixmap)
    def onRefresh(self, value):
        self.headerLabel.setPixmap(value)

    @Slot(dict)
    def onConfigUpdated(self, data):
        self.contentViewUtil.contentArray = data["imported_content"]
        self.contentViewUtil.rotateContent = data["rotate_content"]
        self.contentViewUtil.rotateTimeout = data["rotate_content_time"]

    def setupUi(self, showConfig, showAboutWindow, showQuickstartWindow):
        self.setObjectName("self")
        self.setWindowIcon(getWindowIcon())
        self.setDocumentMode(False)

        self.centralWidget = QWidget(self)
        sizePolicy = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralWidget.sizePolicy().hasHeightForWidth()
        )
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setMinimumSize(QSize(200, 200))
        self.centralWidget.setStyleSheet("border: 0px;")
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

        self.headerLabel = QLabel(self.centralWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerLabel.sizePolicy().hasHeightForWidth())
        self.headerLabel.setSizePolicy(sizePolicy)
        self.headerLabel.setMinimumSize(QSize(400, 50))

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(32)
        font.setBold(True)
        font.setUnderline(False)
        font.setLegacyWeight(75)
        self.headerLabel.setFont(font)
        self.headerLabel.setFrameShape(QFrame.NoFrame)
        self.headerLabel.setAlignment(Qt.AlignCenter)
        self.headerLabel.setText("Menu Board Preview")
        self.headerLabel.setObjectName("headerLabel")
        self.gridLayout_2.addWidget(self.headerLabel, 1, 0, 1, 1)

        self.currentMenuGroupBox = QGroupBox(self.centralWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.currentMenuGroupBox.sizePolicy().hasHeightForWidth()
        )
        self.currentMenuGroupBox.setSizePolicy(sizePolicy)
        self.currentMenuGroupBox.setMinimumSize(QSize(400, 60))
        self.currentMenuGroupBox.setTitle("")
        self.currentMenuGroupBox.setFlat(True)
        self.currentMenuGroupBox.setObjectName("currentMenuGroupBox")

        self.horizontalLayout = QHBoxLayout(self.currentMenuGroupBox)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 8)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.currentMenuLabel = QLabel(self.currentMenuGroupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(
            self.currentMenuLabel.sizePolicy().hasHeightForWidth()
        )
        self.currentMenuLabel.setSizePolicy(sizePolicy)
        self.currentMenuLabel.setMinimumSize(QSize(60, 40))
        self.currentMenuLabel.setText("Current content:")
        self.currentMenuLabel.setAlignment(Qt.AlignLeft)
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(32)
        font.setBold(True)
        font.setItalic(False)
        font.setLegacyWeight(50)
        self.currentMenuLabel.setFont(font)
        self.currentMenuLabel.setStyleSheet("font-size: 32px; text-align: left; font-weight: bold; vertical-align: text-top;")
        self.currentMenuLabel.setFrameShape(QFrame.NoFrame)
        self.currentMenuLabel.setFrameShadow(QFrame.Plain)
        self.currentMenuLabel.setLineWidth(0)
        self.currentMenuLabel.setScaledContents(True)
        self.currentMenuLabel.setAlignment(Qt.AlignLeft)
        self.currentMenuLabel.setObjectName("currentMenuLabel")
        self.currentMenuLabel.setContentsMargins(0, 0, 0, 20)
        self.horizontalLayout.addWidget(self.currentMenuLabel, alignment=Qt.AlignTop)
        self.horizontalLayout.setStretch(0, 1)

        self.bottomSpacer = QWidget(self.currentMenuGroupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bottomSpacer.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.bottomSpacer)
        self.gridLayout_2.addWidget(self.currentMenuGroupBox, 0, 0, 1, 1, Qt.AlignTop)

        self.setCentralWidget(self.centralWidget)

        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 800, 29))
        self.menuBar.setObjectName("menuBar")
        self.setMenuBar(self.menuBar)

        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setTitle("File")
        self.menuFile.setObjectName("menuFile")

        self.displaySettingsAction = QAction(self, icon=getIcon("settings.svg"), shortcut=Qt.CTRL | Qt.Key_E)
        self.displaySettingsAction.setText("&Display Settings")
        self.displaySettingsAction.setObjectName("displaySettingsAction")
        self.displaySettingsAction.triggered.connect(showConfig)
        self.menuFile.addAction(self.displaySettingsAction)

        self.exitAction = QAction(self, icon=getIcon("close.svg"), shortcut=Qt.CTRL | Qt.Key_X)
        self.exitAction.setText("E&xit")
        self.exitAction.setObjectName("exitAction")
        self.exitAction.triggered.connect(lambda: sys.exit())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.exitAction)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setTitle("Help")
        self.menuHelp.setObjectName("menuHelp")

        self.showQuickstartAction = QAction(self, icon=getIcon("library_add.svg"), shortcut=Qt.CTRL | Qt.Key_Q)
        self.showQuickstartAction.setText("&Quickstart")
        self.showQuickstartAction.setObjectName("quickstartAction")
        self.showQuickstartAction.triggered.connect(showQuickstartWindow)
        self.menuHelp.addAction(self.showQuickstartAction)

        self.showAboutAction = QAction(self, icon=getIcon("about.svg"), shortcut=Qt.CTRL | Qt.Key_A)
        self.showAboutAction.setText("&About")
        self.showAboutAction.setObjectName("aboutAction")
        self.showAboutAction.triggered.connect(showAboutWindow)
        self.menuHelp.addAction(self.showAboutAction)

        self.menuBar.addAction(self.menuHelp.menuAction())

        self.setWindowTitle("Preview / Configuration")
