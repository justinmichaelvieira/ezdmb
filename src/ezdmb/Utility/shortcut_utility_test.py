import pytest
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QApplication, QWidget

from ezdmb.Utility.shortcut_utility import setCloseOnEscKey, setOpenOnOKey

class TestShortcutUtility:
    @pytest.fixture
    def qapp(self):
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return app
    def test_set_close_on_esc_key_creates_shortcut(self, qapp: QApplication | QCoreApplication):
        window = QWidget()

        setCloseOnEscKey(window)

        assert hasattr(window, "closeOnEscShortcut")
        assert window.closeOnEscShortcut.key() == QKeySequence(Qt.Key.Key_Escape)
        assert window.closeOnEscShortcut.parent() is window

    def test_set_open_on_o_key_creates_shortcut_and_triggers_callback(self, qapp: QApplication | QCoreApplication):
        window = QWidget()
        calls = []

        def open_lambda():
            calls.append("opened")

        setOpenOnOKey(window, open_lambda)

        assert hasattr(window, "openOnOShortcut")
        assert window.openOnOShortcut.key() == QKeySequence(Qt.Key.Key_O)

        window.openOnOShortcut.activated.emit()
        assert calls == ["opened"]
