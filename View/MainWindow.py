from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtWebKit import QWebSettings
from View import HtmlViewUtility
import mainwindow_auto

class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file
        #settings = self.current_menu.settings()
        #settings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        #settings.setAttribute(QWebSettings.LocalContentCanAccessFileUrls, True)
        #settings.setAttribute(QWebSettings.LocalStorageEnabled, True)
        #settings.setAttribute(QWebSettings.AutoLoadImages, True)
        self.htmlUtil = HtmlViewUtility.HtmlViewUtility(config.ContentArray,
            config.RotateContent, config.RotateContentTime, self.current_menu, self.onRefresh)

    @pyqtSlot(str)
    def onRefresh(self, value):
        self.current_menu.setHtml(value)
