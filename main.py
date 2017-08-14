# main.py
# DMB startup script
# Justin Vieira [justin@rancorsoft.com] / Richard Haynes / Adam Brody
# Rancorsoft, LLC 2016

import argparse  # Cmd line option lib
import sys
import os.path as osp
from PyQt5 import QtCore, QtNetwork, QtGui
from PyQt5.QtWidgets import *
from Controller import Configuration
from View import FullScreenWindow, MainWindow, ConfigDialog

# This is a required defined class for argparse -JV
class CmdArgs:
    pass

# starting point of the app runtime
def main():
    # a new app instance
    app, fullScreenMenu, advancedConfig, mainwin = populateInstance()
    # store screen geometry
    screenWidth = fullScreenMenu.frameGeometry().width()
    screenHeight = fullScreenMenu.frameGeometry().height()
    #size and show menu
    fullScreenMenu.label_pic.resize(screenWidth, screenHeight)
    parseCmdLineArgs(screenHeight, screenWidth)
    # without this, the script exits immediately.
    sys.exit(app.exec_())

def parseCmdLineArgs(screenHeight, screenWidth):
    # command line option setup and processing
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-x', '--xpos', help='X Position of window', type=int, default=0)
    argparser.add_argument('-y', '--ypos', help='Y position of window', type=int, default=0)
    argparser.add_argument('-sw', '--width', help='Width of window', type=int, default=screenWidth)
    argparser.add_argument('-sh', '--height', help='Height of window', type=int, default=screenHeight)
    args = vars(argparser.parse_args())
    return args

def populateInstance():
    app = QApplication(sys.argv)
    app.setOrganizationName("Rancorsoft")
    app.setOrganizationDomain("Rancorsoft.com")
    app.setApplicationName("Digital Menu Board")

    QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)

    config = Configuration.Configuration()
    fullScreenMenu = FullScreenWindow.FullScreenWindow(config)
    mainwin = MainWindow.MainWindow(config)
    mainwin.setWindowIcon(QtGui.QIcon(osp.join(osp.dirname(__file__), 'Images/logo_256x256.jpg')))
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

# python bit to figure how who started This
if __name__ == "__main__":
    main()