# pylint: disable=no-name-in-module
from copy import deepcopy
from uuid import uuid4

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView,
    QButtonGroup,
    QCalendarWidget,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ezdmb.Controller.configuration import (
    configuration,
    default_content_groups,
    default_time_blocks,
)
from ezdmb.Utility.icon_utility import getWindowIcon
from ezdmb.Utility.media_utility import CONTENT_FILE_DIALOG_FILTER
from ezdmb.View import resources  # noqa: F401


class config_widget(QWidget):
    trigger_settings_ui_update = Signal()

    _REPEAT_MODES = ("None", "Daily", "Weekly")
    _WEEKDAYS = (
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    )
    _SLOT_MINUTES = 30
    _SLOTS_PER_DAY = 24 * 60 // _SLOT_MINUTES

    def __init__(self, parent, config: configuration):
        super(self.__class__, self).__init__(parent)
        self._config = config
        self._loadingUi = False
        self._updatingGroups = False
        self._updatingScheduleGrid = False
        self._rotationMode = "interval"
        self._groups = default_content_groups()
        self._timeBlocks = default_time_blocks()
        self.trigger_settings_ui_update.connect(self.setUiFromConfig)

        # widgets
        self.setObjectName("config_widget")
        self.setMinimumSize(QSize(520, 360))

        self.setWindowIcon(getWindowIcon())

        preferredSizePolicy = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )
        preferredSizePolicy.setHorizontalStretch(0)
        preferredSizePolicy.setVerticalStretch(0)
        preferredSizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(preferredSizePolicy)
        self.vLayout6 = QVBoxLayout(self)
        self.vLayout6.setContentsMargins(20, 18, 20, 18)
        self.vLayout6.setSpacing(12)
        self.vLayout6.setObjectName("vLayout6")

        minExpMinExpSizePolicy = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )
        fixedFixedSizePolicy = QSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )

        self.settingsWidget = QWidget(self)
        self.settingsWidget.setSizePolicy(minExpMinExpSizePolicy)
        self.settingsWidget.setObjectName("settingsWidget")
        self.settingsLayout = QVBoxLayout(self.settingsWidget)
        self.settingsLayout.setContentsMargins(0, 0, 0, 0)

        self.settingsTabs = QTabWidget(self.settingsWidget)
        self.settingsTabs.setObjectName("settingsTabs")
        self.settingsLayout.addWidget(self.settingsTabs)

        # fonts
        twelvePtFont = QFont()
        twelvePtFont.setPointSize(12)
        twelvePtFont.setBold(False)
        self.contentWidget = QWidget(self.settingsTabs)
        self.contentWidget.setSizePolicy(minExpMinExpSizePolicy)
        self.contentWidget.setObjectName("contentTab")

        self.vLayout5 = QVBoxLayout(self.contentWidget)
        self.vLayout5.setContentsMargins(0, 0, 0, 0)
        self.vLayout5.setSpacing(12)
        self.vLayout5.setObjectName("vLayout5")
        self.rotationSettingsGrpBox = QGroupBox(self.contentWidget)
        preferredSizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        preferredSizePolicy.setHorizontalStretch(0)
        preferredSizePolicy.setVerticalStretch(0)
        preferredSizePolicy.setHeightForWidth(
            self.rotationSettingsGrpBox.sizePolicy().hasHeightForWidth()
        )
        self.rotationSettingsGrpBox.setSizePolicy(preferredSizePolicy)
        self.rotationSettingsGrpBox.setMinimumSize(QSize(180, 130))
        self.rotationSettingsGrpBox.setFont(twelvePtFont)
        self.rotationSettingsGrpBox.setObjectName("rotationSettingsGrpBox")

        self.hLayout2 = QVBoxLayout(self.rotationSettingsGrpBox)
        self.hLayout2.setContentsMargins(8, 8, 8, 8)
        self.hLayout2.setSpacing(6)
        self.hLayout2.setObjectName("hLayout2")

        rotationRadioFont = QFont(twelvePtFont)
        rotationRadioFont.setPointSize(12)

        self.noneRadio = QRadioButton("None", self.rotationSettingsGrpBox)
        self.noneRadio.setFont(rotationRadioFont)
        self.noneRadio.setMinimumHeight(34)
        self.noneRadio.setObjectName("noneRadio")
        self.hLayout2.addWidget(self.noneRadio)

        self.everySecondsRadio = QRadioButton("Fixed Period: Every", self.rotationSettingsGrpBox)
        self.everySecondsRadio.setFont(rotationRadioFont)
        self.everySecondsRadio.setMinimumHeight(34)
        self.everySecondsRadio.setObjectName("everySecondsRadio")

        self.rotateTimeBox = QDoubleSpinBox(self.rotationSettingsGrpBox)
        self.rotateTimeBox.setSizePolicy(fixedFixedSizePolicy)
        self.rotateTimeBox.setMinimumSize(QSize(70, 32))
        self.rotateTimeBox.setFont(twelvePtFont)
        self.rotateTimeBox.setDecimals(0)
        self.rotateTimeBox.setMinimum(1)
        self.rotateTimeBox.setMaximum(1800)
        self.rotateTimeBox.setObjectName("rotateTimeBox")
        self.secondsLabel = QLabel(self.rotationSettingsGrpBox)
        self.secondsLabel.setSizePolicy(minExpMinExpSizePolicy)
        self.secondsLabel.setMinimumSize(QSize(30, 30))
        self.secondsLabel.setFont(twelvePtFont)
        self.secondsLabel.setObjectName("secondsLabel")

        self.rotationIntervalLayout = QHBoxLayout()
        self.rotationIntervalLayout.setSpacing(10)
        self.rotationIntervalLayout.addWidget(self.everySecondsRadio)
        self.rotationIntervalLayout.addWidget(self.rotateTimeBox)
        self.rotationIntervalLayout.addWidget(self.secondsLabel)
        self.hLayout2.addLayout(self.rotationIntervalLayout)

        self.byScheduleRadio = QRadioButton("By schedule grid", self.rotationSettingsGrpBox)
        self.byScheduleRadio.setFont(rotationRadioFont)
        self.byScheduleRadio.setMinimumHeight(34)
        self.byScheduleRadio.setObjectName("byScheduleRadio")
        self.hLayout2.addWidget(self.byScheduleRadio)

        self.rotationModeButtonGroup = QButtonGroup(self.rotationSettingsGrpBox)
        self.rotationModeButtonGroup.setExclusive(True)
        self.rotationModeButtonGroup.addButton(self.everySecondsRadio)
        self.rotationModeButtonGroup.addButton(self.byScheduleRadio)
        self.rotationModeButtonGroup.addButton(self.noneRadio)

        self.vLayout5.addWidget(self.rotationSettingsGrpBox)

        self.addRemoveGrpBox = QGroupBox(self.contentWidget)
        self.addRemoveGrpBox.setSizePolicy(minExpMinExpSizePolicy)
        self.addRemoveGrpBox.setMinimumSize(QSize(180, 140))
        self.addRemoveGrpBox.setFont(twelvePtFont)
        self.addRemoveGrpBox.setObjectName("addRemoveGrpBox")

        self.vLayout2 = QVBoxLayout(self.addRemoveGrpBox)
        self.vLayout2.setContentsMargins(8, 8, 8, 8)
        self.vLayout2.setSpacing(8)
        self.vLayout2.setObjectName("vLayout2")

        self.groupToolbar = QWidget(self.addRemoveGrpBox)
        self.groupToolbar.setObjectName("groupToolbar")
        self.groupToolbarLayout = QHBoxLayout(self.groupToolbar)
        self.groupToolbarLayout.setContentsMargins(0, 0, 0, 0)
        self.groupToolbarLayout.setSpacing(8)
        self.contentGroupCombo = QComboBox(self.groupToolbar)
        self.contentGroupCombo.setObjectName("contentGroupCombo")
        self.groupToolbarLayout.addWidget(self.contentGroupCombo, 1)

        self.addGroupButton = QPushButton("Add Group", self.groupToolbar)
        self.addGroupButton.setObjectName("addGroupButton")
        self.groupToolbarLayout.addWidget(self.addGroupButton)

        self.renameGroupButton = QPushButton("Rename", self.groupToolbar)
        self.renameGroupButton.setObjectName("renameGroupButton")
        self.groupToolbarLayout.addWidget(self.renameGroupButton)

        self.deleteGroupButton = QPushButton("Delete Group", self.groupToolbar)
        self.deleteGroupButton.setObjectName("deleteGroupButton")
        self.groupToolbarLayout.addWidget(self.deleteGroupButton)
        self.vLayout2.addWidget(self.groupToolbar)

        self.loadedContentWidget = QListWidget(self.addRemoveGrpBox)
        self.loadedContentWidget.setSizePolicy(minExpMinExpSizePolicy)
        self.loadedContentWidget.setMinimumSize(QSize(200, 20))
        self.loadedContentWidget.setObjectName("loadedContentWidget")
        self.vLayout2.addWidget(self.loadedContentWidget)

        self.frame = QFrame(self.addRemoveGrpBox)
        self.frame.setMinimumSize(QSize(180, 48))
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Plain)
        self.frame.setObjectName("frame")

        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 4, 0, 0)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")

        addPixmap = QPixmap(":/images/add.svg")
        addButtonIcon = QIcon(addPixmap)

        self.addContentButton = QPushButton(self.frame)
        self.addContentButton.setIcon(addButtonIcon)
        self.addContentButton.setIconSize(addPixmap.rect().size())
        self.addContentButton.setMinimumSize(QSize(120, 34))
        self.addContentButton.setFont(twelvePtFont)
        self.addContentButton.setObjectName("addContentButton")
        self.horizontalLayout.addWidget(self.addContentButton)

        deletePixmap = QPixmap(":/images/delete.svg")
        deleteButtonIcon = QIcon(deletePixmap)
        self.deleteSelectionButton = QPushButton(self.frame)
        self.deleteSelectionButton.setIcon(deleteButtonIcon)
        self.deleteSelectionButton.setIconSize(deletePixmap.rect().size())
        self.deleteSelectionButton.setMinimumSize(QSize(120, 34))
        self.deleteSelectionButton.setFont(twelvePtFont)
        self.deleteSelectionButton.setObjectName("deleteSelectionButton")
        self.horizontalLayout.addWidget(self.deleteSelectionButton)

        self.vLayout2.addWidget(self.frame)
        self.vLayout5.addWidget(self.addRemoveGrpBox)

        self.settingsTabs.addTab(self.contentWidget, "Content")
        self._buildScheduleTab()
        self.vLayout6.addWidget(self.settingsWidget)

        self.setWindowTitle("Settings")
        self.rotationSettingsGrpBox.setTitle("Rotation")
        self.secondsLabel.setText("seconds")
        self.addRemoveGrpBox.setTitle("Add/Remove content")
        self.addContentButton.setText("Add Content")
        self.deleteSelectionButton.setText("Delete Selection")

        self.setUiFromConfig()

        # signals
        self.addGroupButton.clicked.connect(self.addContentGroup)
        self.renameGroupButton.clicked.connect(self.renameContentGroup)
        self.deleteGroupButton.clicked.connect(self.deleteContentGroup)
        self.contentGroupCombo.currentIndexChanged.connect(
            self.onContentGroupChanged
        )
        self.addContentButton.clicked.connect(self.addContent)
        self.deleteSelectionButton.clicked.connect(self.deleteSelectedContent)
        self.everySecondsRadio.toggled.connect(
            lambda checked: self.onRotationModeToggled("interval", checked)
        )
        self.byScheduleRadio.toggled.connect(
            lambda checked: self.onRotationModeToggled("schedule", checked)
        )
        self.noneRadio.toggled.connect(
            lambda checked: self.onRotationModeToggled("none", checked)
        )
        self.rotateTimeBox.valueChanged.connect(self.saveUpdatedConfig)
        self.repeatCombo.currentTextChanged.connect(self.onRepeatModeChanged)
        self.scheduleGroupCombo.currentIndexChanged.connect(
            self._refreshScheduleGroupHelp
        )
        self.scheduleCalendar.selectionChanged.connect(self.onScheduleDateChanged)
        self.timeBlockGrid.itemSelectionChanged.connect(
            self.onTimeBlockSelectionChanged
        )

    def _buildScheduleTab(self):
        self.scheduleWidget = QWidget(self.settingsTabs)
        self.scheduleWidget.setObjectName("scheduleTab")
        self.scheduleLayout = QVBoxLayout(self.scheduleWidget)
        self.scheduleLayout.setContentsMargins(8, 8, 8, 8)
        self.scheduleLayout.setSpacing(8)

        self.repeatLayout = QHBoxLayout()
        self.repeatLabel = QLabel("Repeat:", self.scheduleWidget)
        self.repeatLabel.setObjectName("repeatLabel")
        self.repeatCombo = QComboBox(self.scheduleWidget)
        self.repeatCombo.addItems(self._REPEAT_MODES)
        self.repeatCombo.setObjectName("repeatCombo")
        self.repeatLayout.addWidget(self.repeatLabel)
        self.repeatLayout.addWidget(self.repeatCombo)
        self.scheduleGroupLabel = QLabel("Assign blocks to:", self.scheduleWidget)
        self.scheduleGroupLabel.setObjectName("scheduleGroupLabel")
        self.repeatLayout.addWidget(self.scheduleGroupLabel)
        self.scheduleGroupCombo = QComboBox(self.scheduleWidget)
        self.scheduleGroupCombo.setObjectName("scheduleGroupCombo")
        self.repeatLayout.addWidget(self.scheduleGroupCombo, 1)
        self.repeatLayout.addStretch(1)
        self.scheduleLayout.addLayout(self.repeatLayout)

        self.scheduleHelpLabel = QLabel(
            "Choose a group, then select 30-minute blocks to assign those times "
            "to it. Assignments replace existing groups; choose Clear blocks "
            "to remove an assignment.",
            self.scheduleWidget,
        )
        self.scheduleHelpLabel.setWordWrap(True)
        self.scheduleHelpLabel.setObjectName("scheduleHelpLabel")
        self.scheduleLayout.addWidget(self.scheduleHelpLabel)

        self.scheduleGridLayout = QHBoxLayout()
        self.scheduleCalendar = QCalendarWidget(self.scheduleWidget)
        self.scheduleCalendar.setObjectName("scheduleCalendar")
        self.scheduleCalendar.setGridVisible(True)
        self.scheduleCalendar.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        self.scheduleCalendar.setMinimumSize(QSize(220, 180))
        self.scheduleGridLayout.addWidget(
            self.scheduleCalendar,
            0,
            Qt.AlignmentFlag.AlignTop,
        )

        self.timeBlockGrid = QTableWidget(self.scheduleWidget)
        self.timeBlockGrid.setObjectName("timeBlockGrid")
        self.timeBlockGrid.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.timeBlockGrid.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.timeBlockGrid.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.timeBlockGrid.setAlternatingRowColors(True)
        self.timeBlockGrid.setMinimumHeight(220)
        self.timeBlockGrid.verticalHeader().setDefaultSectionSize(18)
        self.timeBlockGrid.horizontalHeader().setMinimumSectionSize(36)
        self.timeBlockGrid.horizontalHeader().setDefaultSectionSize(56)
        self.timeBlockGrid.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.scheduleGridLayout.addWidget(self.timeBlockGrid, 1)
        self.scheduleLayout.addLayout(self.scheduleGridLayout, 1)

        self.settingsTabs.addTab(self.scheduleWidget, "Schedule")

    def _refreshTimeBlockGrid(self):
        repeat_mode = self.repeatCombo.currentText()
        if repeat_mode == "Daily":
            column_headers = ["Daily"]
        elif repeat_mode == "Weekly":
            column_headers = list(self._WEEKDAYS)
        else:
            column_headers = ["Selected date"]

        self._updatingScheduleGrid = True
        try:
            self.scheduleCalendar.setVisible(repeat_mode == "None")
            self.timeBlockGrid.clear()
            self.timeBlockGrid.setRowCount(self._SLOTS_PER_DAY)
            self.timeBlockGrid.setColumnCount(len(column_headers))
            self.timeBlockGrid.setHorizontalHeaderLabels(column_headers)
            self.timeBlockGrid.setVerticalHeaderLabels(
                [
                    self._slotToTime(slot)
                    for slot in range(self._SLOTS_PER_DAY)
                ]
            )

            for row in range(self._SLOTS_PER_DAY):
                for column in range(len(column_headers)):
                    item = QTableWidgetItem()
                    item.setFlags(
                        Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
                    )
                    self.timeBlockGrid.setItem(row, column, item)

            if repeat_mode == "Daily":
                blocks_by_column = [self._timeBlocks["daily"]]
            elif repeat_mode == "Weekly":
                blocks_by_column = [
                    self._timeBlocks["weekly"].get(day, [])
                    for day in self._WEEKDAYS
                ]
            else:
                date_key = self.scheduleCalendar.selectedDate().toString(
                    Qt.DateFormat.ISODate
                )
                blocks_by_column = [
                    self._timeBlocks["dated"].get(date_key, [])
                ]

            for column, blocks in enumerate(blocks_by_column):
                for block in blocks:
                    group_id = block.get("group_id")
                    group = self._findGroup(group_id)
                    if group is None:
                        continue
                    for row in self._rowsFromBlocks([block]):
                        self._setGridItemGroup(
                            self.timeBlockGrid.item(row, column),
                            group,
                        )
        finally:
            self._updatingScheduleGrid = False

    def _refreshScheduleGroupCombo(self, selected_group_id=None):
        if not hasattr(self, "scheduleGroupCombo"):
            return

        self.scheduleGroupCombo.clear()
        self.scheduleGroupCombo.addItem("Clear blocks", None)
        for group in self._groups:
            self.scheduleGroupCombo.addItem(group["name"], group["id"])

        index = (
            self.scheduleGroupCombo.findData(selected_group_id)
            if selected_group_id is not None
            else -1
        )
        if index < 0 and self._groups:
            index = 1
        self.scheduleGroupCombo.setCurrentIndex(max(index, 0))
        self._refreshScheduleGroupHelp()

    def _refreshScheduleGroupHelp(self):
        if not hasattr(self, "scheduleGroupCombo"):
            return
        if self.scheduleGroupCombo.currentData() is None:
            self.scheduleHelpLabel.setText(
                "Select Clear blocks, then select time cells to remove their "
                "group assignment."
            )
        else:
            self.scheduleHelpLabel.setText(
                "Choose a group, then select 30-minute blocks to assign those "
                "times to it. Assignments replace existing groups."
            )

    @staticmethod
    def _slotToTime(slot):
        total_minutes = slot * config_widget._SLOT_MINUTES
        return f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"

    @classmethod
    def _timeToSlot(cls, value):
        hours, minutes = (int(part) for part in value.split(":"))
        total_minutes = hours * 60 + minutes
        if (
            not 0 <= total_minutes <= 24 * 60
            or total_minutes % cls._SLOT_MINUTES != 0
        ):
            raise ValueError(f"Invalid 30-minute time block boundary: {value}")
        return total_minutes // cls._SLOT_MINUTES

    @classmethod
    def _rowsFromBlocks(cls, blocks):
        rows = set()
        for block in blocks:
            start = cls._timeToSlot(block["start"])
            end = cls._timeToSlot(block["end"])
            if end < start:
                raise ValueError("A time block must end after it starts.")
            rows.update(range(start, end))
        return rows

    @classmethod
    def _blocksFromAssignments(cls, assignments):
        blocks = []
        start = None
        current_group_id = None

        for slot in range(cls._SLOTS_PER_DAY + 1):
            group_id = (
                assignments[slot]
                if slot < cls._SLOTS_PER_DAY
                else None
            )
            if group_id == current_group_id:
                continue

            if current_group_id is not None:
                blocks.append(
                    {
                        "start": cls._slotToTime(start),
                        "end": cls._slotToTime(slot),
                        "group_id": current_group_id,
                    }
                )

            current_group_id = group_id
            start = slot if group_id is not None else None

        return blocks

    def _findGroup(self, group_id):
        return next(
            (group for group in self._groups if group["id"] == group_id),
            None,
        )

    def _setGridItemGroup(self, item, group):
        item.setText(group["name"])
        item.setToolTip(group["name"])
        item.setData(Qt.ItemDataRole.UserRole, group["id"])

    def _scheduleBlocksForColumn(self, column):
        repeat_mode = self.repeatCombo.currentText()
        if repeat_mode == "Daily":
            return self._timeBlocks["daily"]
        if repeat_mode == "Weekly":
            return self._timeBlocks["weekly"].get(self._WEEKDAYS[column], [])
        date_key = self.scheduleCalendar.selectedDate().toString(
            Qt.DateFormat.ISODate
        )
        return self._timeBlocks["dated"].get(date_key, [])

    def _assignmentsFromBlocks(self, blocks):
        assignments = [None] * self._SLOTS_PER_DAY
        group_order = {
            group["id"]: index for index, group in enumerate(self._groups)
        }
        for block in sorted(
            blocks,
            key=lambda entry: group_order.get(entry.get("group_id"), len(group_order)),
        ):
            group_id = block.get("group_id")
            if group_id not in group_order:
                continue
            for slot in self._rowsFromBlocks([block]):
                if assignments[slot] is None:
                    assignments[slot] = group_id
        return assignments

    def closeDialog(self):
        self.close()

    def getContentList(self):
        return [
            str(self.loadedContentWidget.item(i).text())
            for i in range(self.loadedContentWidget.count())
        ]

    def _currentContentGroup(self):
        return self._findGroup(self.contentGroupCombo.currentData())

    def _updateCurrentGroupContent(self):
        group = self._currentContentGroup()
        if group is not None:
            group["content"] = self.getContentList()

    def getAllContentList(self):
        self._updateCurrentGroupContent()
        return [
            str(content)
            for group in self._groups
            for content in group["content"]
        ]

    def _refreshContentGroupControls(self, selected_group_id=None):
        self._updatingGroups = True
        try:
            self.contentGroupCombo.clear()
            for group in self._groups:
                self.contentGroupCombo.addItem(group["name"], group["id"])

            index = self.contentGroupCombo.findData(selected_group_id)
            if index < 0 and self._groups:
                index = 0
            self.contentGroupCombo.setCurrentIndex(max(index, 0))

            group = self._currentContentGroup()
            self.loadedContentWidget.clear()
            if group is not None:
                for content in group["content"]:
                    self.loadedContentWidget.addItem(str(content))

            self._updateGroupToolbarState(self._rotationMode == "schedule")
            selected_schedule_group = self.scheduleGroupCombo.currentData()
            self._refreshScheduleGroupCombo(selected_schedule_group)
        finally:
            self._updatingGroups = False

    def _updateGroupToolbarState(self, schedule_mode):
        self.groupToolbar.setVisible(schedule_mode)
        group = self._currentContentGroup()
        self.contentGroupCombo.setEnabled(schedule_mode)
        self.addGroupButton.setEnabled(schedule_mode)
        self.renameGroupButton.setEnabled(schedule_mode and group is not None)
        self.deleteGroupButton.setEnabled(
            schedule_mode and len(self._groups) > 1
        )

    def _validateGroupName(self, name, excluded_group_id=None):
        normalized_name = name.strip()
        if not normalized_name:
            QMessageBox.warning(
                self,
                "Invalid Group Name",
                "A group name is required.",
            )
            return None
        if any(
            group["id"] != excluded_group_id
            and group["name"].casefold() == normalized_name.casefold()
            for group in self._groups
        ):
            QMessageBox.warning(
                self,
                "Invalid Group Name",
                "Group names must be unique.",
            )
            return None
        return normalized_name

    def addContentGroup(self):
        name, accepted = QInputDialog.getText(
            self,
            "Add Content Group",
            "Group name:",
        )
        if not accepted:
            return
        name = self._validateGroupName(name)
        if name is None:
            return

        group = {
            "id": uuid4().hex,
            "name": name,
            "content": [],
        }
        self._groups.append(group)
        self._refreshContentGroupControls(group["id"])
        self.saveUpdatedConfig()

    def renameContentGroup(self):
        group = self._currentContentGroup()
        if group is None:
            return

        name, accepted = QInputDialog.getText(
            self,
            "Rename Content Group",
            "Group name:",
        )
        if not accepted:
            return
        name = self._validateGroupName(name, group["id"])
        if name is None:
            return

        group["name"] = name
        self._refreshContentGroupControls(group["id"])
        self._refreshTimeBlockGrid()
        self.saveUpdatedConfig()

    def deleteContentGroup(self):
        group = self._currentContentGroup()
        if group is None or len(self._groups) <= 1:
            return

        answer = QMessageBox.question(
            self,
            "Delete Content Group",
            f"Delete '{group['name']}' and its content?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        group_id = group["id"]
        group_index = self._groups.index(group)
        self._groups.remove(group)
        self._removeGroupSchedule(group_id)
        next_group = self._groups[min(group_index, len(self._groups) - 1)]
        self._refreshContentGroupControls(next_group["id"])
        self._refreshTimeBlockGrid()
        self.saveUpdatedConfig()

    def _removeGroupSchedule(self, group_id):
        self._timeBlocks["daily"] = [
            block
            for block in self._timeBlocks["daily"]
            if block.get("group_id") != group_id
        ]
        for key in ("weekly", "dated"):
            schedules = self._timeBlocks[key]
            for period in list(schedules):
                schedules[period] = [
                    block
                    for block in schedules[period]
                    if block.get("group_id") != group_id
                ]
                if not schedules[period]:
                    del schedules[period]

    def onContentGroupChanged(self, index):
        if self._loadingUi or self._updatingGroups:
            return
        group = self._findGroup(self.contentGroupCombo.itemData(index))
        self.loadedContentWidget.clear()
        if group is not None:
            for content in group["content"]:
                self.loadedContentWidget.addItem(str(content))

    def saveAndClose(self):
        self._config.RotateContent = self._rotationMode == "interval"
        self._config.RotationMode = self._rotationMode
        self._config.RotateContentTime = self.rotateTimeBox.value()
        self._config.ContentArray = self.getAllContentList()
        self._config.ContentGroups = deepcopy(self._groups)
        self._config.TimeBlocks = deepcopy(self._timeBlocks)
        self.saveUpdatedConfig()
        self.close()

    def addContent(self):
        contentFile = QFileDialog.getOpenFileName(
            self,
            "Add Content",
            "",
            CONTENT_FILE_DIALOG_FILTER,
        )[0]
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
        self._loadingUi = True
        try:
            self.rotateTimeBox.setValue(float(self._config.RotateContentTime))

            rotation_mode = getattr(self._config, "RotationMode", None)
            if rotation_mode is None:
                rotation_mode = (
                    "interval" if self._config.RotateContent else "none"
                )
            if rotation_mode not in ("interval", "schedule", "none"):
                raise ValueError(f"Unsupported rotation mode: {rotation_mode}")
            self._rotationMode = rotation_mode
            self.everySecondsRadio.setChecked(rotation_mode == "interval")
            self.byScheduleRadio.setChecked(rotation_mode == "schedule")
            self.noneRadio.setChecked(rotation_mode == "none")
            self.setRotationControlsEnabled(rotation_mode)

            loaded_groups = getattr(self._config, "ContentGroups", None)
            if loaded_groups is None:
                loaded_groups = default_content_groups(self._config.ContentArray)
            self._groups = deepcopy(loaded_groups)
            if not self._groups:
                self._groups = default_content_groups()
            for index, group in enumerate(self._groups):
                group.setdefault("id", f"group-{index + 1}")
                group.setdefault("name", f"Group {index + 1}")
                group.setdefault("content", [])
            self._refreshContentGroupControls(self._groups[0]["id"])

            loaded_time_blocks = getattr(self._config, "TimeBlocks", None)
            if loaded_time_blocks is None:
                loaded_time_blocks = default_time_blocks()
            self._timeBlocks = deepcopy(loaded_time_blocks)
            self._timeBlocks.setdefault("repeat", "None")
            self._timeBlocks.setdefault("daily", [])
            self._timeBlocks.setdefault("weekly", {})
            self._timeBlocks.setdefault("dated", {})

            first_group_id = self._groups[0]["id"]
            for block in self._timeBlocks["daily"]:
                block.setdefault("group_id", first_group_id)
            for day_blocks in self._timeBlocks["weekly"].values():
                for block in day_blocks:
                    block.setdefault("group_id", first_group_id)
            for date_blocks in self._timeBlocks["dated"].values():
                for block in date_blocks:
                    block.setdefault("group_id", first_group_id)

            repeat_mode = self._timeBlocks["repeat"]
            if repeat_mode not in self._REPEAT_MODES:
                raise ValueError(f"Unsupported repeat mode: {repeat_mode}")
            self.repeatCombo.setCurrentText(repeat_mode)
            self._refreshTimeBlockGrid()
        finally:
            self._loadingUi = False

        print("UI updated from config")

    def onRepeatModeChanged(self, repeat_mode):
        if self._loadingUi:
            return
        if repeat_mode not in self._REPEAT_MODES:
            raise ValueError(f"Unsupported repeat mode: {repeat_mode}")

        self._timeBlocks["repeat"] = repeat_mode
        self._refreshTimeBlockGrid()
        self.saveUpdatedConfig()

    def onScheduleDateChanged(self):
        if not self._loadingUi:
            self._refreshTimeBlockGrid()

    def onTimeBlockSelectionChanged(self):
        if self._loadingUi or self._updatingScheduleGrid:
            return

        selected_cells = self.timeBlockGrid.selectedIndexes()
        if not selected_cells:
            return

        repeat_mode = self.repeatCombo.currentText()
        self._timeBlocks["repeat"] = repeat_mode
        selected_group_id = self.scheduleGroupCombo.currentData()

        if repeat_mode == "Daily":
            assignments = self._assignmentsFromBlocks(
                self._timeBlocks["daily"]
            )
            for index in selected_cells:
                assignments[index.row()] = selected_group_id
            self._timeBlocks["daily"] = self._blocksFromAssignments(assignments)
        elif repeat_mode == "Weekly":
            for column in {index.column() for index in selected_cells}:
                day = self._WEEKDAYS[column]
                assignments = self._assignmentsFromBlocks(
                    self._timeBlocks["weekly"].get(day, [])
                )
                for index in selected_cells:
                    if index.column() == column:
                        assignments[index.row()] = selected_group_id
                blocks = self._blocksFromAssignments(assignments)
                if blocks:
                    self._timeBlocks["weekly"][day] = blocks
                else:
                    self._timeBlocks["weekly"].pop(day, None)
        else:
            date_key = self.scheduleCalendar.selectedDate().toString(
                Qt.DateFormat.ISODate
            )
            dated_blocks = self._timeBlocks["dated"]
            assignments = self._assignmentsFromBlocks(
                dated_blocks.get(date_key, [])
            )
            for index in selected_cells:
                assignments[index.row()] = selected_group_id
            blocks = self._blocksFromAssignments(assignments)
            if blocks:
                dated_blocks[date_key] = blocks
            else:
                dated_blocks.pop(date_key, None)

        group = self._findGroup(selected_group_id)
        for index in selected_cells:
            item = self.timeBlockGrid.item(index.row(), index.column())
            if group is None:
                item.setText("")
                item.setToolTip("")
                item.setData(Qt.ItemDataRole.UserRole, None)
            else:
                self._setGridItemGroup(item, group)

        self.saveUpdatedConfig()

    def onRotationModeToggled(self, mode, checked):
        if not checked or self._loadingUi:
            return

        self._rotationMode = mode
        self.setRotationControlsEnabled(mode)
        if mode == "schedule":
            self.settingsTabs.setCurrentWidget(self.scheduleWidget)
        self.saveUpdatedConfig()

    def setRotationControlsEnabled(self, mode):
        enabled = mode != "none"
        self.rotateTimeBox.setEnabled(enabled)
        self.secondsLabel.setEnabled(enabled)
        self._updateGroupToolbarState(mode == "schedule")
        group_font = self.rotationSettingsGrpBox.font()
        self.rotationSettingsGrpBox.setProperty("rotationEnabled", enabled)
        self.rotationSettingsGrpBox.style().unpolish(self.rotationSettingsGrpBox)
        self.rotationSettingsGrpBox.style().polish(self.rotationSettingsGrpBox)
        self.rotationSettingsGrpBox.setFont(group_font)
        self.rotationSettingsGrpBox.update()

    def saveUpdatedConfig(self):
        if self._loadingUi:
            return
        self._updateCurrentGroupContent()
        self._config.save_config(
            self._rotationMode == "interval",
            float(self.rotateTimeBox.value()),
            self.getAllContentList(),
            TimeBlocks=deepcopy(self._timeBlocks),
            ContentGroups=deepcopy(self._groups),
            RotationMode=self._rotationMode,
        )
