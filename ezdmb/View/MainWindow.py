from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QTextBrowser
from ezdmb.Utility.ShortcutUtility import setEscKey

from ezdmb.View.generated.mainwindow_ui import Ui_MainWindow
from ezdmb.View import HtmlViewUtility


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file
        self.webView = QTextBrowser(self)
        self.htmlUtil = HtmlViewUtility.HtmlViewUtility(
            config.ContentArray,
            config.RotateContent,
            config.RotateContentTime,
            self.webView,
            self.onRefresh,
        )
        setEscKey(self)

    @pyqtSlot(str)
    def onRefresh(self, value):
        self.webView.setHtml(value)
