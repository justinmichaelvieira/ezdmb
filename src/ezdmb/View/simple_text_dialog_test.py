import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel

from ezdmb.View import simple_text_dialog


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


class TestSimpleTextDialog:
    def test_renders_rich_text_with_external_links_enabled(self, qapp):
        dialog = simple_text_dialog.simple_text_dialog(
            "About", '<a href="https://example.com">Project site</a>'
        )
        label = dialog.findChild(QLabel)

        assert dialog.windowTitle() == "About"
        assert label is not None
        assert label.textFormat() == Qt.TextFormat.RichText
        assert label.openExternalLinks()
        assert (
            label.textInteractionFlags()
            & Qt.TextInteractionFlag.TextBrowserInteraction
        )

    def test_close_button_rejects_dialog(self, qapp):
        dialog = simple_text_dialog.simple_text_dialog("Help", "Details")
        close_button = dialog.buttonBox.button(QDialogButtonBox.StandardButton.Close)

        close_button.click()

        assert dialog.result() == QDialog.DialogCode.Rejected