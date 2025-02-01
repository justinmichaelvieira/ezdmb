import io
import os.path
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QPixmap

class MenuContentViewUtility(QThread):
    updated = pyqtSignal(QPixmap)

    def __init__(
        self, contentArray, rotateContent, rotateTimeout, pixmap, windowName, onRefresh
    ):
        QThread.__init__(self)
        self.debug = True
        self.contentArray = contentArray
        self.rotateContent = rotateContent
        self.rotateTimeout = rotateTimeout
        self.count = 0
        self.pixmap = pixmap
        self.windowName = windowName
        self.updated.connect(onRefresh)
        self.start()

    def getViewableFilecontent(self, fileName):
        imgExtensions = [".jpg", ".png", ".gif", ".bmp", ".ico"]

        fileExtension = os.path.splitext(fileName)[1].lower()
        # if fileExtension == ".txt":
        #     painter = QPainter(self.pixmap) # QPainter painter( &pix );
        #     painter.setFont(QFont("Arial"));
        #     painter.drawText(QPoint(100, 100), "Test");

        if any(checkExt == fileExtension for checkExt in imgExtensions):
            return QPixmap(fileName)
        else:
            return None

    def run(self):
        i = 0
        while(True):
            index = i % len(self.contentArray)
            pixels = self.contentArray[index]
            img = self.getViewableFilecontent(pixels)
            if img is not None:
                self.pixmap.setPixmap(img)
                self.updated.emit(img)
            i += 1

            if self.debug:
                print(self.windowName + ": Displaying image " + str(index))

            self.sleep(int(self.rotateTimeout * 60))
