"""
main.py
DMB startup script
Justin Vieira [justin@rancorsoft.com] / Richard Haynes / Adam Brody
Rancorsoft, LLC
"""

# pylint: disable=no-name-in-module, c-extension-no-member, missing-function-docstring, missing-class-docstring, unused-variable
import logging
import sys

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication

from ezdmb import STYLESHEET, __version__
from ezdmb.Controller import configuration
from ezdmb.Utility.icon_utility import getWindowIcon
from ezdmb.Utility.logging_utility import setupLogging
from ezdmb.View import (
    config_window,
    full_screen_window,
    simple_text_dialog,
)

_logger = logging.getLogger()

"""
Starting point of the app runtime
"""


def main():
    app, full_screen_menu, _mainwin = populate_instance()
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

    about_win = simple_text_dialog.simple_text_dialog(
        "About ezdmb",
        f"""<p><b>ezdmb v{__version__}
        </p><p>Github: <a href='https://github.com/justinmichaelvieira/ezdmb'>
        https://github.com/justinmichaelvieira/ezdmb</a></p>""",
    )

    quickstart_win = simple_text_dialog.simple_text_dialog(
        "Quickstart Guide",
        """<b>File > Exit</b> to exit the application.<br />
        <b>Help > About</b> to display version and source information.<br />
        <b>Help > Quickstart</b> to display this quickstart guide.<br />""",
    )

    config = configuration.configuration()

    def show_about_window():
        about_win.show()

    def show_quickstart_window():
        quickstart_win.show()

    config_win = config_window.config_window(
        config, show_about_window, show_quickstart_window
    )
    config_win.setWindowIcon(getWindowIcon())

    def open_preview_window():
        show_and_bring_to_front(config_win)

    full_screen_win = full_screen_window.full_screen_window(config, open_preview_window)

    full_screen_win.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
    full_screen_win.showFullScreen()

    open_preview_window()
    config_win.raise_()
    config_win.activateWindow()

    print(f"""
ezdmb v{__version__} started with:
    - Rotation: {config.RotateContent}
    - RotateContentTime: {config.RotateContentTime}s
    - Total Content Screens: {config.ContentArray.__len__()}
""")
    return app, full_screen_win, config_win


def show_and_bring_to_front(window):
    window.show()
    window.raise_()
    window.activateWindow()


if __name__ == "__main__":
    main()
