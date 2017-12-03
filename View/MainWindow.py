from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utility.ShortcutUtility import setEscKey


from View import HtmlViewUtility, mainwindow_auto


class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file
        self.htmlUtil = HtmlViewUtility.HtmlViewUtility(config.ContentArray,
            config.RotateContent, config.RotateContentTime, self.current_menu, self.onRefresh)
        setEscKey(self)

    @pyqtSlot(str)
    def onRefresh(self, value):
        self.current_menu.setHtml(value)
