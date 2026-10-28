"""
menu_content_view_test.py
Tests for the menu_content_view module
"""

import os
import tempfile
from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QThread
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel

from ezdmb.Controller import configuration
from ezdmb.Controller.configuration import (
    default_content_groups,
    default_time_blocks,
)
from ezdmb.View import full_screen_window, menu_content_view


@pytest.fixture
def qapp():
    """Create a QApplication instance for tests"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def mock_config(qapp):
    """Create a mock Configuration object"""
    config = MagicMock(spec=configuration.configuration)
    config.ContentArray = []
    config.ContentGroups = default_content_groups()
    config.TimeBlocks = default_time_blocks()
    config.RotateContent = True
    config.RotationMode = "interval"
    config.RotateContentTime = 5
    config.configUpdated = MagicMock()
    return config


@pytest.fixture
def mock_pixmap_label(qapp):
    """Create a mock QLabel for displaying pixmaps"""
    label = MagicMock(spec=QLabel)
    return label


class test_menu_content_view_init:
    """Tests for menu_content_view initialization"""

    def test_initialization(self, qapp, mock_config, mock_pixmap_label):
        """Test menu_content_view can be initialized"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            assert util is not None
            assert util._config == mock_config
            assert util.windowName == "TestWindow"
            assert util.debug is True

    def test_initialization_sets_properties(self, qapp, mock_config, mock_pixmap_label):
        """Test that initialization sets content properties from config"""
        mock_config.ContentArray = ["image1.jpg", "image2.png"]
        mock_config.RotateContent = True
        mock_config.RotateContentTime = 10
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            assert util.contentArray == ["image1.jpg", "image2.png"]
            assert util.rotateContent is True
            assert util.rotateTimeout == 10

    def test_initialization_connects_signals(
        self, qapp, mock_config, mock_pixmap_label
    ):
        """Test that initialization connects signals"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            # Verify contentUpdated signal was connected
            assert util.contentUpdated is not None


class TestMenuContentViewShutdown:
    def test_stop_interrupts_rotation_wait(self, qapp, mock_config):
        mock_config.RotateContentTime = 3600
        worker = menu_content_view.menu_content_view(
            mock_config, QLabel(), "TestWindow", MagicMock()
        )

        worker.stop()

        assert not worker.isRunning()

    def test_application_shutdown_stops_display_worker(self, qapp, mock_config):
        mock_config.RotateContentTime = 3600
        window = full_screen_window.full_screen_window(mock_config, MagicMock())

        qapp.aboutToQuit.emit()

        assert not window.contentViewUtil.isRunning()


class TestGetViewableFileContent:
    """Tests for getViewableFilecontent method"""

    def test_recognizes_jpg_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that jpg files are recognized as viewable"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                # Create a dummy jpg file
                test_file = os.path.join(tmpdir, "test.jpg")
                open(test_file, "a").close()

                # Mock QPixmap to avoid actual image loading
                with patch("ezdmb.View.menu_content_view.QPixmap") as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None
                    mock_pixmap_class.assert_called_once_with(test_file)

    def test_recognizes_png_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that png files are recognized as viewable"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                test_file = os.path.join(tmpdir, "test.png")
                open(test_file, "a").close()

                with patch("ezdmb.View.menu_content_view.QPixmap") as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None

    def test_recognizes_gif_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that gif files are recognized as viewable"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                test_file = os.path.join(tmpdir, "test.gif")
                open(test_file, "a").close()

                with patch("ezdmb.View.menu_content_view.QPixmap") as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None

    def test_recognizes_bmp_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that bmp files are recognized as viewable"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                test_file = os.path.join(tmpdir, "test.bmp")
                open(test_file, "a").close()

                with patch("ezdmb.View.menu_content_view.QPixmap") as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None

    def test_recognizes_ico_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that ico files are recognized as viewable"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                test_file = os.path.join(tmpdir, "test.ico")
                open(test_file, "a").close()

                with patch("ezdmb.View.menu_content_view.QPixmap") as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None

    def test_rejects_unsupported_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that unsupported file types return None"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            result = util.getViewableFilecontent("document.psf")
            assert result is None

    def test_display_index_emits_video_path(self, qapp, mock_config, mock_pixmap_label):
        callback = MagicMock()
        video_callback = MagicMock()
        video_path = "menu-video.MP4"

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback,
                video_callback,
            )
            index = util.display_index(0, [video_path])

        assert index == 0
        video_callback.assert_called_once_with(video_path)
        callback.assert_not_called()
        mock_pixmap_label.setPixmap.assert_not_called()

    def test_extension_case_insensitive(self, qapp, mock_config, mock_pixmap_label):
        """Test that file extension check is case-insensitive"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                # Test uppercase extension
                test_file = os.path.join(tmpdir, "test.JPG")
                open(test_file, "a").close()

                with patch("ezdmb.View.menu_content_view.QPixmap") as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None


