from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from ezdmb.View import resources  # noqa: F401, this is needed to load the resources.qrc file


def getWindowIcon():
    icon = QIcon()
    icon.addFile(":/images/logo_48x48.png", QSize(48, 48))
    return icon


def getIcon(icon_path):
    icon = QIcon()
    icon.addFile(f":/images/{icon_path}", QSize(48, 48))
    return icon
