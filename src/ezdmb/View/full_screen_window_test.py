from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from ezdmb.View import full_screen_window


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def config():
    return SimpleNamespace(
        RotateContent=True,
        RotateContentTime=15,
        ContentArray=[],
        configUpdated=MagicMock(),
    )


class TestFullScreenWindow:
    def test_configures_display_and_refreshes_pixmap(
        self, qapp, config, monkeypatch
    ):
        worker = SimpleNamespace(stop=MagicMock())
        make_worker = MagicMock(return_value=worker)
        monkeypatch.setattr(
            full_screen_window.menu_content_view,
            "menu_content_view",
            make_worker,
        )
        reopen_preview = MagicMock()
        window = full_screen_window.full_screen_window(config, reopen_preview)

        assert window.windowTitle() == "Menu"
        assert window.objectName() == "full_screen_window"
        assert window.minimumWidth() == 200
        assert window.minimumHeight() == 200
        assert window.contentLbl.objectName() == "contentLbl"
        assert window.contentLbl.hasScaledContents()
        make_worker.assert_called_once_with(
            config,
            window.contentLbl,
            "full_screen_window",
            window.onRefresh,
        )

        pixmap = QPixmap(3, 2)
        pixmap.fill(Qt.GlobalColor.red)
        window.onRefresh(pixmap)

        assert window.contentLbl.pixmap().toImage() == pixmap.toImage()
        window.openOnOShortcut.activated.emit()
        reopen_preview.assert_called_once_with()

    def test_application_shutdown_stops_rotation_worker(
        self, qapp, config, monkeypatch
    ):
        worker = SimpleNamespace(stop=MagicMock())
        monkeypatch.setattr(
            full_screen_window.menu_content_view,
            "menu_content_view",
            MagicMock(return_value=worker),
        )
        window = full_screen_window.full_screen_window(config, MagicMock())

        qapp.aboutToQuit.emit()

        worker.stop.assert_called_once_with()
        window.close()