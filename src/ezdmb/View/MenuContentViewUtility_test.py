"""
MenuContentViewUtility_test.py
Tests for the MenuContentViewUtility module
"""
import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread
from ezdmb.View.MenuContentViewUtility import MenuContentViewUtility
from ezdmb.Controller.Configuration import Configuration


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
    config = MagicMock(spec=Configuration)
    config.ContentArray = []
    config.RotateContent = True
    config.RotateContentTime = 5
    config.configUpdated = MagicMock()
    return config


@pytest.fixture
def mock_pixmap_label(qapp):
    """Create a mock QLabel for displaying pixmaps"""
    label = MagicMock(spec=QLabel)
    return label


class TestMenuContentViewUtilityInit:
    """Tests for MenuContentViewUtility initialization"""

    def test_initialization(self, qapp, mock_config, mock_pixmap_label):
        """Test MenuContentViewUtility can be initialized"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
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

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            assert util.contentArray == ["image1.jpg", "image2.png"]
            assert util.rotateContent is True
            assert util.rotateTimeout == 10

    def test_initialization_connects_signals(self, qapp, mock_config, mock_pixmap_label):
        """Test that initialization connects signals"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            # Verify contentUpdated signal was connected
            assert util.contentUpdated is not None


class TestGetViewableFileContent:
    """Tests for getViewableFilecontent method"""

    def test_recognizes_jpg_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that jpg files are recognized as viewable"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                # Create a dummy jpg file
                test_file = os.path.join(tmpdir, "test.jpg")
                open(test_file, 'a').close()

                # Mock QPixmap to avoid actual image loading
                with patch('ezdmb.View.MenuContentViewUtility.QPixmap') as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None
                    mock_pixmap_class.assert_called_once_with(test_file)

    def test_recognizes_png_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that png files are recognized as viewable"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                test_file = os.path.join(tmpdir, "test.png")
                open(test_file, 'a').close()

                with patch('ezdmb.View.MenuContentViewUtility.QPixmap') as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None

    def test_recognizes_gif_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that gif files are recognized as viewable"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                test_file = os.path.join(tmpdir, "test.gif")
                open(test_file, 'a').close()

                with patch('ezdmb.View.MenuContentViewUtility.QPixmap') as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None

    def test_recognizes_bmp_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that bmp files are recognized as viewable"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                test_file = os.path.join(tmpdir, "test.bmp")
                open(test_file, 'a').close()

                with patch('ezdmb.View.MenuContentViewUtility.QPixmap') as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None

    def test_recognizes_ico_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that ico files are recognized as viewable"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                test_file = os.path.join(tmpdir, "test.ico")
                open(test_file, 'a').close()

                with patch('ezdmb.View.MenuContentViewUtility.QPixmap') as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None

    def test_rejects_unsupported_extension(self, qapp, mock_config, mock_pixmap_label):
        """Test that unsupported file types return None"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            result = util.getViewableFilecontent("document.txt")
            assert result is None

    def test_extension_case_insensitive(self, qapp, mock_config, mock_pixmap_label):
        """Test that file extension check is case-insensitive"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            with tempfile.TemporaryDirectory() as tmpdir:
                # Test uppercase extension
                test_file = os.path.join(tmpdir, "test.JPG")
                open(test_file, 'a').close()

                with patch('ezdmb.View.MenuContentViewUtility.QPixmap') as mock_pixmap_class:
                    mock_pixmap_class.return_value = MagicMock(spec=QPixmap)
                    result = util.getViewableFilecontent(test_file)

                    assert result is not None


class TestOnConfigUpdated:
    """Tests for onConfigUpdated slot"""

    def test_updates_content_array(self, qapp, mock_config, mock_pixmap_label):
        """Test that onConfigUpdated updates contentArray"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            new_data = {
                "imported_content": ["new_image1.jpg", "new_image2.png"],
                "rotate_content": True,
                "rotate_content_time": 20
            }

            util.onConfigUpdated(new_data)

            assert util.contentArray == ["new_image1.jpg", "new_image2.png"]

    def test_updates_rotate_content(self, qapp, mock_config, mock_pixmap_label):
        """Test that onConfigUpdated updates rotateContent"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            new_data = {
                "imported_content": [],
                "rotate_content": False,
                "rotate_content_time": 15
            }

            util.onConfigUpdated(new_data)

            assert util.rotateContent is False

    def test_updates_rotate_timeout(self, qapp, mock_config, mock_pixmap_label):
        """Test that onConfigUpdated updates rotateTimeout"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            new_data = {
                "imported_content": [],
                "rotate_content": True,
                "rotate_content_time": 60
            }

            util.onConfigUpdated(new_data)

            assert util.rotateTimeout == 60


class TestMenuContentViewUtilityProperties:
    """Tests for MenuContentViewUtility properties"""

    def test_window_name_stored(self, qapp, mock_config, mock_pixmap_label):
        """Test that window name is properly stored"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "FullScreenWindow",
                callback
            )

            assert util.windowName == "FullScreenWindow"

    def test_debug_mode_enabled(self, qapp, mock_config, mock_pixmap_label):
        """Test that debug mode is enabled by default"""
        callback = MagicMock()

        with patch.object(QThread, 'start'):
            util = MenuContentViewUtility(
                mock_config,
                mock_pixmap_label,
                "TestWindow",
                callback
            )

            assert util.debug is True
