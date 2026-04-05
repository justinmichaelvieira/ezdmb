# pylint: disable=no-name-in-module
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
)

from ezdmb import __version__


class SimpleTextDialog(QDialog):
    def __init__(self, titleText, messageText):
        super().__init__()

        # self.setWindowTitle("About ezdmb")
        self.setWindowTitle(titleText)

        # message = QLabel("ezdmb v" + __version__ + "\nGithub: https://github.com/justinmichaelvieira/ezdmb\n")
        message = QLabel(messageText)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
