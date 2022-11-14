from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow
from ezdmb.Utility.ShortcutUtility import setEscKey

from ezdmb.View.generated.MainWindow_ui import Ui_MainWindow
from ezdmb.View import HtmlViewUtility


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file
        self.htmlUtil = HtmlViewUtility.HtmlViewUtility(
            config.ContentArray,
            config.RotateContent,
            config.RotateContentTime,
            self.mainWindowCurrentContent,
            self.onRefresh,
        )
        setEscKey(self)

    @pyqtSlot(str)
    def onRefresh(self, value):
        self.mainWindowCurrentContent.setText(value)
