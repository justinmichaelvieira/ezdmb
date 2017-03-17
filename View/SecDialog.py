import sys
import PyQt5
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import secdialog_auto
import Configuration

class SecDialog(QDialog, secdialog_auto.Ui_SecDialog):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.okCancelButtonBox.accepted.connect(self.closeDialog)
        self.okCancelButtonBox.rejected.connect(self.saveAndClose)

    def closeDialog(self):
        self.close()
        pass

    def saveAndClose(self):
        self.close()
        pass
