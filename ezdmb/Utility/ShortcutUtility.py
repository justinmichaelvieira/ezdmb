from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence


def setCloseOnEscKey(window):
    window.shortcut = QShortcut(QKeySequence(Qt.Key_Escape), window)
    window.shortcut.activated.connect(lambda: QApplication.quit())
