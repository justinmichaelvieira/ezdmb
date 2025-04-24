from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QCheckBox,
    QDialog,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget
)

from ezdmb.Controller.Configuration import Configuration


class ConfigDialog(QDialog):
    def __init__(self, config: Configuration):
        super(self.__class__, self).__init__()
        self._config = config

        # widgets
        self.setObjectName("ConfigDialog")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(401, 331)

        preferredSizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        preferredSizePolicy.setHorizontalStretch(0)
        preferredSizePolicy.setVerticalStretch(0)
        preferredSizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(preferredSizePolicy)
        self.setMinimumSize(QSize(400, 300))
        self.vLayout6 = QVBoxLayout(self)
        self.vLayout6.setContentsMargins(0, 0, 0, 0)
        self.vLayout6.setSpacing(0)
        self.vLayout6.setObjectName("vLayout6")

        minMinSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        minExpMinExpSizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        fixedFixedSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.settingsTabs = QTabWidget(self)
        self.settingsTabs.setSizePolicy(minMinSizePolicy)
        self.settingsTabs.setMinimumSize(QSize(200, 180))

        # fonts
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
        self.contentTab = QWidget()
        self.contentTab.setSizePolicy(minExpMinExpSizePolicy)
        self.contentTab.setMinimumSize(QSize(300, 100))
        self.contentTab.setObjectName("contentTab")

        self.vLayout5 = QVBoxLayout(self.contentTab)
        self.vLayout5.setObjectName("vLayout5")
        self.rotationSettingsGrpBox = QGroupBox(self.contentTab)
        preferredSizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        preferredSizePolicy.setHorizontalStretch(0)
        preferredSizePolicy.setVerticalStretch(0)
        preferredSizePolicy.setHeightForWidth(self.rotationSettingsGrpBox.sizePolicy().hasHeightForWidth())
        self.rotationSettingsGrpBox.setSizePolicy(preferredSizePolicy)
        self.rotationSettingsGrpBox.setMinimumSize(QSize(180, 80))
        self.rotationSettingsGrpBox.setFont(sixteenPtFont)
        self.rotationSettingsGrpBox.setObjectName("rotationSettingsGrpBox")

        self.hLayout2 = QHBoxLayout(self.rotationSettingsGrpBox)
        self.hLayout2.setContentsMargins(8, 0, 8, 0)
        self.hLayout2.setSpacing(2)
        self.hLayout2.setObjectName("hLayout2")

        self.rotateImagesCheck = QCheckBox(self.rotationSettingsGrpBox)

        self.rotateImagesCheck.setSizePolicy(fixedFixedSizePolicy)
        self.rotateImagesCheck.setMinimumSize(QSize(180, 24))
        self.rotateImagesCheck.setFont(twelvePtFont)
        self.rotateImagesCheck.setObjectName("rotateImagesCheck")

        self.hLayout2.addWidget(self.rotateImagesCheck)

        self.rotateTimeBox = QDoubleSpinBox(self.rotationSettingsGrpBox)
        self.rotateTimeBox.setSizePolicy(fixedFixedSizePolicy)
        self.rotateTimeBox.setMinimumSize(QSize(70, 24))
        self.rotateTimeBox.setFont(twelvePtFont)
        self.rotateTimeBox.setDecimals(0)
        self.rotateTimeBox.setMinimum(1)
        self.rotateTimeBox.setMaximum(1800)
        self.rotateTimeBox.setObjectName("rotateTimeBox")

        self.hLayout2.addWidget(self.rotateTimeBox)

        self.secondsLabel = QLabel(self.rotationSettingsGrpBox)
        self.secondsLabel.setSizePolicy(minExpMinExpSizePolicy)
        self.secondsLabel.setMinimumSize(QSize(50, 31))
        self.secondsLabel.setFont(twelvePtFont)
        self.secondsLabel.setObjectName("secondsLabel")
        self.hLayout2.addWidget(self.secondsLabel)

        self.vLayout5.addWidget(self.rotationSettingsGrpBox)

        self.addRemoveGrpBox = QGroupBox(self.contentTab)
        self.addRemoveGrpBox.setSizePolicy(minExpMinExpSizePolicy)
        self.addRemoveGrpBox.setMinimumSize(QSize(180, 140))
        self.addRemoveGrpBox.setFont(sixteenPtFont)
        self.addRemoveGrpBox.setObjectName("addRemoveGrpBox")

        self.vLayout2 = QVBoxLayout(self.addRemoveGrpBox)
        self.vLayout2.setContentsMargins(6, 0, 6, 0)
        self.vLayout2.setSpacing(0)
        self.vLayout2.setObjectName("vLayout2")

        self.loadedContentWidget = QListWidget(self.addRemoveGrpBox)
        self.loadedContentWidget.setSizePolicy(minExpMinExpSizePolicy)
        self.loadedContentWidget.setMinimumSize(QSize(200, 20))
        self.loadedContentWidget.setObjectName("loadedContentWidget")
        self.vLayout2.addWidget(self.loadedContentWidget)

        self.frame = QFrame(self.addRemoveGrpBox)
        self.frame.setMinimumSize(QSize(180, 40))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setObjectName("frame")

        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(6, 3, 6, 8)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.addContentButton = QPushButton(self.frame)
        self.addContentButton.setMinimumSize(QSize(120, 36))
        self.addContentButton.setFont(twelvePtFont)
        self.addContentButton.setObjectName("addContentButton")
        self.horizontalLayout.addWidget(self.addContentButton)

        self.deleteSelectionButton = QPushButton(self.frame)
        self.deleteSelectionButton.setMinimumSize(QSize(120, 36))
        self.deleteSelectionButton.setFont(twelvePtFont)
        self.deleteSelectionButton.setObjectName("deleteSelectionButton")
        self.horizontalLayout.addWidget(self.deleteSelectionButton)

        self.vLayout2.addWidget(self.frame)
        self.vLayout5.addWidget(self.addRemoveGrpBox)

        self.settingsTabs.addTab(self.contentTab, "")
        self.vLayout6.addWidget(self.settingsTabs)

        self.setWindowTitle("Settings")
        self.rotationSettingsGrpBox.setTitle("Rotation settings")
        self.rotateImagesCheck.setText(" Rotate content every")
        self.secondsLabel.setText("seconds")
        self.addRemoveGrpBox.setTitle("Add/Remove content")
        self.addContentButton.setText("Add Content")
        self.deleteSelectionButton.setText("Delete Selection")
        self.settingsTabs.setTabText(self.settingsTabs.indexOf(self.contentTab), "Content")

        self.settingsTabs.setCurrentIndex(0)
        self.setUiFromConfig()

        # signals
        self.addContentButton.clicked.connect(self.addContent)
        self.deleteSelectionButton.clicked.connect(self.deleteSelectedContent)
        self.rotateImagesCheck.stateChanged.connect(self.saveUpdatedConfig)
        self.rotateTimeBox.valueChanged.connect(self.saveUpdatedConfig)

        # Display list of loaded content files for the DMB in the loadedContentWidget
        for i in config.ContentArray:
            item = QListWidgetItem("%s" % str(i))
            self.loadedContentWidget.addItem(item)

    def closeDialog(self):
        self.close()

    def getContentList(self):
        return [
            str(self.loadedContentWidget.item(i).text())
            for i in range(self.loadedContentWidget.count())
        ]

    def saveUpdatedConfig(self):
        self._config.SaveConfig(
            self.rotateImagesCheck.isChecked(),
            float(self.rotateTimeBox.value()),
            self.getContentList(),
        )

    def saveAndClose(self):
        self._config.RotateContent = self.rotateImagesCheck.isChecked()
        self._config.RotateContentTime = self.rotateTimeBox.value()
        self._config.ContentArray = self.getContentList()
        self.saveUpdatedConfig()
        self.close()

    def addContent(self):
        contentFile = QFileDialog.getOpenFileName(self)[0]
        if contentFile != "":
            self.loadedContentWidget.addItem(contentFile)
            self.saveUpdatedConfig()

    def deleteSelectedContent(self):
        for SelectedItem in self.loadedContentWidget.selectedItems():
            self.loadedContentWidget.takeItem(
                self.loadedContentWidget.row(SelectedItem)
            )

        self.saveUpdatedConfig()

    def setUiFromConfig(self):
        self.rotateImagesCheck.setChecked(bool(self._config.RotateContent))
        self.rotateTimeBox.setValue(float(self._config.RotateContentTime))
