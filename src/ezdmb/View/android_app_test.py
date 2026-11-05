from types import SimpleNamespace
from typing import cast
from unittest.mock import Mock

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from ezdmb.Controller.configuration import (
    configuration,
    default_content_groups,
    default_time_blocks,
)
from ezdmb.Utility.android_storage_utility import android_storage_utility
from ezdmb.View import android_app


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def app_window(qapp, monkeypatch, tmp_path):
    worker = SimpleNamespace(
        errorUpdated=Mock(),
        pause=Mock(),
        resume=Mock(),
        stop=Mock(),
    )
    monkeypatch.setattr(
        android_app,
        "menu_content_view",
        Mock(return_value=worker),
    )
    config = SimpleNamespace(
        RotateContent=True,
        RotateContentTime=15,
        ContentArray=[],
        RotationMode="interval",
        ContentGroups=default_content_groups(),
        TimeBlocks=default_time_blocks(),
        save_config=Mock(),
    )
    storage_adapter = android_storage_utility(
        tmp_path,
        picker=Mock(),
    )
    window = android_app.android_app_window(
        cast(configuration, config),
        storage_adapter,
    )
    yield window, worker
    window.shutdown()
    window.close()


def test_android_app_starts_on_display_and_exposes_settings(app_window):
    window, worker = app_window

    assert window._pageStack.currentWidget() is window.displayPage
    assert window.displayPage.settingsButton.text() == "Settings"
    worker.resume.assert_called_once_with()


def test_settings_navigation_pauses_display_and_back_resumes(app_window):
    window, worker = app_window

    window.showSettings()

    assert window._pageStack.currentWidget() is window.settingsPage
    worker.pause.assert_called_once_with()

    event = QKeyEvent(
        QKeyEvent.Type.KeyPress,
        Qt.Key.Key_Back,
        Qt.KeyboardModifier.NoModifier,
    )
    window.keyPressEvent(event)

    assert event.isAccepted()
    assert window._pageStack.currentWidget() is window.displayPage
    worker.resume.assert_called_with()


def test_settings_feedback_is_shown_inline(app_window):
    window, _worker = app_window

    window.showSettings()
    window.showStatusMessage("The bundle has been successfully imported.")

    assert window._pageStack.currentWidget() is window.settingsPage
    assert window.actionStatusLabel.text() == (
        "The bundle has been successfully imported."
    )
    assert not window.actionStatusLabel.isHidden()


def test_android_window_closes_rotation_worker(app_window):
    window, worker = app_window

    window.shutdown()

    worker.stop.assert_called_once_with()


def test_android_display_explains_unsupported_web_content(app_window):
    window, _worker = app_window
    display = window.displayPage.display

    display.onWebRefresh("https://example.com/menu")

    assert "cannot be rendered on Android" in display.contentLbl.text()


def test_android_display_reports_missing_pdf(app_window, tmp_path):
    window, _worker = app_window
    display = window.displayPage.display

    display.onPdfRefresh(str(tmp_path / "missing.pdf"))

    assert "PDF file is unavailable" in display.contentLbl.text()


def test_android_display_avoids_unstable_multimedia_jni_module(
    qapp,
    monkeypatch,
):
    worker = SimpleNamespace(
        errorUpdated=Mock(),
        pause=Mock(),
        resume=Mock(),
        stop=Mock(),
    )
    config = SimpleNamespace(
        RotateContent=True,
        RotateContentTime=15,
        ContentArray=[],
        RotationMode="interval",
        ContentGroups=default_content_groups(),
        TimeBlocks=default_time_blocks(),
        configUpdated=Mock(),
    )
    module_lookups = []

    def resolve_qt_type(module_name, type_name):
        module_lookups.append(module_name)

    monkeypatch.setattr(android_app, "is_android", lambda: True)
    monkeypatch.setattr(android_app, "_qt_type", resolve_qt_type)
    monkeypatch.setattr(
        android_app,
        "menu_content_view",
        Mock(return_value=worker),
    )
    display = android_app.android_display_widget(
        cast(configuration, config)
    )

    assert "PySide6.QtMultimedia" not in module_lookups
    assert "PySide6.QtMultimediaWidgets" not in module_lookups
    display.onVideoRefresh("menu.mp4")
    assert "Video playback is not available" in display.contentLbl.text()
    display.shutdown()
