from PyQt5.QtCore import QSize, Qt, QRect, QMetaObject, pyqtSlot
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
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
    QAction,
    QHBoxLayout,
)

from ezdmb.Utility.ShortcutUtility import setEscKey
from ezdmb.View import MenuContentViewUtility


class MainWindow(QMainWindow):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.contentUtil = MenuContentViewUtility.MenuContentViewUtility(
            config.ContentArray,
            config.RotateContent,
            config.RotateContentTime,
            self.headerLabel,
            "MainWindow",
            self.onRefresh,
        )
        setEscKey(self)

    @pyqtSlot(QPixmap)
    def onRefresh(self, value):
        self.headerLabel.setPixmap(value)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setIconSize(QSize(18, 18))
        MainWindow.setDocumentMode(False)
        self.centralWidget = QWidget(MainWindow)
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
        self.centralWidget.setStyleSheet("")
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
        sizePolicy.setHeightForWidth(
            self.headerLabel.sizePolicy().hasHeightForWidth()
        )
        self.headerLabel.setSizePolicy(sizePolicy)
        self.headerLabel.setMinimumSize(QSize(0, 60))
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.headerLabel.setFont(font)
        self.headerLabel.setFrameShape(QFrame.NoFrame)
        self.headerLabel.setAlignment(Qt.AlignCenter)
        self.headerLabel.setObjectName("headerLabel")
        self.gridLayout_2.addWidget(self.headerLabel, 0, 0, 1, 1)
        self.currentMenuGroupBox = QGroupBox(self.centralWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.currentMenuGroupBox.sizePolicy().hasHeightForWidth()
        )
        self.currentMenuGroupBox.setSizePolicy(sizePolicy)
        self.currentMenuGroupBox.setMinimumSize(QSize(200, 200))
        self.currentMenuGroupBox.setTitle("")
        self.currentMenuGroupBox.setFlat(True)
        self.currentMenuGroupBox.setObjectName("currentMenuGroupBox")
        self.horizontalLayout = QHBoxLayout(self.currentMenuGroupBox)
        self.horizontalLayout.setContentsMargins(4, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.currentMenuLabel = QLabel(self.currentMenuGroupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.currentMenuLabel.sizePolicy().hasHeightForWidth()
        )
        self.currentMenuLabel.setSizePolicy(sizePolicy)
        self.currentMenuLabel.setMinimumSize(QSize(200, 200))
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(64)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(50)
        self.currentMenuLabel.setFont(font)
        self.currentMenuLabel.setStyleSheet("font-size: 96px;text-align: center;")
        self.currentMenuLabel.setFrameShape(QFrame.NoFrame)
        self.currentMenuLabel.setFrameShadow(QFrame.Plain)
        self.currentMenuLabel.setLineWidth(0)
        self.currentMenuLabel.setScaledContents(False)
        self.currentMenuLabel.setObjectName("currentMenuLabel")

        spacerSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.spacerLblLeft = QLabel(self.currentMenuGroupBox)
        self.spacerLblLeft.setSizePolicy(spacerSizePolicy)
        self.spacerLblLeft.setMinimumSize(QSize(300, 200))
        self.horizontalLayout.addWidget(self.spacerLblLeft)
        self.spacerLblRight = QLabel(self.currentMenuGroupBox)
        self.spacerLblRight.setSizePolicy(spacerSizePolicy)
        self.spacerLblRight.setMinimumSize(QSize(300, 200))
        self.horizontalLayout.addWidget(self.currentMenuLabel)
        self.horizontalLayout.addWidget(self.spacerLblRight)
        self.gridLayout_2.addWidget(self.currentMenuGroupBox, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setGeometry(QRect(0, 0, 800, 29))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.editDisplaySettingsAction = QAction(MainWindow)
        self.editDisplaySettingsAction.setObjectName(
            "editDisplaySettingsAction"
        )
        self.exitAction = QAction(MainWindow)
        self.exitAction.setObjectName("exitAction")
        self.menuFile.addAction(self.editDisplaySettingsAction)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.exitAction)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("DMB Configuration")
        self.headerLabel.setText("Digital Menu Board Config")
        self.currentMenuLabel.setText("Current Content")
        self.menuFile.setTitle("File")
        self.editDisplaySettingsAction.setText("Edit Display Settings")
        self.exitAction.setText("Exit")
