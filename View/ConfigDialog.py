from PyQt5.QtWidgets import *
#import numpy as np
import configdialog_auto


class ConfigDialog(QDialog, configdialog_auto.Ui_ConfigDialog):

    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._config = config
        self.okCancelButtonBox.rejected.connect(self.closeDialog)
        self.okCancelButtonBox.accepted.connect(self.saveAndClose)
        self.addImageButton.clicked.connect(self.addContent)
        self.deleteSelectionButton.clicked.connect(self.deleteSelectedContent)

    def closeDialog(self):
        self.close()

    def saveAndClose(self):
        tmpContentList = [str(self.loadedContentWidget.item(i).text()) for i in range(self.loadedContentWidget.count())]
        self._config.SaveSettings(self.use_images_check.isChecked(), self.use_html_file_check.isChecked(),
                                  self.use_menu_data_check.isChecked(), self.rotate_images_check.isChecked(),
                                  float(self.rotateTimeBox.value()),tmpContentList)
        self.close()

    def addContent(self):
        contentFile = QFileDialog.getOpenFileName(self)[0]
        self.loadedContentWidget.addItem(contentFile)

    def deleteSelectedContent(self):
        for SelectedItem in self.loadedContentWidget.selectedItems():
            self.loadedContentWidget.takeItem(self.loadedContentWidget.row(SelectedItem))