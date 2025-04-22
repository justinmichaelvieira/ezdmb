# main.py
# DMB startup script
# Justin Vieira [justin@rancorsoft.com] / Richard Haynes / Adam Brody
# Rancorsoft, LLC

import logging
import sys

from PyQt5 import QtCore, QtNetwork, QtGui
from PyQt5.QtWidgets import QApplication

from ezdmb.Controller import Configuration
from ezdmb.Controller.LoggingUtility import setupLogging
from ezdmb.View import FullScreenWindow, ConfigDialog, PreviewWindow

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

    # read and apply app stylesheet
    with open(_styleSheet, "r") as f:
        css = f.read()

    app.setStyleSheet(css)

    # child windows
    _config = Configuration.Configuration()
    _previewWin = PreviewWindow.PreviewWindow(_config)
    _configWin = ConfigDialog.ConfigDialog(_config)

    _previewWin.setWindowIcon(
        QtGui.QIcon(":/logo_256x256.jpg")
    )
    # allow preview window to be reopened with 'o' key
    previewWindowOpenLambda = lambda: showAndBringToFront(_previewWin)
    _fullScreenWin = FullScreenWindow.FullScreenWindow(_config, previewWindowOpenLambda)

    # show preview window on load
    previewWindowOpenLambda()

    _fullScreenWin.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    _fullScreenWin.showFullScreen()

    showConfigAction = lambda: _configWin.show()
    _previewWin.editDisplaySettingsAction.triggered.connect(showConfigAction)
    _previewWin.exitAction.triggered.connect(lambda: sys.exit())
    _previewWin.raise_()
    _previewWin.activateWindow()
    return app, _fullScreenWin, _configWin, _previewWin

def showAndBringToFront(window):
    window.show()
    window.raise_()
    window.activateWindow()

if __name__ == "__main__":
    main()
