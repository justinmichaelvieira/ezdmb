from PyQt5.QtWidgets import QWidget
from .navheader_ui import Ui_Form


class NavHeader(QWidget, Ui_Form):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
