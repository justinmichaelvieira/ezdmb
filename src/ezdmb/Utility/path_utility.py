import os
from pathlib import Path

from PySide6.QtCore import QOperatingSystemVersion, QStandardPaths


def get_appdata_path() -> str:
    """Get the path to the appdata folder for the application"""
    if os.name == "nt":
        folder = os.getenv("APPDATA")
        appdata_path = os.path.join(folder or "./", "ezdmb")
    elif is_android():
        appdata_path = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        if not appdata_path:
            raise RuntimeError(
                "Qt did not provide an Android application data directory."
            )
    else:
        appdata_path = os.path.join(str(Path.home()), ".ezdmb")

    return appdata_path


def is_android() -> bool:
    return (
        QOperatingSystemVersion.currentType()
        == QOperatingSystemVersion.OSType.Android
    )
