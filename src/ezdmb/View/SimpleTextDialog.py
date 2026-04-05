# pylint: disable=no-name-in-module
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
)


class SimpleTextDialog(QDialog):
    def __init__(self, titleText, messageText):
        super().__init__()

        self.setWindowTitle(titleText)

        message = QLabel(messageText)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
