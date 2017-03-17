# main.py
# DMB startup script
# Adam Brody [adam@rancorsoft.com] / Justin Vieira [justin@rancorsoft.com] / Richard Haynes [richard@rancorsoft.com]
# Rancorsoft, LLC 2016

import sys
import PyQt5
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

# Our own class imports
from View import MainWindow
from View import SecDialog
from View import FullScreenWindow

import Configuration

from Controller import SelectFile

# Cmd line library
import argparse
# This is a required defined class for argparse -JV
class CmdArgs:
    pass

# starting point of the app runtime
def main():
    # a new app instance
    app = QApplication(sys.argv)

    config = Configuration.Configuration()
    # print(config.get_savedImage)
    fullScreenMenu = FullScreenWindow.FullScreenWindow()
    configDialog = MainWindow.MainWindow()
    configDialog.current_menu.setPixmap(QtGui.QPixmap(config.SavedImage))
    advancedConfig = SecDialog.SecDialog()
    configDialog.show()
    fullScreenMenu.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    fullScreenMenu.showFullScreen()

    selectFile = SelectFile.SelectFile();
    configDialog.setImageButton.clicked.connect(lambda: selectFile.selectFile(configDialog, fullScreenMenu))
    #configDialog.pushButton_2.clicked.connect(lambda: advancedConfig.show())

    # store screen geometry
    screenWidth = fullScreenMenu.frameGeometry().width()
    screenHeight = fullScreenMenu.frameGeometry().height()

    fullScreenMenu.label_pic.resize(screenWidth, screenHeight)

    # command line option setup and processing
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-x', '--xpos', help='X Position of window', type=int, default=0)
    argparser.add_argument('-y', '--ypos', help='Y position of window', type=int, default=0)
    # argparser.add_argument('-sw', '--width', help='Width of window', type=int, default=800)
    argparser.add_argument('-sw', '--width', help='Width of window', type=int, default=screenWidth)
    argparser.add_argument('-sh', '--height', help='Height of window', type=int, default=screenHeight)
    args = vars(argparser.parse_args())

    print(args['width'])
    print(args['height'])
    # without this, the script exits immediately.
    sys.exit(app.exec_())
# python bit to figure how who started This
if __name__ == "__main__":
    main()