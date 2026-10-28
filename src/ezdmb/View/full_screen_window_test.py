from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QApplication

from ezdmb.Controller.configuration import (
    default_content_groups,
    default_time_blocks,
)
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
        RotationMode="interval",
        ContentGroups=default_content_groups(),
        TimeBlocks=default_time_blocks(),
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
            window.onVideoRefresh,
            window.onPdfRefresh,
            window.onWebRefresh,
        )

        pixmap = QPixmap(3, 2)
        pixmap.fill(Qt.GlobalColor.red)
        window.onRefresh(pixmap)

        assert window.contentLbl.pixmap().toImage() == pixmap.toImage()
        window.openOnOShortcut.activated.emit()
        reopen_preview.assert_called_once_with()

    def test_plays_video_and_stops_it_for_image_content(
        self, qapp, config, monkeypatch, tmp_path
    ):
        worker = SimpleNamespace(stop=MagicMock())
        monkeypatch.setattr(
            full_screen_window.menu_content_view,
            "menu_content_view",
            MagicMock(return_value=worker),
        )
        player = MagicMock()
        player_class = MagicMock(return_value=player)
        player_class.Loops = QMediaPlayer.Loops
        monkeypatch.setattr(full_screen_window, "QMediaPlayer", player_class)
        audio_output = MagicMock()
        monkeypatch.setattr(
            full_screen_window,
            "QAudioOutput",
            MagicMock(return_value=audio_output),
        )
        window = full_screen_window.full_screen_window(config, MagicMock())
        video_path = str(tmp_path / "menu.mp4")

        window.onVideoRefresh(video_path)

        player.setSource.assert_called_once_with(QUrl.fromLocalFile(video_path))
        player.setLoops.assert_called_once_with(QMediaPlayer.Loops.Infinite)
        player.play.assert_called_once_with()
        assert window.contentStack.currentWidget() is window.videoWidget

        pixmap = QPixmap(3, 2)
        pixmap.fill(Qt.GlobalColor.red)
        window.onRefresh(pixmap)

        player.stop.assert_called()
        assert window.contentStack.currentWidget() is window.contentLbl
        assert window.contentLbl.pixmap().toImage() == pixmap.toImage()
        window.close()

    def test_video_playback_error_is_visible(
        self, qapp, config, monkeypatch, tmp_path
    ):
        worker = SimpleNamespace(stop=MagicMock())
        monkeypatch.setattr(
            full_screen_window.menu_content_view,
            "menu_content_view",
            MagicMock(return_value=worker),
        )
        player = MagicMock()
        player_class = MagicMock(return_value=player)
        player_class.Loops = QMediaPlayer.Loops
        monkeypatch.setattr(full_screen_window, "QMediaPlayer", player_class)
        monkeypatch.setattr(
            full_screen_window,
            "QAudioOutput",
            MagicMock(return_value=MagicMock()),
        )
        window = full_screen_window.full_screen_window(config, MagicMock())

        window.onVideoRefresh(str(tmp_path / "unsupported.mp4"))
        window.onVideoError(
            QMediaPlayer.Error.FormatError,
            "Unsupported video format",
        )

        assert window.contentLbl.text() == "Unable to play video."
        assert window.contentStack.currentWidget() is window.contentLbl
        window.close()

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