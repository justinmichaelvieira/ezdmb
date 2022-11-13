from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ezdmb.Utility.ShortcutUtility import setEscKey
from ezdmb.View import HtmlViewUtility

from ezdmb.View.generated.FullScreenWindow_ui import Ui_FullScreenWindow


class FullScreenWindow(QMainWindow, Ui_FullScreenWindow):
    def __init__(self, config):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.htmlUtil = HtmlViewUtility.HtmlViewUtility(
            config.ContentArray,
            config.RotateContent,
            config.RotateContentTime,
            self.label_pic,
            self.onRefresh,
        )
        setEscKey(self)

    @pyqtSlot(str)
    def onRefresh(self, value):
        # self.label_pic.setHtml(value)
        pass
