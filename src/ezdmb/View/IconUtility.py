from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
import ezdmb.View.resources as resources  # noqa: F401, this is needed to load the resources.qrc file


def getWindowIcon():
    icon = QIcon()
    icon.addFile(":/images/logo_48x48.png", QSize(48, 48))
    return icon
