from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
)


class simple_text_dialog(QDialog):
    def __init__(self, titleText, messageText):
        super().__init__()

        self.setWindowTitle(titleText)

        message = QLabel(messageText)
        message.setTextFormat(Qt.RichText)
        message.setTextInteractionFlags(Qt.TextBrowserInteraction)
        message.setOpenExternalLinks(True)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