class TestOnConfigUpdated:
    """Tests for onConfigUpdated slot"""

    def test_updates_content_array(self, qapp, mock_config, mock_pixmap_label):
        """Test that onConfigUpdated updates contentArray"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            new_data = {
                "imported_content": ["new_image1.jpg", "new_image2.png"],
                "rotate_content": True,
                "rotate_content_time": 20,
            }

            util.onConfigUpdated(new_data)

            assert util.contentArray == ["new_image1.jpg", "new_image2.png"]

    def test_updates_rotate_content(self, qapp, mock_config, mock_pixmap_label):
        """Test that onConfigUpdated updates rotateContent"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            new_data = {
                "imported_content": [],
                "rotate_content": False,
                "rotate_content_time": 15,
            }

            util.onConfigUpdated(new_data)

            assert util.rotateContent is False

    def test_updates_rotate_timeout(self, qapp, mock_config, mock_pixmap_label):
        """Test that onConfigUpdated updates rotateTimeout"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            new_data = {
                "imported_content": [],
                "rotate_content": True,
                "rotate_content_time": 60,
            }

            util.onConfigUpdated(new_data)

            assert util.rotateTimeout == 60

    def test_updates_rotation_mode_groups_and_schedule(
        self, qapp, mock_config, mock_pixmap_label
    ):
        callback = MagicMock()
        groups = [
            {
                "id": "breakfast",
                "name": "Breakfast",
                "content": ["breakfast.png"],
            }
        ]
        time_blocks = {
            "repeat": "Daily",
            "daily": [
                {
                    "start": "06:00",
                    "end": "11:00",
                    "group_id": "breakfast",
                }
            ],
            "weekly": {},
            "dated": {},
        }

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback,
            )
            util.onConfigUpdated(
                {
                    "imported_content": ["breakfast.png"],
                    "content_groups": groups,
                    "rotation_mode": "schedule",
                    "time_blocks": time_blocks,
                    "rotate_content": False,
                    "rotate_content_time": 15,
                }
            )

        assert util.rotationMode == "schedule"
        assert util.rotateContent is False
        assert util.contentGroups == groups
        assert util.timeBlocks == time_blocks


class TestScheduledGroupSelection:
    def test_daily_schedule_selects_matching_group(
        self, qapp, mock_config, mock_pixmap_label
    ):
        mock_config.RotationMode = "schedule"
        mock_config.ContentGroups = [
            {
                "id": "breakfast",
                "name": "Breakfast",
                "content": ["breakfast.png"],
            },
            {
                "id": "lunch",
                "name": "Lunch",
                "content": ["lunch.png"],
            },
        ]
        mock_config.TimeBlocks = {
            "repeat": "Daily",
            "daily": [
                {
                    "start": "06:00",
                    "end": "11:00",
                    "group_id": "breakfast",
                },
                {
                    "start": "11:00",
                    "end": "15:00",
                    "group_id": "lunch",
                },
            ],
            "weekly": {},
            "dated": {},
        }

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                MagicMock(),
            )

        assert (
            util.getScheduledGroup(
                datetime(2026, 10, 22, 8, 0, tzinfo=UTC)
            )["id"]
            == "breakfast"
        )
        assert (
            util.getScheduledGroup(
                datetime(2026, 10, 22, 11, 0, tzinfo=UTC)
            )["id"]
            == "lunch"
        )
        assert (
            util.getScheduledGroup(
                datetime(2026, 10, 22, 15, 0, tzinfo=UTC)
            )
            is None
        )

    def test_weekly_and_dated_schedules_select_groups(
        self, qapp, mock_config, mock_pixmap_label
    ):
        mock_config.RotationMode = "schedule"
        mock_config.ContentGroups = [
            {"id": "dinner", "name": "Dinner", "content": ["dinner.png"]}
        ]
        mock_config.TimeBlocks = {
            "repeat": "Weekly",
            "daily": [],
            "weekly": {
                "Thursday": [
                    {
                        "start": "17:00",
                        "end": "22:00",
                        "group_id": "dinner",
                    }
                ]
            },
            "dated": {
                "2026-10-23": [
                    {
                        "start": "00:00",
                        "end": "24:00",
                        "group_id": "dinner",
                    }
                ]
            },
        }

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                MagicMock(),
            )

        assert (
            util.getScheduledGroup(
                datetime(2026, 10, 22, 18, 0, tzinfo=UTC)
            )["id"]
            == "dinner"
        )

        util.timeBlocks["repeat"] = "None"
        assert (
            util.getScheduledGroup(
                datetime(2026, 10, 23, 12, 0, tzinfo=UTC)
            )["id"]
            == "dinner"
        )

    def test_first_group_wins_overlapping_schedule_blocks(
        self, qapp, mock_config, mock_pixmap_label
    ):
        mock_config.RotationMode = "schedule"
        mock_config.ContentGroups = [
            {"id": "breakfast", "name": "Breakfast", "content": []},
            {"id": "lunch", "name": "Lunch", "content": []},
        ]
        mock_config.TimeBlocks = {
            "repeat": "Daily",
            "daily": [
                {
                    "start": "08:00",
                    "end": "10:00",
                    "group_id": "lunch",
                },
                {
                    "start": "08:00",
                    "end": "10:00",
                    "group_id": "breakfast",
                },
            ],
            "weekly": {},
            "dated": {},
        }

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                MagicMock(),
            )

        assert (
            util.getScheduledGroup(
                datetime(2026, 10, 22, 9, 0, tzinfo=UTC)
            )["id"]
            == "breakfast"
        )


class test_menu_content_view_utility_properties:
    """Tests for menu_content_view_utility properties"""

    def test_window_name_stored(self, qapp, mock_config, mock_pixmap_label):
        """Test that window name is properly stored"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "FullScreenWindow", callback
            )

            assert util.windowName == "FullScreenWindow"

    def test_debug_mode_enabled(self, qapp, mock_config, mock_pixmap_label):
        """Test that debug mode is enabled by default"""
        callback = MagicMock()

        with patch.object(QThread, "start"):
            util = menu_content_view.menu_content_view(
                mock_config, mock_pixmap_label, "TestWindow", callback
            )

            assert util.debug is True
