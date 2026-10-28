from types import SimpleNamespace
from typing import cast
from unittest.mock import Mock

import pytest
from PySide6.QtCore import QDate, QPoint, Qt
from PySide6.QtGui import QImage, QPainter
from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QApplication,
    QLabel,
    QPushButton,
    QRadioButton,
    QStyle,
    QStyleOptionButton,
    QStyleOptionSpinBox,
    QTableWidgetSelectionRange,
)

from ezdmb import STYLESHEET
from ezdmb.Controller.configuration import (
    configuration,
    default_content_groups,
    default_time_blocks,
)
from ezdmb.View.config_widget import config_widget


def spin_subcontrol_rect(spin_box, subcontrol):
    option = QStyleOptionSpinBox()
    option.initFrom(spin_box)
    option.rect = spin_box.rect()
    option.buttonSymbols = spin_box.buttonSymbols()
    option.stepEnabled = (
        QAbstractSpinBox.StepEnabledFlag.StepUpEnabled
        | QAbstractSpinBox.StepEnabledFlag.StepDownEnabled
    )
    return spin_box.style().subControlRect(
        QStyle.ComplexControl.CC_SpinBox,
        option,
        subcontrol,
        spin_box,
    )


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    application = cast(QApplication, app)
    application.setStyleSheet(STYLESHEET)
    return application


@pytest.fixture
def settings_widget(qapp):
    config = SimpleNamespace(
        RotateContent=True,
        RotateContentTime=15,
        ContentArray=[],
        RotationMode="interval",
        ContentGroups=default_content_groups(),
        TimeBlocks=default_time_blocks(),
        save_config=Mock(),
    )
    return config_widget(None, cast(configuration, config))


def test_settings_layout_is_responsive(settings_widget):
    assert settings_widget.minimumWidth() == 520
    assert settings_widget.minimumHeight() == 360
    assert settings_widget.settingsWidget.layout() is not None
    assert settings_widget.contentWidget.minimumWidth() == 0
    assert settings_widget.contentWidget.minimumHeight() == 0


def test_settings_controls_have_compact_hierarchy(settings_widget):
    assert settings_widget.settingsWidget.font().pointSize() <= 10
    assert settings_widget.rotationSettingsGrpBox.font().pointSize() == 12
    assert settings_widget.addRemoveGrpBox.font().pointSize() == 12
    assert settings_widget.everySecondsRadio.font().pointSize() == 14
    assert settings_widget.everySecondsRadio.minimumHeight() == 34
    assert settings_widget.vLayout5.spacing() == 12
    assert settings_widget.addContentButton.minimumHeight() == 34
    assert not settings_widget.addContentButton.icon().isNull()


def test_add_content_button_displays_icon_instead_of_text(settings_widget):
    assert settings_widget.addContentButton.text() == ""
    assert not settings_widget.addContentButton.icon().isNull()
    assert settings_widget.addContentButton.accessibleName() == "Add Content"
    assert settings_widget.addContentButton.toolTip() == "Add Content"


def test_inline_content_delete_removes_only_clicked_file(settings_widget, tmp_path):
    first_path = str(tmp_path / "first.png")
    second_path = str(tmp_path / "second.png")
    settings_widget._addContentListItem(first_path)
    settings_widget._addContentListItem(second_path)

    first_item = settings_widget.loadedContentWidget.item(0)
    row_widget = settings_widget.loadedContentWidget.itemWidget(first_item)
    assert row_widget is not None
    filename_label = row_widget.findChild(QLabel, "contentFilenameLabel")
    delete_button = row_widget.findChild(QPushButton, "deleteContentButton")
    assert filename_label is not None
    assert delete_button is not None
    assert filename_label.text() == "first.png"
    assert filename_label.toolTip() == first_path

    delete_button.click()

    assert settings_widget.getContentList() == [second_path]
    current_group = settings_widget._currentContentGroup()
    assert current_group is not None
    assert current_group["content"] == [second_path]
    settings_widget._config.save_config.assert_called_once()


def test_application_theme_styles_settings_controls(qapp):
    style = qapp.styleSheet()

    assert "font-family:" not in style
    assert "background-color: #f5f6f7" in style
    assert "QGroupBox" in style
    assert "QListWidget::item:selected" in style
    assert "QPushButton#addContentButton" in style
    assert "QRadioButton#everySecondsRadio::indicator" in style
    assert "width: 20px" in style
    assert "color: #174f91" in style
    assert "#3c3f41" not in style


