from types import SimpleNamespace

import pytest
from PySide6.QtWidgets import QApplication

from ezdmb import STYLESHEET
from ezdmb.View.config_widget import config_widget


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
    assert settings_widget.vLayout5.spacing() == 12
    assert settings_widget.addContentButton.minimumHeight() == 34


def test_application_theme_styles_settings_controls(qapp):
    style = qapp.styleSheet()

    assert "font-family:" not in style
    assert "background-color: #f5f6f7" in style
    assert "QGroupBox" in style
    assert "QListWidget::item:selected" in style
    assert "QPushButton#addContentButton" in style
    assert "color: #174f91" in style
    assert "#3c3f41" not in style
