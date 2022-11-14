from pprint import pformat

from PyQt5.QtWidgets import QDialog, QListWidgetItem, QFileDialog

from ezdmb.Controller import SqliteImporter
from ezdmb.View.generated.ConfigDialog_ui import Ui_ConfigDialog


class ConfigDialog(QDialog, Ui_ConfigDialog):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Display list of loaded content files for the DMB in the loadedContentWidget
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
        tmpContentList = [
            str(self.loadedContentWidget.item(i).text())
            for i in range(self.loadedContentWidget.count())
        ]
        self._config.SaveConfig(
            self.useImagesCheck.isChecked(),
            self.useHtmlFileCheck.isChecked(),
            self.useMenuDataCheck.isChecked(),
            self.rotateImagesCheck.isChecked(),
            float(self.rotateTimeBox.value()),
            tmpContentList,
        )

        self._config.UseImages = self.useImagesCheck.isChecked()
        self._config.UseHTML = self.useHtmlFileCheck.isChecked()
        self._config.UseImported = self.useMenuDataCheck.isChecked()
        self._config.RotateContent = self.rotateImagesCheck.isChecked()
        self._config.RotateContentTime = self.rotateTimeBox.value()
        self._config.ContentArray = tmpContentList
        self.close()

    def addContent(self):
        contentFile = QFileDialog.getOpenFileName(self)[0]
        self.loadedContentWidget.addItem(contentFile)

    def deleteSelectedContent(self):
        for SelectedItem in self.loadedContentWidget.selectedItems():
            self.loadedContentWidget.takeItem(
                self.loadedContentWidget.row(SelectedItem)
            )

    def setUiFromConfig(self):
        self.useImagesCheck.setChecked(bool(self._config.UseImages))
        self.useHtmlFileCheck.setChecked(bool(self._config.UseHTML))
        self.useMenuDataCheck.setChecked(bool(self._config.UseImported))
        self.rotateImagesCheck.setChecked(bool(self._config.RotateContent))
        self.rotateTimeBox.setValue(float(self._config.RotateContentTime))

    def importMenuToSqliteFromFile(self):
        importer = SqliteImporter.SqliteImporter()
        menuFile = QFileDialog.getOpenFileName(self)[0]
        menuData = importer.ImportMenuToSqliteFromFile(menuFile)
        self.menuLbl.text = pformat(menuData)
