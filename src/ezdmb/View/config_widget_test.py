from types import SimpleNamespace

import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QApplication,
    QStyle,
    QStyleOptionSpinBox,
)

from ezdmb import STYLESHEET
from ezdmb.View.config_widget import config_widget


def spin_subcontrol_rect(spin_box, subcontrol):
    option = QStyleOptionSpinBox()
    option.initFrom(spin_box)
    option.rect = spin_box.rect()
    option.buttonSymbols = spin_box.buttonSymbols()
    option.stepEnabled = (
        QAbstractSpinBox.StepEnabled.StepUpEnabled
        | QAbstractSpinBox.StepEnabled.StepDownEnabled
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
    app.setStyleSheet(STYLESHEET)
    return app


@pytest.fixture
def settings_widget(qapp):
    config = SimpleNamespace(
        RotateContent=True,
        RotateContentTime=15,
        ContentArray=[],
    )
    return config_widget(None, config)


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
    assert settings_widget.rotateImagesCheck.font().pointSize() == 14
    assert settings_widget.rotateImagesCheck.minimumHeight() == 34
    assert settings_widget.vLayout5.spacing() == 12
    assert settings_widget.addContentButton.minimumHeight() == 34
    assert not settings_widget.addContentButton.icon().isNull()


def test_application_theme_styles_settings_controls(qapp):
    style = qapp.styleSheet()

    assert "font-family:" not in style
    assert "background-color: #f5f6f7" in style
    assert "QGroupBox" in style
    assert "QListWidget::item:selected" in style
    assert "QPushButton#addContentButton" in style
    assert "QCheckBox#rotateImagesCheck::indicator" in style
    assert "width: 20px" in style
    assert "color: #174f91" in style
    assert "#3c3f41" not in style


def test_rotation_checkbox_is_above_interval_controls(settings_widget):
    assert settings_widget.hLayout2.itemAt(0).widget() is (
        settings_widget.rotateImagesCheck
    )
    assert settings_widget.hLayout2.itemAt(1).layout() is (
        settings_widget.rotationIntervalLayout
    )


def test_rotation_controls_follow_checkbox(settings_widget):
    assert settings_widget.rotateTimeBox.isEnabled()
    assert settings_widget.secondsLabel.isEnabled()
    assert settings_widget.rotationSettingsGrpBox.property("rotationEnabled") is True

    settings_widget.rotateImagesCheck.setChecked(False)

    assert not settings_widget.rotateTimeBox.isEnabled()
    assert not settings_widget.secondsLabel.isEnabled()
    assert settings_widget.rotationSettingsGrpBox.property("rotationEnabled") is False

    settings_widget.rotateImagesCheck.setChecked(True)

    assert settings_widget.rotateTimeBox.isEnabled()
    assert settings_widget.secondsLabel.isEnabled()
    assert settings_widget.rotationSettingsGrpBox.property("rotationEnabled") is True


def test_rotation_group_uses_disabled_background_style(qapp):
    style = qapp.styleSheet()

    assert 'QGroupBox[rotationEnabled="false"]' in style
    assert "background-color: #e8eaed" in style
    assert "QCheckBox#rotateImagesCheck, QLabel#secondsLabel" in style
    assert "background-color: transparent" in style
    assert "QDoubleSpinBox#rotateTimeBox" in style


def test_rotation_controls_follow_loaded_configuration(qapp):
    config = SimpleNamespace(
        RotateContent=False,
        RotateContentTime=15,
        ContentArray=[],
    )
    widget = config_widget(None, config)

    assert not widget.rotateImagesCheck.isChecked()
    assert not widget.rotateTimeBox.isEnabled()
    assert not widget.secondsLabel.isEnabled()


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
