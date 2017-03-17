import sys
import PyQt5
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import mainwindow_auto

# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file