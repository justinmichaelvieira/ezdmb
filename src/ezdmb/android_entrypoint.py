"""Android-specific application startup."""

import logging
import sys

from PySide6.QtWidgets import QApplication

from ezdmb import STYLESHEET, __version__
from ezdmb.Controller.configuration import configuration
from ezdmb.Utility.android_storage_utility import android_storage_utility
from ezdmb.Utility.logging_utility import setupLogging
from ezdmb.View.android_app import android_app_window

_logger = logging.getLogger(__name__)


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Rancorsoft")
    app.setOrganizationDomain("Rancorsoft.com")
    app.setApplicationName("Digital Menu Board")
    app.setQuitOnLastWindowClosed(True)
    app.setStyleSheet(
        STYLESHEET
        + """
QPushButton {
    min-height: 48px;
    font-size: 14pt;
}

QComboBox, QDateEdit {
    min-height: 48px;
    font-size: 14pt;
}

QPushButton#androidSettingsButton {
    background-color: rgba(31, 95, 159, 235);
    border-color: #1f5f9f;
    border-radius: 12px;
    color: #ffffff;
    padding: 12px 20px;
}
"""
    )

    config = configuration()
    setupLogging()
    window = android_app_window(config, android_storage_utility())
    window.showFullScreen()
    _logger.info("ezdmb v%s Android application started.", __version__)
    sys.exit(app.exec())
