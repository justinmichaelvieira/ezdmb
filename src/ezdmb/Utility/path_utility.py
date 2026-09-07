import os
from pathlib import Path


def get_appdata_path() -> str:
    """Get the path to the appdata folder for the application"""
    if os.name == "nt":
        appdata_path = os.path.join(os.getenv("APPDATA"), "ezdmb")
    else:
        appdata_path = os.path.join(str(Path.home()), ".ezdmb")

    return appdata_path
