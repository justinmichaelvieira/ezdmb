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

styleSheet = "style.css"
logger = logging.getLogger()


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
    logger.info("DMB Application started.")
    sys.exit(app.exec_())


def populateInstance():
    app = QApplication(sys.argv)
    app.setOrganizationName("Rancorsoft")
    app.setOrganizationDomain("Rancorsoft.com")
    app.setApplicationName("Digital Menu Board")

    # read and apply app stylesheet
    with open(styleSheet, "r") as f:
        css = f.read()

    app.setStyleSheet(css)

    config = Configuration.Configuration()
    fullScreenWin = FullScreenWindow.FullScreenWindow(config)
    previewWin = PreviewWindow.MainWindow(config)

    previewWin.setWindowIcon(
        QtGui.QIcon(":/logo_256x256.jpg")
    )
    previewWin.show()

    configWin = ConfigDialog.ConfigDialog(config)

    fullScreenWin.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    fullScreenWin.showFullScreen()

    previewWin.editDisplaySettingsAction.triggered.connect(lambda: showConfig(configWin))
    previewWin.exitAction.triggered.connect(lambda: sys.exit())
    previewWin.raise_()
    previewWin.activateWindow()
    return app, fullScreenWin, configWin, previewWin


def showConfig(win):
    win.show()


if __name__ == "__main__":
    main()
