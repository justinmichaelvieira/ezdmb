# pylint: disable=no-name-in-module
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QKeySequence, QShortcut


def setCloseOnEscKey(window):
    window.closeOnEscShortcut = QShortcut(QKeySequence(Qt.Key_Escape), window)
    window.closeOnEscShortcut.activated.connect(lambda: QApplication.quit())


def setOpenOnOKey(window, openLambda):
    window.openOnOShortcut = QShortcut(QKeySequence(Qt.Key_O), window)
    window.openOnOShortcut.activated.connect(openLambda)
