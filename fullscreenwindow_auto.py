# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fullscreenwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from Controller import Configuration


class Ui_FullScreenWindow(object):
    def setupUi(self, FullScreenWindow):
        FullScreenWindow.setObjectName("FullScreenWindow")
        FullScreenWindow.setWindowModality(QtCore.Qt.WindowModal)
        FullScreenWindow.setEnabled(True)
        FullScreenWindow.resize(1202, 940)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FullScreenWindow.sizePolicy().hasHeightForWidth())
        FullScreenWindow.setSizePolicy(sizePolicy)
        FullScreenWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(FullScreenWindow)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 2, 1115, 745))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_pic = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.label_pic.sizePolicy().hasHeightForWidth())
        self.label_pic.setSizePolicy(sizePolicy)
        self.label_pic.setAutoFillBackground(True)
        self.label_pic.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_pic.setText("")

        #not generated!
        config = Configuration.Configuration()
        self.label_pic.setPixmap(QtGui.QPixmap(config.SavedImage))
        
        self.label_pic.setScaledContents(True)
        self.label_pic.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_pic.setObjectName("label_pic")
        self.verticalLayout.addWidget(self.label_pic)
        FullScreenWindow.setCentralWidget(self.label_pic)

        self.retranslateUi(FullScreenWindow)
        QtCore.QMetaObject.connectSlotsByName(FullScreenWindow)

    def retranslateUi(self, FullScreenWindow):
        _translate = QtCore.QCoreApplication.translate
        FullScreenWindow.setWindowTitle(_translate("FullScreenWindow", "Menu"))

