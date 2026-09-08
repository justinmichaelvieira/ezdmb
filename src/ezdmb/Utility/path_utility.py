import os
from pathlib import Path


def get_appdata_path() -> str:
    """Get the path to the appdata folder for the application"""
    if os.name == "nt":
        folder = os.getenv("APPDATA")
        appdata_path = os.path.join(folder or "./", "ezdmb")
    else:
        appdata_path = os.path.join(str(Path.home()), ".ezdmb")

    return appdata_path
