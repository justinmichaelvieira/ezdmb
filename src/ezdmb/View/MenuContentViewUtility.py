import os.path
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from PyQt5.QtGui import QPixmap
from ezdmb.Controller.Configuration import Configuration


class MenuContentViewUtility(QThread):
    contentUpdated = pyqtSignal(QPixmap)

    def __init__(
        self, config: Configuration, pixmap, windowName, onRefresh
    ):
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

    @pyqtSlot(dict)
    def onConfigUpdated(self, data):
        self.contentArray = data["imported_content"]
        self.rotateContent = data["rotate_content"]
        self.rotateTimeout = data["rotate_content_time"]

    def getViewableFilecontent(self, fileName):
        imgExtensions = [".jpg", ".png", ".gif", ".bmp", ".ico"]

        fileExtension = os.path.splitext(fileName)[1].lower()

        if any(checkExt == fileExtension for checkExt in imgExtensions):
            return QPixmap(fileName)
        else:
            return None

    def run(self):
        i = 0
        while (True):
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
