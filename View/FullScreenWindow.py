from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utility.ShortcutUtility import setEscKey
from View import HtmlViewUtility, fullscreenwindow_auto


class FullScreenWindow(QMainWindow, fullscreenwindow_auto.Ui_FullScreenWindow):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.htmlUtil = HtmlViewUtility.HtmlViewUtility(config.ContentArray,
            config.RotateContent, config.RotateContentTime, self.label_pic, self.onRefresh)
        setEscKey(self)

    @pyqtSlot(str)
    def onRefresh(self, value):
        self.label_pic.setHtml(value)
