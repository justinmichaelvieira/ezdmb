import sys
import PyQt5
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from View import HtmlViewUtility
import fullscreenwindow_auto

class FullScreenWindow(QMainWindow, fullscreenwindow_auto.Ui_FullScreenWindow):

    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setPreviewImageContent(config.SavedImage)

    def setPreviewImageContent(self, image):
        hUtility = HtmlViewUtility.HtmlViewUtility()
        self.label_pic.setHtml(hUtility.getImagePage(image))