# main.py
# DMB startup script
# Justin Vieira [justin@rancorsoft.com] / Richard Haynes / Adam Brody
# Rancorsoft, LLC

import logging
import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication

from ezdmb.Controller import Configuration
from ezdmb.Controller.LoggingUtility import setupLogging
from ezdmb.View import AboutDialog, FullScreenWindow, ConfigDialog, PreviewWindow

_styleSheet = """
* {
    border-color: #2b2b2b;
    font-size: 13px;
    alternate-background-color: #3c3f41;
}

QPushButton::pressed {
    background: #303F9F;
    color: #448AFF;
}

QToolButton {
    color: #FFFFFF;
}

QLineEdit[accessibleName="selectedFileEdit"] {
    color: #757575;
}

QScrollArea {
    background: #ffffff;
}

QToolButton {
    background: #303F9F;
    border: 0;
}

QFrame[accessibleName="navHeaderFrame"] {
    background: #303F9F;
}

QLabel[accessibleName="titleBar"] {
    background: #3F51B5;
    color: #FFFFFF;
}

QFrame {
    border: none;
}

QScrollArea {
    color: #bbbbbb;
    background-color: #3c3f41;
    border: none;
    border-top: 1px solid #2b2b2b;
    selection-background-color: #2f65ca;
    selection-color: #bbbbbb;
}
QDialog QScrollArea {
    border-top: none;
    border: none;
}

QPlainTextEdit {
    background-color: #2b2b2b;
    border: none;
    color: #bbbbbb;
    selection-background-color: #2f65ca;
}

QGraphicsView {
    background-color: #3c3f41;
    border-color: #2b2b2b;
    color: #bbbbbb;
}
"""
_logger = logging.getLogger()


# starting point of the app runtime
def main():
    app, fullScreenMenu, _advancedConfig, _mainwin = populateInstance()
    setupLogging()
    # store screen geometry
    screenWidth = fullScreenMenu.frameGeometry().width()
    screenHeight = fullScreenMenu.frameGeometry().height()
    # size and show menu
    fullScreenMenu.contentLbl.resize(screenWidth, screenHeight)
    # without this, the script exits immediately.
    _logger.info("DMB Application started.")
    sys.exit(app.exec_())


def populateInstance():
    app = QApplication(sys.argv)
    app.setOrganizationName("Rancorsoft")
    app.setOrganizationDomain("Rancorsoft.com")
    app.setApplicationName("Digital Menu Board")

    app.setStyleSheet(_styleSheet)

    _aboutWin = AboutDialog.AboutDialog()

    _config = Configuration.Configuration()
    _configWin = ConfigDialog.ConfigDialog(_config)

    def showConfig():
        _configWin.show()

    def showAboutWindow():
        _aboutWin.show()

    _previewWin = PreviewWindow.PreviewWindow(_config, showConfig, showAboutWindow)
    _previewWin.setWindowIcon(QtGui.QIcon(":/logo_256x256.jpg"))

    def openPreviewWindow():
        showAndBringToFront(_previewWin)

    _fullScreenWin = FullScreenWindow.FullScreenWindow(_config, openPreviewWindow)

    _fullScreenWin.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    _fullScreenWin.showFullScreen()

    openPreviewWindow()
    _previewWin.raise_()
    _previewWin.activateWindow()
    return app, _fullScreenWin, _configWin, _previewWin


def showAndBringToFront(window):
    window.show()
    window.raise_()
    window.activateWindow()


if __name__ == "__main__":
    main()
