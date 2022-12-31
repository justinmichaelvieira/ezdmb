from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QWidget, QFrame, QLabel, QGridLayout

from ezdmb.Utility.ShortcutUtility import setEscKey
from ezdmb.View import HtmlViewUtility


class FullScreenWindow(QMainWindow):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.htmlUtil = HtmlViewUtility.HtmlViewUtility(
            config.ContentArray,
            config.RotateContent,
            config.RotateContentTime,
            self.htmlContent,
            self.onRefresh,
        )
        setEscKey(self)

    @pyqtSlot(str)
    def onRefresh(self, value):
        self.htmlContent.setText(value)

    def setupUi(self, FullScreenWindow):
        FullScreenWindow.setObjectName("FullScreenWindow")
        FullScreenWindow.setWindowModality(Qt.WindowModal)
        FullScreenWindow.setEnabled(True)
        FullScreenWindow.resize(202, 202)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FullScreenWindow.sizePolicy().hasHeightForWidth())
        FullScreenWindow.setSizePolicy(sizePolicy)
        FullScreenWindow.setMinimumSize(QSize(200, 200))
        FullScreenWindow.setAutoFillBackground(True)
        self.centralwidget = QWidget(FullScreenWindow)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.htmlContent = QLabel(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.htmlContent.sizePolicy().hasHeightForWidth())
        self.htmlContent.setSizePolicy(sizePolicy)
        self.htmlContent.setFrameShape(QFrame.NoFrame)
        self.htmlContent.setLineWidth(0)
        self.htmlContent.setTextFormat(Qt.RichText)
        self.htmlContent.setScaledContents(True)
        self.htmlContent.setObjectName("htmlContent")
        self.gridLayout_2.addWidget(self.htmlContent, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        FullScreenWindow.setCentralWidget(self.centralwidget)
        FullScreenWindow.setWindowTitle("Menu")
