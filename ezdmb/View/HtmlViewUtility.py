import os.path
from PyQt5.QtCore import pyqtSignal, QThread


class HtmlViewUtility(QThread):
    updated = pyqtSignal(str)

    def __init__(
        self, contentArray, rotateContent, rotateTimeout, webkitWidget, onRefresh
    ):
        QThread.__init__(self)
        self.debug = True
        self.contentArray = contentArray
        self.rotateContent = rotateContent
        self.rotateTimeout = rotateTimeout
        self.webkitWidget = webkitWidget
        self.count = 0
        self.updated.connect(onRefresh)
        self.start()

    def getPage(self, fileName):
        fileExtension = os.path.splitext(fileName)[1].lower()
        imgExtensions = [".jpg", ".png", ".gif", ".bmp", ".ico"]
        if fileExtension == ".html":
            return open(fileName, "r").read()
        elif any(checkExt == fileExtension for checkExt in imgExtensions):
            return self.getStretchFillImgPage(fileName)

    def getStretchFillImgPage(self, image):
        return f'<img src="file://{image}" style="object-fit: contain; width: 100%; height: 100%; scale: 200%;" />'

    def run(self):
        i = 0
        while(True):
            html = self.getPage(self.contentArray[i % len(self.contentArray)])
            i+=1

            if self.debug:
                print(html)

            self.updated.emit(str(html))
            self.sleep(int(self.rotateTimeout * 60))
