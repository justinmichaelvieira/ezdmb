# main2.py
# DMB startup script
# Adam Brody [adam@rancorsoft.com] / Justin Vieira [justin@rancorsoft.com]
# Rancorsoft, LLC 2016

import sys
import PyQt5
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

# Our own class imports
from View import MainWindow
from View import SecDialog

# Cmd line library
import argparse
# I think this is a required defined class for argparse?  Hmm -JV
class CmdArgs:
    pass

# starting point of the app runtime
def main():
    # a new app instance
    app = QApplication(sys.argv)

    form = MainWindow.MainWindow()
    form2 = SecDialog.SecDialog()
    form.show()

    def selectFile():
        class override_graphicsScene (Qt.QGraphicsScene):
            def __init__(form,parent = None):
                super(override_graphicsScene,form).__init__(parent)

            def mousePressEvent(form, event):
                super(override_graphicsScene, form).mousePressEvent(event)
                print(event.pos())

        main_img = QFileDialog.getOpenFileName()[0]    
        form.label_pic.pixmap = Qt.QPixmap()
        form.label_pic.setPixmap(QtGui.QPixmap(main_img))
        form.label_pic.pixmap = form.label_pic.pixmap.scaled(form.size(), Qt.Qt.KeepAspectRatio)
        print(main_img)

    form.pushButton.clicked.connect(selectFile)
    form.pushButton_2.clicked.connect(lambda: form2.show())

    def advancedSettings():
        multiSelectImages = []
        if form2.checkBox == True:
            for n in multiSelectImages
                form.label_pic.pixmap = Qt.QPixmap()
                form.label_pic.setPixmap(QtGui.QPixmap(n))
                form.label_pic.pixmap = form.label_pic.pixmap.scaled(form.size(), Qt.Qt.KeepAspectRatio)
        

    form2.buttonBox.Ok.clicked.connect(advancedSettings)

    # store screen geometry
    screenWidth = form.frameGeometry().width()
    screenHeight = form.frameGeometry().height()

    # simple command line options sample
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