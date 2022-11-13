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
        return (
            """<html>
<body>
    <img src="file:///"""
            + image
            + """" width="100%" height="100%" />
</body>
</html>
"""
        )

    def run(self):
        for i in range(10000):
            html = self.getPage(self.contentArray[i % len(self.contentArray)])
            if self.debug:
                print(html)
            self.updated.emit(str(html))
            self.sleep(int(self.rotateTimeout * 60))
