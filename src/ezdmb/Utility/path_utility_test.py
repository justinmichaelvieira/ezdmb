import os
from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import QStandardPaths

from ezdmb.Utility.path_utility import get_appdata_path


class TestPathUtility:
    def test_get_appdata_path_uses_windows_appdata(self):
        expected_path = os.path.join("/tmp/appdata", "ezdmb")

        with (
            patch("os.name", "nt"),
            patch("os.getenv", return_value="/tmp/appdata"),
        ):
            assert get_appdata_path() == expected_path

    def test_get_appdata_path_uses_home_directory_for_non_windows(self):
        home_path = Path("C:/tmp/home")

        with (
            patch("os.name", "posix"),
            patch.object(Path, "home", return_value=home_path),
        ):
            assert get_appdata_path() == str(home_path / ".ezdmb")

    def test_get_appdata_path_uses_qt_android_data_location(self):
        with (
            patch("ezdmb.Utility.path_utility.is_android", return_value=True),
            patch(
                "ezdmb.Utility.path_utility.QStandardPaths.writableLocation",
                return_value="/data/user/0/org.ezdmb/files",
            ) as writable_location,
        ):
            assert (
                get_appdata_path()
                == "/data/user/0/org.ezdmb/files"
            )

        writable_location.assert_called_once_with(
            QStandardPaths.StandardLocation.AppDataLocation
        )
