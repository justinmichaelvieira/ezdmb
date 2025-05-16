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

_styleSheet = "style.css"
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

    # apply app stylesheet
    with open(_styleSheet, "r") as f:
        css = f.read()

    app.setStyleSheet(css)

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
