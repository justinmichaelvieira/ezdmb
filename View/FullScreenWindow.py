from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebKit import QWebSettings
from View import HtmlViewUtility
import fullscreenwindow_auto

class FullScreenWindow(QMainWindow, fullscreenwindow_auto.Ui_FullScreenWindow):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        #settings = self.label_pic.settings()
        #settings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        #settings.setAttribute(QWebSettings.LocalContentCanAccessFileUrls, True)
        #settings.setAttribute(QWebSettings.LocalStorageEnabled, True)
        #settings.setAttribute(QWebSettings.AutoLoadImages, True)
        self.htmlUtil = HtmlViewUtility.HtmlViewUtility(config.ContentArray,
            config.RotateContent, config.RotateContentTime, self.label_pic, self.onRefresh)

    @pyqtSlot(str)
    def onRefresh(self, value):
        self.label_pic.setHtml(value)
