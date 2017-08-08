import threading
from PyQt5.QtCore import QUrl, pyqtSignal, QThread
from PyQt5.QtWebKit import QWebSettings

class HtmlViewUtility(QThread):
    updated = pyqtSignal(str)
    def __init__(self, contentArray, rotateContent, rotateTimeout, webkitWidget, onRefresh):
        QThread.__init__(self)
        self.debug = True
        self.contentArray = contentArray
        self.rotateContent = rotateContent
        self.rotateTimeout = rotateTimeout
        self.webkitWidget = webkitWidget
        self.count = 0
        self.updated.connect(onRefresh)
        self.start()

    def getStretchFillImgPage(self, image):
        return '''<html>
<body>
    <image src="file:///''' + image + '''" width="100%" height="100%" ></image>
</body>
</html>
'''
    def run( self ):
        for i in range(10000):
            html = self.getStretchFillImgPage(self.contentArray[i % len(self.contentArray)])
            if self.debug:
                print(html)
            self.updated.emit(str(html))
            self.sleep(self.rotateTimeout *60)
