"""
main.py
DMB startup script
Justin Vieira [justin@rancorsoft.com] / Richard Haynes / Adam Brody
Rancorsoft, LLC
"""

# pylint: disable=no-name-in-module, c-extension-no-member, missing-function-docstring, missing-class-docstring, unused-variable
import logging
import sys

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QApplication

from ezdmb import __version__, STYLESHEET
from ezdmb.Controller import Configuration
from ezdmb.Controller.LoggingUtility import setupLogging
from ezdmb.View import FullScreenWindow, ConfigDialog, PreviewWindow, SimpleTextDialog
from PySide6.QtGui import QIcon, QPixmap

_logger = logging.getLogger()

"""
Starting point of the app runtime
"""


def main():
    app, full_screen_menu, advanced_config, mainwin = populate_instance()
    setupLogging()
    # store screen geometry
    screen_width = full_screen_menu.frameGeometry().width()
    screen_height = full_screen_menu.frameGeometry().height()
    # size and show menu
    full_screen_menu.contentLbl.resize(screen_width, screen_height)
    # without this, the script exits immediately.
    _logger.info("DMB Application started.")
    sys.exit(app.exec())


def populate_instance():
    app = QApplication(sys.argv)
    app.setOrganizationName("Rancorsoft")
    app.setOrganizationDomain("Rancorsoft.com")
    app.setApplicationName("Digital Menu Board")

    app.setStyleSheet(STYLESHEET)

    about_win = SimpleTextDialog.SimpleTextDialog(
        "About ezdmb",
        f"""<p><b>ezdmb v{__version__}
        </p><p>Github: <a href='https://github.com/justinmichaelvieira/ezdmb'>
        https://github.com/justinmichaelvieira/ezdmb</a></p>""",
    )

    quickstart_win = SimpleTextDialog.SimpleTextDialog(
        "Quickstart Guide",
        """        On app start, both the Main (fullscreen) and Preview/Configuration<br />
        windows are shown on the desktop. The Settings window can be closed with the<br />
        "X" icon at top right of the window. The 'Esc' key is used to exit the application.<br />
        Clicking or tapping the Main window and then pressing the 'o' key will reopen the<br />
        Preview/Configuration window.<br />""",
    )

    config = Configuration.Configuration()
    config_win = ConfigDialog.ConfigDialog(config)

    def show_config():
        config_win.show()

    def show_about_window():
        about_win.show()

    def show_quickstart_window():
        quickstart_win.show()

    preview_win = PreviewWindow.PreviewWindow(
        config, show_config, show_about_window, show_quickstart_window
    )
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
