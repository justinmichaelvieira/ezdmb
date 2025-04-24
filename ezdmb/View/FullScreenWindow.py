from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QWidget, QFrame, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap

from ezdmb.Utility.ShortcutUtility import setCloseOnEscKey, setOpenOnOKey
from ezdmb.View import MenuContentViewUtility
from ezdmb.Controller.Configuration import Configuration


class FullScreenWindow(QMainWindow):
    def __init__(self, config: Configuration, reopenPreviewWindow):
        super(self.__class__, self).__init__()
        self._config = config

        self.setObjectName("FullScreenWindow")
        self.setWindowModality(Qt.WindowModal)
        self.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(200, 200))
        self.setAutoFillBackground(True)
        self.centralwidget = QWidget(self)
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
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("Menu")

        self.contentViewUtil = MenuContentViewUtility.MenuContentViewUtility(
            self._config,
            self.contentLbl,
            "FullScreenWindow",
            self.onRefresh,
        )
        setCloseOnEscKey(self)
        setOpenOnOKey(self, reopenPreviewWindow)

    @pyqtSlot(QPixmap)
    def onRefresh(self, value):
        self.contentLbl.setPixmap(value)
