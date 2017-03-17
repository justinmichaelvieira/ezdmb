import sys
import PyQt5
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import fullscreenwindow_auto

class FullScreenWindow(QMainWindow, fullscreenwindow_auto.Ui_FullScreenWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)