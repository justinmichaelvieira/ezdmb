# pylint: disable=no-name-in-module
import os.path

from PySide6.QtCore import QPoint, QThread, Signal, Slot
from PySide6.QtGui import QFont, QPainter, QPixmap, Qt

from ezdmb.Controller.configuration import configuration


class menu_content_view_utility(QThread):
    contentUpdated = Signal(QPixmap)

    def __init__(self, config: configuration, pixmap, windowName, onRefresh):
        QThread.__init__(self)
        self._config = config

        self.debug = True
        self.contentArray = self._config.ContentArray
        self.rotateContent = self._config.RotateContent
        self.rotateTimeout = self._config.RotateContentTime
        self.count = 0
        self.pixmap = pixmap
        self.windowName = windowName
        self.contentUpdated.connect(onRefresh)
        self._config.configUpdated.connect(self.onConfigUpdated)
        self.start()

    def __del__(self):
        self.wait()

    @Slot(dict)
    def onConfigUpdated(self, data):
        self.contentArray = data["imported_content"]
        self.rotateContent = data["rotate_content"]
        self.rotateTimeout = data["rotate_content_time"]

    def getViewableFilecontent(self, fileName):
        imgExtensions = [".jpg", ".png", ".gif", ".bmp", ".ico"]

        fileExtension = os.path.splitext(fileName)[1].lower()

        if any(checkExt == fileExtension for checkExt in imgExtensions):
            return QPixmap(fileName)
        elif fileExtension == ".txt":
            with open(fileName, "r") as f:
                txt_content = f.read()
                pix = QPixmap(400, 300)
                pix.fill(Qt.white)
                painter = QPainter(pix)
                painter.setFont(QFont("Arial"))

                row_spacing = 20
                i = 1
                for line in txt_content.splitlines():
                    painter.drawText(QPoint(12, i * row_spacing), line)
                    i += 1

                return pix
        else:
            return None

    def run(self):
        i = 0
        while True:
            if len(self.contentArray) > 0:
                index = i % len(self.contentArray)
                pixels = self.contentArray[index]
                img = self.getViewableFilecontent(pixels)
                if img is not None:
                    self.pixmap.setPixmap(img)
                    self.contentUpdated.emit(img)
                i += 1

                if self.debug:
                    print(self.windowName + ": Displaying image " + str(index))
            else:
                print("No content to display; Skipping rotation.")

            self.sleep(int(self.rotateTimeout))
