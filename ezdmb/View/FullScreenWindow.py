from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QWidget, QFrame, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap

from ezdmb.Utility.ShortcutUtility import setEscKey
from ezdmb.View import MenuContentViewUtility


class FullScreenWindow(QMainWindow):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.contentViewUtil = MenuContentViewUtility.MenuContentViewUtility(
            config.ContentArray,
            config.RotateContent,
            config.RotateContentTime,
            self.contentLbl,
            "FullScreenWindow",
            self.onRefresh,
        )
        setEscKey(self)

    @pyqtSlot(QPixmap)
    def onRefresh(self, value):
        self.contentLbl.setPixmap(value)

    def setupUi(self, FullScreenWindow):
        FullScreenWindow.setObjectName("FullScreenWindow")
        FullScreenWindow.setWindowModality(Qt.WindowModal)
        FullScreenWindow.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        FullScreenWindow.setSizePolicy(sizePolicy)
        FullScreenWindow.setMinimumSize(QSize(200, 200))
        FullScreenWindow.setAutoFillBackground(True)
        self.centralwidget = QWidget(FullScreenWindow)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.contentLbl = QLabel(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.contentLbl.setSizePolicy(sizePolicy)
        self.contentLbl.setFrameShape(QFrame.NoFrame)
        self.contentLbl.setLineWidth(0)
        self.contentLbl.setTextFormat(Qt.RichText)
        self.contentLbl.setScaledContents(True)
        self.contentLbl.setObjectName("contentLbl")
        self.gridLayout_2.addWidget(self.contentLbl, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        FullScreenWindow.setCentralWidget(self.centralwidget)
        FullScreenWindow.setWindowTitle("Menu")
