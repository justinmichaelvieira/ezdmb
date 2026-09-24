from pathlib import Path
import os
from unittest.mock import patch
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
