from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
)

from ezdmb import __version__


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About ezdmb")

        message = QLabel("ezdmb v" + __version__ + "\nGithub: https://github.com/justinmichaelvieira/ezdmb\n")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
