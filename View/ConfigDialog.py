from pprint import pformat

from PyQt5.QtWidgets import *

from Controller import SqliteImporter
from View import configdialog_auto


class ConfigDialog(QDialog, configdialog_auto.Ui_ConfigDialog):

    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # display list of loaded content files for the DMB
        # in the loadedContentWidget
        for i in config.ContentArray:
            item = QListWidgetItem("%s" % str(i))
            self.loadedContentWidget.addItem(item)

        self._config = config
        self.okCancelButtonBox.rejected.connect(self.closeDialog)
        self.okCancelButtonBox.accepted.connect(self.saveAndClose)
        self.addImageButton.clicked.connect(self.addContent)
        self.deleteSelectionButton.clicked.connect(self.deleteSelectedContent)
        self.importButton.clicked.connect(self.importMenuToSqliteFromFile)

    def closeDialog(self):
        self.close()

    def saveAndClose(self):
        tmpContentList = [str(self.loadedContentWidget.item(i).text()) for i in range(self.loadedContentWidget.count())]
        self._config.SaveConfig(self.use_images_check.isChecked(), self.use_html_file_check.isChecked(),
                                  self.use_menu_data_check.isChecked(), self.rotate_images_check.isChecked(),
                                  float(self.rotateTimeBox.value()),tmpContentList)
        self._config.UseImages = self.use_images_check.isChecked()
        self._config.UseHTML = self.use_html_file_check.isChecked()
        self._config.UseImported = self.use_menu_data_check.isChecked()
        self._config.RotateContent = self.rotate_images_check.isChecked()
        self._config.RotateContentTime = self.rotateTimeBox.value()
        self._config.ContentArray = tmpContentList
        self.close()

    def addContent(self):
        contentFile = QFileDialog.getOpenFileName(self)[0]
        self.loadedContentWidget.addItem(contentFile)

    def deleteSelectedContent(self):
        for SelectedItem in self.loadedContentWidget.selectedItems():
            self.loadedContentWidget.takeItem(self.loadedContentWidget.row(SelectedItem))

    def setUiFromConfig(self):
        self.use_images_check.setChecked(bool(self._config.UseImages))
        self.use_html_file_check.setChecked(bool(self._config.UseHTML))
        self.use_menu_data_check.setChecked(bool(self._config.UseImported))
        self.rotate_images_check.setChecked(bool(self._config.RotateContent))
        self.rotateTimeBox.setValue(float(self._config.RotateContentTime))

    def importMenuToSqliteFromFile(self):
        importer = SqliteImporter.SqliteImporter()
        menuFile = QFileDialog.getOpenFileName(self)[0]
        menuData = importer.ImportMenuToSqliteFromFile(menuFile)
        self.menuLbl.text = pformat(menuData)
