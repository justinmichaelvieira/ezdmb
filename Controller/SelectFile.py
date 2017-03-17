import sys
import PyQt5
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import Configuration
import mainwindow_auto

class SelectFile(object):

    def __init__(self):
        super(self.__class__, self).__init__()

    def selectFile(self, form, fullScreenForm):
        class override_graphicsScene (Qt.QGraphicsScene):
            def __init__(form,parent = None):
                super(override_graphicsScene,form).__init__( 
                    )

            def mousePressEvent(form, event):
                super(override_graphicsScene, form).mousePressEvent(event)
                print(event.pos())

        # Display new Image
        main_img = QFileDialog.getOpenFileName()[0]
        form.current_menu.pixmap = Qt.QPixmap()
        form.current_menu.setPixmap(QtGui.QPixmap(main_img))
        form.current_menu.pixmap = form.current_menu.pixmap.scaled(form.size(), Qt.Qt.KeepAspectRatio)
        fullScreenForm.label_pic.pixmap = Qt.QPixmap()
        fullScreenForm.label_pic.setPixmap(QtGui.QPixmap(main_img))
        fullScreenForm.label_pic.pixmap = fullScreenForm.label_pic.pixmap.scaled(fullScreenForm.size(), Qt.Qt.KeepAspectRatio)
        #print(main_img)

        # Save new image as the default image
        config = Configuration.Configuration()
        config.SaveConfig(main_img)