@pytest.mark.parametrize(
    "object_name",
    ("everySecondsRadio", "byScheduleRadio", "noneRadio"),
)
def test_selected_radio_indicator_is_visible(qapp, object_name):
    radio = QRadioButton("Fixed Period: Every")
    radio.setObjectName(object_name)
    radio.setChecked(True)
    radio.resize(240, 34)
    radio.show()
    qapp.processEvents()

    image = QImage(radio.size(), QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    radio.render(painter, QPoint())
    painter.end()

    option = QStyleOptionButton()
    option.initFrom(radio)
    indicator = radio.style().subElementRect(
        QStyle.SubElement.SE_RadioButtonIndicator, option, radio
    )
    assert any(
        image.pixelColor(x, y).name() == "#1f5f9f"
        for x in range(indicator.left(), indicator.right() + 1)
        for y in range(indicator.top(), indicator.bottom() + 1)
    )


def test_rotation_radio_options_share_interval_controls(settings_widget):
    assert settings_widget.hLayout2.itemAt(0).layout() is (
        settings_widget.rotationIntervalLayout
    )
    assert settings_widget.rotationIntervalLayout.itemAt(0).widget() is (
        settings_widget.everySecondsRadio
    )
    assert settings_widget.rotationIntervalLayout.itemAt(1).widget() is (
        settings_widget.rotateTimeBox
    )
    assert settings_widget.hLayout2.itemAt(1).widget() is (
        settings_widget.byScheduleRadio
    )
    assert settings_widget.hLayout2.itemAt(2).widget() is settings_widget.noneRadio


def test_rotation_controls_follow_radio_selection(settings_widget):
    assert settings_widget.everySecondsRadio.isChecked()
    assert settings_widget.rotateTimeBox.isEnabled()
    assert settings_widget.secondsLabel.isEnabled()
    assert settings_widget.rotationSettingsGrpBox.property("rotationEnabled") is True

    settings_widget.noneRadio.setChecked(True)

    assert not settings_widget.rotateTimeBox.isEnabled()
    assert not settings_widget.secondsLabel.isEnabled()
    assert settings_widget.rotationSettingsGrpBox.property("rotationEnabled") is False

    settings_widget.byScheduleRadio.setChecked(True)

    assert settings_widget.rotateTimeBox.isEnabled()
    assert settings_widget.secondsLabel.isEnabled()
    assert settings_widget.rotationSettingsGrpBox.property("rotationEnabled") is True
    assert settings_widget.settingsTabs.currentWidget() is settings_widget.scheduleWidget


def test_group_toolbar_is_visible_only_for_schedule_mode(settings_widget):
    assert not settings_widget.byScheduleRadio.isChecked()
    assert settings_widget.groupToolbar.isHidden()
    assert not settings_widget.contentGroupCombo.isEnabled()
    assert not settings_widget.addGroupButton.isEnabled()
    assert not settings_widget.renameGroupButton.isEnabled()
    assert not settings_widget.deleteGroupButton.isEnabled()

    settings_widget.byScheduleRadio.setChecked(True)

    assert not settings_widget.groupToolbar.isHidden()
    assert settings_widget.contentGroupCombo.isEnabled()
    assert settings_widget.addGroupButton.isEnabled()
    assert settings_widget.renameGroupButton.isEnabled()
    assert not settings_widget.deleteGroupButton.isEnabled()

    settings_widget.everySecondsRadio.setChecked(True)

    assert settings_widget.groupToolbar.isHidden()
    assert not settings_widget.contentGroupCombo.isEnabled()
    assert not settings_widget.addGroupButton.isEnabled()
    assert not settings_widget.renameGroupButton.isEnabled()
    assert not settings_widget.deleteGroupButton.isEnabled()

    settings_widget.noneRadio.setChecked(True)

    assert settings_widget.groupToolbar.isHidden()


def test_add_group_button_displays_icon_instead_of_text(settings_widget):
    assert settings_widget.addGroupButton.text() == ""
    assert not settings_widget.addGroupButton.icon().isNull()
    assert settings_widget.addGroupButton.accessibleName() == "Add Group"
    assert settings_widget.addGroupButton.toolTip() == "Add Group"


def test_delete_group_button_displays_icon_instead_of_text(settings_widget):
    assert settings_widget.deleteGroupButton.text() == ""
    assert not settings_widget.deleteGroupButton.icon().isNull()
    assert settings_widget.deleteGroupButton.accessibleName() == "Delete Group"
    assert settings_widget.deleteGroupButton.toolTip() == "Delete Group"


def test_rename_group_button_displays_icon_instead_of_text(settings_widget):
    assert settings_widget.renameGroupButton.text() == ""
    assert not settings_widget.renameGroupButton.icon().isNull()
    assert settings_widget.renameGroupButton.accessibleName() == "Rename"
    assert settings_widget.renameGroupButton.toolTip() == "Rename"


def test_rotation_group_uses_disabled_background_style(qapp):
    style = qapp.styleSheet()

    assert 'QGroupBox[rotationEnabled="false"]' in style
    assert "background-color: #e8eaed" in style
    assert "QRadioButton#everySecondsRadio" in style
    assert "background-color: transparent" in style
    assert "QDoubleSpinBox#rotateTimeBox" in style


def test_rotation_controls_follow_loaded_configuration(qapp):
    config = SimpleNamespace(
        RotateContent=False,
        RotateContentTime=15,
        ContentArray=[],
        RotationMode="none",
        ContentGroups=default_content_groups(),
        TimeBlocks=default_time_blocks(),
    )
    widget = config_widget(None, cast(configuration, config))

    assert widget.noneRadio.isChecked()
    assert not widget.rotateTimeBox.isEnabled()
    assert not widget.secondsLabel.isEnabled()


def test_rotation_mode_is_saved(settings_widget):
    settings_widget.byScheduleRadio.setChecked(True)

    saved_config = settings_widget._config.save_config.call_args
    assert saved_config.kwargs["RotationMode"] == "schedule"
    assert saved_config.args[0] is False

    settings_widget.noneRadio.setChecked(True)

    saved_config = settings_widget._config.save_config.call_args
    assert saved_config.kwargs["RotationMode"] == "none"


def test_content_groups_have_separate_content_lists(settings_widget, monkeypatch):
    monkeypatch.setattr(
        "ezdmb.View.config_widget.QInputDialog.getText",
        lambda *args: ("Breakfast", True),
    )
    settings_widget.addContentGroup()

    settings_widget.loadedContentWidget.addItem("breakfast.png")
    settings_widget.saveUpdatedConfig()
    settings_widget.contentGroupCombo.setCurrentIndex(0)

    assert settings_widget._groups[0]["name"] == "Default"
    assert settings_widget._groups[0]["content"] == []
    assert settings_widget._groups[1]["name"] == "Breakfast"
    assert settings_widget._groups[1]["content"] == ["breakfast.png"]


def test_add_content_dialog_includes_video_formats(
    settings_widget, monkeypatch, tmp_path
):
    video_path = str(tmp_path / "menu.mp4")
    open_file_dialog = Mock(return_value=(video_path, ""))
    monkeypatch.setattr(
        "ezdmb.View.config_widget.QFileDialog.getOpenFileName",
        open_file_dialog,
    )

    settings_widget.addContent()

    assert settings_widget.loadedContentWidget.item(0).text() == video_path
    assert "*.mp4" in open_file_dialog.call_args.args[3]


def test_schedule_repeat_modes_show_expected_calendar_grid(settings_widget):
    assert settings_widget.repeatCombo.currentText() == "None"
    assert not settings_widget.scheduleCalendar.isHidden()
    assert settings_widget.timeBlockGrid.columnCount() == 1

    settings_widget.repeatCombo.setCurrentText("Daily")
    assert settings_widget.scheduleCalendar.isHidden()
    assert settings_widget.timeBlockGrid.columnCount() == 1
    assert settings_widget.timeBlockGrid.horizontalHeaderItem(0).text() == "Daily"

    settings_widget.repeatCombo.setCurrentText("Weekly")
    assert settings_widget.timeBlockGrid.columnCount() == 7
    assert settings_widget.timeBlockGrid.horizontalHeaderItem(0).text() == "Monday"


def test_selected_time_blocks_are_saved_for_each_repeat_mode(settings_widget):
    settings_widget.repeatCombo.setCurrentText("Daily")
    settings_widget.timeBlockGrid.setRangeSelected(
        QTableWidgetSelectionRange(16, 0, 19, 0),
        True,
    )
    assert settings_widget._timeBlocks["daily"] == [
        {"start": "08:00", "end": "10:00", "group_id": "default"}
    ]

    settings_widget.repeatCombo.setCurrentText("Weekly")
    settings_widget.timeBlockGrid.setRangeSelected(
        QTableWidgetSelectionRange(18, 1, 19, 1),
        True,
    )
    assert settings_widget._timeBlocks["weekly"] == {
        "Tuesday": [
            {"start": "09:00", "end": "10:00", "group_id": "default"}
        ]
    }

    settings_widget.repeatCombo.setCurrentText("None")
    settings_widget.scheduleCalendar.setSelectedDate(QDate(2026, 10, 22))
    settings_widget.timeBlockGrid.setRangeSelected(
        QTableWidgetSelectionRange(16, 0, 17, 0),
        True,
    )
    assert settings_widget._timeBlocks["dated"] == {
        "2026-10-22": [
            {"start": "08:00", "end": "09:00", "group_id": "default"}
        ]
    }
    assert (
        settings_widget._config.save_config.call_args.kwargs["TimeBlocks"]
        == settings_widget._timeBlocks
    )


def test_rotate_time_up_button_click_increments_value(settings_widget, qapp):
    settings_widget.show()
    qapp.processEvents()
    spin_box = settings_widget.rotateTimeBox
    initial_value = spin_box.value()
    up_button = spin_subcontrol_rect(
        spin_box, QStyle.SubControl.SC_SpinBoxUp
    )

    QTest.mouseClick(
        spin_box,
        Qt.MouseButton.LeftButton,
        pos=up_button.center(),
    )

    assert spin_box.value() == initial_value + 1
    settings_widget.close()


def test_rotate_time_uses_native_up_down_arrows(settings_widget, qapp):
    spin_box = settings_widget.rotateTimeBox

    assert spin_box.buttonSymbols() == QAbstractSpinBox.ButtonSymbols.UpDownArrows
    assert "QDoubleSpinBox::up-button" not in qapp.styleSheet()
    assert "QDoubleSpinBox::down-button" not in qapp.styleSheet()
