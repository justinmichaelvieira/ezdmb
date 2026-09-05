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
    config_dialog,
    full_screen_window,
    preview_window,
    simple_text_dialog,
)

_logger = logging.getLogger()

"""
Starting point of the app runtime
"""


def main():
    app, full_screen_menu, _advanced_config, _mainwin = populate_instance()
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
        """<b>File > Settings</b> to change content and cycle time.<br />
        <b>File > Exit</b> to exit the application.<br />
        <b>Help > About</b> to display version and source information.<br />
        <b>Help > Quickstart</b> to display this quickstart guide.<br />""",
    )

    config = configuration.configuration()
    config_win = config_dialog.config_dialog(config)

    def show_config():
        config_win.show()

    def show_about_window():
        about_win.show()

    def show_quickstart_window():
        quickstart_win.show()

    preview_win = preview_window.preview_window(
        config, show_config, show_about_window, show_quickstart_window
    )
    preview_win.setWindowIcon(getWindowIcon())

    def open_preview_window():
        show_and_bring_to_front(preview_win)

    full_screen_win = full_screen_window.full_screen_window(config, open_preview_window)

    full_screen_win.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    full_screen_win.showFullScreen()

    open_preview_window()
    preview_win.raise_()
    preview_win.activateWindow()

    print(f'''
ezdmb v{__version__} started with:
    Rotation: {config.RotateContent}
    RotateContentTime {config.RotateContentTime} sec
    and {config.ContentArray.__len__()} screens to rotate through.
''')
    return app, full_screen_win, config_win, preview_win


def show_and_bring_to_front(window):
    window.show()
    window.raise_()
    window.activateWindow()


if __name__ == "__main__":
    main()
