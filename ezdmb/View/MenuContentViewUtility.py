import os.path
from PyQt5.QtCore import pyqtSignal, QThread, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QFont

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
        if fileExtension == ".txt":
            pix = QPixmap() # QPixmap pix = ...;
            painter = QPainter(pix) # QPainter painter( &pix );
            painter.setFont(QFont("Arial"));
            painter.drawText(QPoint(100, 100), os.read());
        elif any(checkExt == fileExtension for checkExt in imgExtensions):
            return QPixmap(fileName)

    def run(self):
        i = 0
        while(True):
            index = i % len(self.contentArray)
            pixels = self.contentArray[index]
            img = self.getViewableFilecontent(pixels)
            self.pixmap.setPixmap(img)
            i += 1

            if self.debug:
                print(self.windowName + ": Displaying image " + str(index))

            self.updated.emit(img)
            self.sleep(int(self.rotateTimeout * 60))
