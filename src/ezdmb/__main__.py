"""
main.py
DMB startup script
Justin Vieira [justin@rancorsoft.com] / Richard Haynes / Adam Brody
Rancorsoft, LLC
"""
# pylint: disable=no-name-in-module, c-extension-no-member, missing-function-docstring, missing-class-docstring, unused-variable
import logging
import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication

from ezdmb.Controller import Configuration
from ezdmb.Controller.LoggingUtility import setupLogging
from ezdmb.View import AboutDialog, FullScreenWindow, ConfigDialog, PreviewWindow

STYLESHEET = """
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

"""
Starting point of the app runtime
"""


def main():
    app, full_screen_menu, advanced_config, mainwin = populateInstance()
    setupLogging()
    # store screen geometry
    screenWidth = full_screen_menu.frameGeometry().width()
    screenHeight = full_screen_menu.frameGeometry().height()
    # size and show menu
    full_screen_menu.contentLbl.resize(screenWidth, screenHeight)
    # without this, the script exits immediately.
    _logger.info("DMB Application started.")
    sys.exit(app.exec_())


def populateInstance():
    app = QApplication(sys.argv)
    app.setOrganizationName("Rancorsoft")
    app.setOrganizationDomain("Rancorsoft.com")
    app.setApplicationName("Digital Menu Board")

    app.setStyleSheet(STYLESHEET)

    about_win = AboutDialog.AboutDialog()

    config = Configuration.Configuration()
    config_win = ConfigDialog.ConfigDialog(config)

    def show_config():
        config_win.show()

    def show_about_window():
        about_win.show()

    preview_win = PreviewWindow.PreviewWindow(config, show_config, show_about_window)
    preview_win.setWindowIcon(QtGui.QIcon(":/logo_256x256.jpg"))

    def open_preview_window():
        show_and_bring_to_front(preview_win)

    full_screen_win = FullScreenWindow.FullScreenWindow(config, open_preview_window)

    full_screen_win.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    full_screen_win.showFullScreen()

    open_preview_window()
    preview_win.raise_()
    preview_win.activateWindow()
    return app, full_screen_win, config_win, preview_win


def show_and_bring_to_front(window):
    window.show()
    window.raise_()
    window.activateWindow()


if __name__ == "__main__":
    main()
