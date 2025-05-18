from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QShortcut
from PyQt5.QtGui import QKeySequence


def setCloseOnEscKey(window):
    window.closeOnEscShortcut = QShortcut(QKeySequence(Qt.Key_Escape), window)
    window.closeOnEscShortcut.activated.connect(lambda: QApplication.quit())


def setOpenOnOKey(window, openLambda):
    window.openOnOShortcut = QShortcut(QKeySequence(Qt.Key_O), window)
    window.openOnOShortcut.activated.connect(openLambda)
