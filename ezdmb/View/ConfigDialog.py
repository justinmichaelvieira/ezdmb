from pprint import pformat

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget
)

from ezdmb.Controller import SqliteImporter


class ConfigDialog(QDialog):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Display list of loaded content files for the DMB in the loadedContentWidget
        for i in config.ContentArray:
            item = QListWidgetItem("%s" % str(i))
            self.loadedContentWidget.addItem(item)

        self._config = config
        self.saveCancelButtonBox.rejected.connect(self.closeDialog)
        self.saveCancelButtonBox.accepted.connect(self.saveAndClose)
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
        try:
            menuData = importer.ImportMenuToSqliteFromFile(menuFile)
        except AttributeError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Could not load menu file.")
            msg.setInformativeText('The menu file could not be loaded; Please make sure the menu file is in the proper format.')
            msg.setWindowTitle("Could not load menu file.")
            msg.exec_()

    def setupUi(self, ConfigDialog):
        ConfigDialog.setObjectName("ConfigDialog")
        ConfigDialog.setWindowModality(Qt.ApplicationModal)
        ConfigDialog.resize(401, 331)
    
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ConfigDialog.sizePolicy().hasHeightForWidth())
        ConfigDialog.setSizePolicy(sizePolicy)
        ConfigDialog.setMinimumSize(QSize(400, 300))
        self.verticalLayout_6 = QVBoxLayout(ConfigDialog)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        
        minMinSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.settingsTabs = QTabWidget(ConfigDialog)
        self.settingsTabs.setSizePolicy(minMinSizePolicy)
        self.settingsTabs.setMinimumSize(QSize(200, 180))

        twelvePtFont = QFont()
        twelvePtFont.setPointSize(12)
        twelvePtFont.setBold(False)
        twelvePtFont.setWeight(50)

        fourteenPtFont = QFont()
        fourteenPtFont.setPointSize(14)
        fourteenPtFont.setBold(False)
        fourteenPtFont.setWeight(50)

        sixteenPtFont = QFont()
        sixteenPtFont.setPointSize(16)
        sixteenPtFont.setBold(False)
        sixteenPtFont.setWeight(50)

        twentyPointFont = QFont()
        twentyPointFont.setPointSize(20)

        self.settingsTabs.setFont(twentyPointFont)
        self.settingsTabs.setTabPosition(QTabWidget.North)
        self.settingsTabs.setTabShape(QTabWidget.Rounded)
        self.settingsTabs.setObjectName("settingsTabs")
        self.typesTab = QWidget()

        minExpMinExpSizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self.typesTab.setSizePolicy(minExpMinExpSizePolicy)
        self.typesTab.setMinimumSize(QSize(500, 300))
        self.typesTab.setObjectName("typesTab")
        self.verticalLayout_4 = QVBoxLayout(self.typesTab)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QGroupBox(self.typesTab)
        self.groupBox.setSizePolicy(minExpMinExpSizePolicy)
        self.groupBox.setMinimumSize(QSize(100, 100))

        self.groupBox.setFont(sixteenPtFont)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(-1, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.useImagesCheck = QCheckBox(self.groupBox)

        minExpandingFixedPolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.useImagesCheck.setSizePolicy(minExpandingFixedPolicy)
        self.useImagesCheck.setMinimumSize(QSize(100, 40))

        self.useImagesCheck.setFont(fourteenPtFont)
        self.useImagesCheck.setObjectName("useImagesCheck")
        self.verticalLayout.addWidget(self.useImagesCheck)

        self.useHtmlFileCheck = QCheckBox(self.groupBox)
        self.useHtmlFileCheck.setMinimumSize(QSize(100, 40))
        self.useHtmlFileCheck.setFont(fourteenPtFont)
        self.useHtmlFileCheck.setObjectName("useHtmlFileCheck")
        self.verticalLayout.addWidget(self.useHtmlFileCheck)

        self.useMenuDataCheck = QCheckBox(self.groupBox)
        self.useMenuDataCheck.setSizePolicy(minExpandingFixedPolicy)
        self.useMenuDataCheck.setMinimumSize(QSize(100, 40))
        self.useMenuDataCheck.setFont(fourteenPtFont)
        self.useMenuDataCheck.setObjectName("useMenuDataCheck")
        self.verticalLayout.addWidget(self.useMenuDataCheck)

        self.saveCancelButtonBox = QDialogButtonBox(self.groupBox)
        self.saveCancelButtonBox.setSizePolicy(minExpandingFixedPolicy)
        self.saveCancelButtonBox.setMinimumSize(QSize(140, 30))

        self.saveCancelButtonBox.setFont(twelvePtFont)
        self.saveCancelButtonBox.setLayoutDirection(Qt.LeftToRight)
        self.saveCancelButtonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.saveCancelButtonBox.setCenterButtons(True)
        self.saveCancelButtonBox.setObjectName("saveCancelButtonBox")
        self.verticalLayout.addWidget(self.saveCancelButtonBox)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.settingsTabs.addTab(self.typesTab, "")

        self.contentTab = QWidget()
        self.contentTab.setSizePolicy(minExpMinExpSizePolicy)
        self.contentTab.setMinimumSize(QSize(300, 100))
        self.contentTab.setObjectName("contentTab")

        self.verticalLayout_5 = QVBoxLayout(self.contentTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_2 = QGroupBox(self.contentTab)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QSize(180, 80))

        self.groupBox_2.setFont(sixteenPtFont)
        self.groupBox_2.setObjectName("groupBox_2")

        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setContentsMargins(8, 0, 8, 0)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.rotateImagesCheck = QCheckBox(self.groupBox_2)

        fixedFixedSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.rotateImagesCheck.setSizePolicy(fixedFixedSizePolicy)
        self.rotateImagesCheck.setMinimumSize(QSize(180, 24))
        self.rotateImagesCheck.setFont(twelvePtFont)
        self.rotateImagesCheck.setObjectName("rotateImagesCheck")

        self.horizontalLayout_2.addWidget(self.rotateImagesCheck)

        self.rotateTimeBox = QDoubleSpinBox(self.groupBox_2)
        self.rotateTimeBox.setSizePolicy(fixedFixedSizePolicy)
        self.rotateTimeBox.setMinimumSize(QSize(70, 24))
        self.rotateTimeBox.setFont(twelvePtFont)
        self.rotateTimeBox.setDecimals(0)
        self.rotateTimeBox.setMinimum(1)
        self.rotateTimeBox.setMaximum(1800)
        self.rotateTimeBox.setObjectName("rotateTimeBox")

        self.horizontalLayout_2.addWidget(self.rotateTimeBox)

        self.secondsLabel = QLabel(self.groupBox_2)
        self.secondsLabel.setSizePolicy(minExpMinExpSizePolicy)
        self.secondsLabel.setMinimumSize(QSize(50, 31))
        self.secondsLabel.setFont(twelvePtFont)
        self.secondsLabel.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.secondsLabel)

        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.contentTab)
        self.groupBox_3.setSizePolicy(minExpMinExpSizePolicy)
        self.groupBox_3.setMinimumSize(QSize(180, 140))
        self.groupBox_3.setFont(sixteenPtFont)
        self.groupBox_3.setObjectName("groupBox_3")

        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setContentsMargins(6, 0, 6, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setSizePolicy(minExpMinExpSizePolicy)
        self.label_2.setMinimumSize(QSize(200, 32))
        self.label_2.setFont(twelvePtFont)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)

        self.loadedContentWidget = QListWidget(self.groupBox_3)
        self.loadedContentWidget.setSizePolicy(minExpMinExpSizePolicy)
        self.loadedContentWidget.setMinimumSize(QSize(200, 20))
        self.loadedContentWidget.setObjectName("loadedContentWidget")
        self.verticalLayout_2.addWidget(self.loadedContentWidget)

        self.frame = QFrame(self.groupBox_3)
        self.frame.setMinimumSize(QSize(180, 40))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setObjectName("frame")

        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(6, 3, 6, 8)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.addImageButton = QPushButton(self.frame)
        self.addImageButton.setMinimumSize(QSize(120, 36))
        self.addImageButton.setFont(twelvePtFont)
        self.addImageButton.setObjectName("addImageButton")
        self.horizontalLayout.addWidget(self.addImageButton)

        self.deleteSelectionButton = QPushButton(self.frame)
        self.deleteSelectionButton.setMinimumSize(QSize(120, 36))
        self.deleteSelectionButton.setFont(twelvePtFont)
        self.deleteSelectionButton.setObjectName("deleteSelectionButton")
        self.horizontalLayout.addWidget(self.deleteSelectionButton)

        self.verticalLayout_2.addWidget(self.frame)
        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.settingsTabs.addTab(self.contentTab, "")

        self.importTab = QWidget()
        self.importTab.setObjectName("importTab")

        self.verticalLayout_7 = QVBoxLayout(self.importTab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.currentImportedMenuDataBox = QGroupBox(self.importTab)

        self.importMenuDataBox = QGroupBox(self.importTab)
        self.importMenuDataBox.setFont(sixteenPtFont)
        self.importMenuDataBox.setTitle("")
        self.importMenuDataBox.setAlignment(Qt.AlignCenter)
        self.importMenuDataBox.setFlat(True)
        self.importMenuDataBox.setObjectName("importMenuDataBox")

        self.verticalLayout_8 = QVBoxLayout(self.importMenuDataBox)
        self.verticalLayout_8.setContentsMargins(0, 0, -1, -1)
        self.verticalLayout_8.setObjectName("verticalLayout_8")

        self.importButton = QPushButton(self.importMenuDataBox)
        self.importButton.setSizePolicy(fixedFixedSizePolicy)
        self.importButton.setMinimumSize(QSize(200, 60))
        self.importButton.setObjectName("importButton")
        self.verticalLayout_8.addWidget(self.importButton)

        self.verticalLayout_7.addWidget(self.importMenuDataBox)

        self.settingsTabs.addTab(self.importTab, "")
        self.verticalLayout_6.addWidget(self.settingsTabs)

        ConfigDialog.setWindowTitle("Settings")
        self.useImagesCheck.setText("Use images")
        self.useHtmlFileCheck.setText("Use HTML files")
        self.useMenuDataCheck.setText("Use menu data import")
        self.settingsTabs.setTabText(self.settingsTabs.indexOf(self.typesTab), "Types")
        self.groupBox_2.setTitle("Rotation settings")
        self.rotateImagesCheck.setText(" Rotate content every")
        self.secondsLabel.setText("seconds")
        self.groupBox_3.setTitle("Add/Remove")
        self.label_2.setText("Loaded content:")
        self.addImageButton.setText("Add Content")
        self.deleteSelectionButton.setText("Delete Selection")
        self.settingsTabs.setTabText(self.settingsTabs.indexOf(self.contentTab), "Content")
        self.currentImportedMenuDataBox.setTitle("Current Imported Menu Data")
        self.importButton.setText("Import from file")
        self.settingsTabs.setTabText(self.settingsTabs.indexOf(self.importTab), "Import")
        self.settingsTabs.setCurrentIndex(0)
        