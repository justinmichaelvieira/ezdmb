# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configdialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConfigDialog(object):
    def setupUi(self, ConfigDialog):
        ConfigDialog.setObjectName("ConfigDialog")
        ConfigDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ConfigDialog.resize(1058, 1023)
        ConfigDialog.setMinimumSize(QtCore.QSize(1054, 992))
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(ConfigDialog)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.Content = QtWidgets.QTabWidget(ConfigDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Content.sizePolicy().hasHeightForWidth())
        self.Content.setSizePolicy(sizePolicy)
        self.Content.setMinimumSize(QtCore.QSize(1042, 928))
        self.Content.setObjectName("Content")
        self.tab_basic = QtWidgets.QWidget()
        self.tab_basic.setObjectName("tab_basic")
        self.groupBox = QtWidgets.QGroupBox(self.tab_basic)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 1020, 885))
        self.groupBox.setMinimumSize(QtCore.QSize(1020, 885))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.use_images_check_2 = QtWidgets.QCheckBox(self.groupBox)
        self.use_images_check_2.setGeometry(QtCore.QRect(30, 300, 951, 241))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.use_images_check_2.sizePolicy().hasHeightForWidth())
        self.use_images_check_2.setSizePolicy(sizePolicy)
        self.use_images_check_2.setMinimumSize(QtCore.QSize(951, 241))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.use_images_check_2.setFont(font)
        self.use_images_check_2.setObjectName("use_images_check_2")
        self.use_images_check = QtWidgets.QCheckBox(self.groupBox)
        self.use_images_check.setGeometry(QtCore.QRect(30, 40, 981, 241))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.use_images_check.sizePolicy().hasHeightForWidth())
        self.use_images_check.setSizePolicy(sizePolicy)
        self.use_images_check.setMinimumSize(QtCore.QSize(981, 241))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.use_images_check.setFont(font)
        self.use_images_check.setObjectName("use_images_check")
        self.use_images_check_3 = QtWidgets.QCheckBox(self.groupBox)
        self.use_images_check_3.setGeometry(QtCore.QRect(30, 560, 991, 311))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.use_images_check_3.sizePolicy().hasHeightForWidth())
        self.use_images_check_3.setSizePolicy(sizePolicy)
        self.use_images_check_3.setMinimumSize(QtCore.QSize(981, 0))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.use_images_check_3.setFont(font)
        self.use_images_check_3.setObjectName("use_images_check_3")
        self.Content.addTab(self.tab_basic, "")
        self.tab_images = QtWidgets.QWidget()
        self.tab_images.setObjectName("tab_images")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_images)
        self.groupBox_2.setGeometry(QtCore.QRect(9, 10, 1021, 121))
        self.groupBox_2.setMinimumSize(QtCore.QSize(1021, 121))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(490, 30, 511, 71))
        self.label.setMinimumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox.setGeometry(QtCore.QRect(310, 50, 121, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox.setSizePolicy(sizePolicy)
        self.doubleSpinBox.setMinimumSize(QtCore.QSize(71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.doubleSpinBox.setFont(font)
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setMinimum(0.5)
        self.doubleSpinBox.setMaximum(30.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox.setGeometry(QtCore.QRect(30, 30, 271, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setMinimumSize(QtCore.QSize(271, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_images)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 140, 1021, 601))
        self.groupBox_3.setMinimumSize(QtCore.QSize(1021, 601))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(40, 30, 971, 61))
        self.label_2.setMinimumSize(QtCore.QSize(971, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.listView = QtWidgets.QListView(self.groupBox_3)
        self.listView.setGeometry(QtCore.QRect(20, 100, 991, 271))
        self.listView.setMinimumSize(QtCore.QSize(991, 271))
        self.listView.setObjectName("listView")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(570, 400, 261, 61))
        self.pushButton_2.setMinimumSize(QtCore.QSize(261, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(190, 400, 271, 61))
        self.pushButton.setMinimumSize(QtCore.QSize(271, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.Content.addTab(self.tab_images, "")
        self.verticalLayout_6.addWidget(self.Content)
        self.groupBox_4 = QtWidgets.QGroupBox(ConfigDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMinimumSize(QtCore.QSize(1040, 90))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.okCancelButtonBox = QtWidgets.QDialogButtonBox(self.groupBox_4)
        self.okCancelButtonBox.setGeometry(QtCore.QRect(-10, 20, 1040, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.okCancelButtonBox.sizePolicy().hasHeightForWidth())
        self.okCancelButtonBox.setSizePolicy(sizePolicy)
        self.okCancelButtonBox.setMinimumSize(QtCore.QSize(1040, 34))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.okCancelButtonBox.setFont(font)
        self.okCancelButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.okCancelButtonBox.setCenterButtons(False)
        self.okCancelButtonBox.setObjectName("okCancelButtonBox")
        self.verticalLayout_6.addWidget(self.groupBox_4)

        self.retranslateUi(ConfigDialog)
        self.Content.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ConfigDialog)

    def retranslateUi(self, ConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        ConfigDialog.setWindowTitle(_translate("ConfigDialog", "Dialog"))
        self.groupBox.setTitle(_translate("ConfigDialog", "Content"))
        self.use_images_check_2.setText(_translate("ConfigDialog", "Use HTML file"))
        self.use_images_check.setText(_translate("ConfigDialog", "Use images"))
        self.use_images_check_3.setText(_translate("ConfigDialog", "Use menu data import"))
        self.Content.setTabText(self.Content.indexOf(self.tab_basic), _translate("ConfigDialog", "Basic"))
        self.groupBox_2.setTitle(_translate("ConfigDialog", "Rotation settings"))
        self.label.setText(_translate("ConfigDialog", "minutes"))
        self.checkBox.setText(_translate("ConfigDialog", " Rotate Images every"))
        self.groupBox_3.setTitle(_translate("ConfigDialog", "Add/Remove"))
        self.label_2.setText(_translate("ConfigDialog", "Loaded Images:"))
        self.pushButton_2.setText(_translate("ConfigDialog", "Delete Selection"))
        self.pushButton.setText(_translate("ConfigDialog", "Add Image"))
        self.Content.setTabText(self.Content.indexOf(self.tab_images), _translate("ConfigDialog", "Images"))
