# main.py
# DMB startup script
# Justin Vieira [justin@rancorsoft.com] / Richard Haynes / Adam Brody
# Rancorsoft, LLC 2016

# import argparse  # Cmd line option lib
import logging
import sys
import os.path as osp

from PyQt5 import QtCore, QtNetwork, QtGui
from PyQt5.QtWidgets import QApplication
import pyqt5ac

from Controller import Configuration, Backend
from Controller.LoggingUtility import setupLogging
from View import FullScreenWindow, MainWindow, ConfigDialog

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
    fullScreenMenu.label_pic.resize(screenWidth, screenHeight)
    Backend.Backend()
    # without this, the script exits immediately.
    logger.info("DMB Application started.")
    sys.exit(app.exec_())


def populateInstance():
    # Todo: It's probably safer to just host a local webserver for content.
    # For now --disable-web-security allows local files in our html.
    sys.argv.append("--disable-web-security")
    app = QApplication(sys.argv)
    app.setOrganizationName("Rancorsoft")
    app.setOrganizationDomain("Rancorsoft.com")
    app.setApplicationName("Digital Menu Board")

    # read and apply app stylesheet
    with open(styleSheet, "r") as f:
        css = f.read()
    app.setStyleSheet(css)

    QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)

    config = Configuration.Configuration()
    fullScreenMenu = FullScreenWindow.FullScreenWindow(config)
    mainwin = MainWindow.MainWindow(config)

    mainwin.setWindowIcon(
        QtGui.QIcon(osp.join(osp.dirname(__file__), "Images/logo_256x256.jpg"))
    )
    mainwin.show()

    advancedConfig = ConfigDialog.ConfigDialog(config)
    advancedConfig.use_images_check.setChecked(config.UseImages == "true")
    advancedConfig.use_html_file_check.setChecked(config.UseHTML == "true")
    advancedConfig.use_menu_data_check.setChecked(config.UseImported == "true")
    advancedConfig.rotate_images_check.setChecked(config.RotateContent == "true")
    advancedConfig.rotateTimeBox.setValue(float(config.RotateContentTime))

    fullScreenMenu.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    fullScreenMenu.showFullScreen()
    
    mainwin.pushButton_2.clicked.connect(lambda: showAdvConfig(advancedConfig))
    mainwin.raise_()
    mainwin.activateWindow()
    return app, fullScreenMenu, advancedConfig, mainwin


def showAdvConfig(advancedConfig):
    advancedConfig.setUiFromConfig()
    advancedConfig.show()


if __name__ == "__main__":
    main()
