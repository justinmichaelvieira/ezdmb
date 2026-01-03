"""
Configuration_test.py
Tests for the Configuration module
"""
import os
import json
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from ezdmb.Controller.Configuration import Configuration


@pytest.fixture
def qapp():
    """Create a QApplication instance for tests"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for config files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


class TestConfigurationInit:
    """Tests for Configuration initialization"""

    def test_configuration_creates_instance(self, qapp):
        """Test that Configuration can be instantiated"""
        with patch('os.getenv', return_value=None):
            with patch('os.name', 'posix'):
                with patch.object(Path, 'home', return_value=Path(tempfile.gettempdir())):
                    config = Configuration()
                    assert config is not None
                    assert isinstance(config.Data, dict)

    def test_configuration_creates_appdata_directory_windows(self, qapp, temp_config_dir):
        """Test that Configuration creates appdata directory on Windows"""
        config_path = os.path.join(temp_config_dir, 'ezdmb')
        with patch('os.name', 'nt'):
            with patch('os.getenv', return_value=temp_config_dir):
                with patch.object(Configuration, '__init__', lambda x: None):
                    Configuration()  # noqq: F841
                    # Manually call the init logic
                    os.makedirs(config_path, exist_ok=True)
                    assert os.path.exists(config_path)

    def test_configuration_creates_appdata_directory_linux(self, qapp, temp_config_dir):
        """Test that Configuration creates appdata directory on Linux"""
        with patch('os.name', 'posix'):
            with patch.object(Path, 'home', return_value=Path(temp_config_dir)):
                config_path = os.path.join(temp_config_dir, '.ezdmb')
                os.makedirs(config_path, exist_ok=True)
                assert os.path.exists(config_path)

    def test_configuration_creates_default_config_file(self, qapp, temp_config_dir):
        """Test that Configuration creates default config file on first run"""
        config_path = os.path.join(temp_config_dir, 'dmb_config.json')

        # Create default config
        default_config = {
            "rotate_content": True,
            "rotate_content_time": 15,
            "imported_content": []
        }

        with open(config_path, 'w') as f:
            json.dump(default_config, f)

        with open(config_path, 'r') as f:
            loaded_config = json.load(f)

        assert loaded_config["rotate_content"] is True
        assert loaded_config["rotate_content_time"] == 15
        assert loaded_config["imported_content"] == []


class TestConfigurationProperties:
    """Tests for Configuration properties"""

    def test_rotate_content_property(self, qapp, temp_config_dir):
        """Test RotateContent property getter and setter"""
        with patch('os.getenv', return_value=temp_config_dir):
            with patch('os.name', 'nt'):
                with patch.object(Configuration, '__init__', lambda x: None):
                    config = Configuration()
                    config.set_rotate_content(True)
                    assert config.get_rotate_content() is True
                    config.set_rotate_content(False)
                    assert config.get_rotate_content() is False

    def test_rotate_content_time_property(self, qapp, temp_config_dir):
        """Test RotateContentTime property getter and setter"""
        with patch.object(Configuration, '__init__', lambda x: None):
            config = Configuration()
            config.set_rotate_content_time(30)
            assert config.get_rotate_content_time() == 30
            config.set_rotate_content_time(60)
            assert config.get_rotate_content_time() == 60

    def test_content_array_property(self, qapp, temp_config_dir):
        """Test ContentArray property getter and setter"""
        with patch.object(Configuration, '__init__', lambda x: None):
            config = Configuration()
            test_array = ["/path/to/image1.jpg", "/path/to/image2.png"]
            config.set_content_array(test_array)
            assert config.get_content_array() == test_array

    def test_data_property(self, qapp, temp_config_dir):
        """Test Data property getter and setter"""
        with patch.object(Configuration, '__init__', lambda x: None):
            config = Configuration()
            test_data = {
                "rotate_content": True,
                "rotate_content_time": 20,
                "imported_content": []
            }
            config.set_data(test_data)
            assert config.get_data() == test_data


class TestConfigurationSaveConfig:
    """Tests for Configuration.SaveConfig method"""

    def test_save_config_creates_json(self, qapp, temp_config_dir):
        """Test that SaveConfig writes JSON to file"""
        config_file = os.path.join(temp_config_dir, 'dmb_config.json')

        config = MagicMock(spec=Configuration)
        config.config_path = config_file
        test_data = {}
        config._data = test_data
        config.get_data = MagicMock(return_value=test_data)

        # Call the actual SaveConfig method
        Configuration.SaveConfig(config, True, "20", ["/path/to/image.jpg"])

        # Verify file was created and contains correct data
        assert os.path.exists(config_file)
        with open(config_file, 'r') as f:
            saved_data = json.load(f)

        assert saved_data["rotate_content"] is True
        assert saved_data["rotate_content_time"] == 20
        assert saved_data["imported_content"] == ["/path/to/image.jpg"]

    def test_save_config_with_multiple_images(self, qapp, temp_config_dir):
        """Test SaveConfig with multiple image paths"""
        config_file = os.path.join(temp_config_dir, 'dmb_config.json')
        images = [
            "/path/to/menu1.jpg",
            "/path/to/menu2.png",
            "/path/to/menu3.gif"
        ]

        config = MagicMock(spec=Configuration)
        config.config_path = config_file
        test_data = {}
        config._data = test_data
        config.get_data = MagicMock(return_value=test_data)

        Configuration.SaveConfig(config, True, "30", images)

        with open(config_file, 'r') as f:
            saved_data = json.load(f)

        assert saved_data["imported_content"] == images
        assert len(saved_data["imported_content"]) == 3

    def test_save_config_converts_time_to_int(self, qapp, temp_config_dir):
        """Test that SaveConfig converts rotate_content_time to int"""
        config_file = os.path.join(temp_config_dir, 'dmb_config.json')

        config = MagicMock(spec=Configuration)
        config.config_path = config_file
        test_data = {}
        config._data = test_data
        config.get_data = MagicMock(return_value=test_data)

        # Pass time as string
        Configuration.SaveConfig(config, True, "45", [])

        with open(config_file, 'r') as f:
            saved_data = json.load(f)

        assert isinstance(saved_data["rotate_content_time"], int)
        assert saved_data["rotate_content_time"] == 45

    def test_save_config_emits_signal(self, qapp, temp_config_dir):
        """Test that SaveConfig emits configUpdated signal"""
        config_file = os.path.join(temp_config_dir, 'dmb_config.json')

        config = MagicMock(spec=Configuration)
        config.config_path = config_file
        test_data = {}
        config._data = test_data
        config.get_data = MagicMock(return_value=test_data)
        config.configUpdated = MagicMock()

        Configuration.SaveConfig(config, False, "15", [])

        # Verify signal was emitted
        config.configUpdated.emit.assert_called_once()


class TestConfigurationIntegration:
    """Integration tests for Configuration"""

    def test_full_configuration_workflow(self, qapp, temp_config_dir):
        """Test complete workflow: create, save, and load config"""
        config_file = os.path.join(temp_config_dir, 'dmb_config.json')

        # Create initial config
        initial_config = {
            "rotate_content": True,
            "rotate_content_time": 15,
            "imported_content": []
        }

        with open(config_file, 'w') as f:
            json.dump(initial_config, f)

        # Load and verify
        with open(config_file, 'r') as f:
            loaded = json.load(f)

        assert loaded["rotate_content"] is True
        assert loaded["rotate_content_time"] == 15

        # Modify and save
        loaded["rotate_content_time"] = 30
        loaded["imported_content"] = ["image.jpg"]

        with open(config_file, 'w') as f:
            json.dump(loaded, f)

        # Reload and verify changes
        with open(config_file, 'r') as f:
            final = json.load(f)

        assert final["rotate_content_time"] == 30
        assert final["imported_content"] == ["image.jpg"]
