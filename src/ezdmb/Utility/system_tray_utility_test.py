from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QWidget

from ezdmb.Utility.system_tray_utility import system_tray_utility


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


class TestSystemTrayUtility:
    def test_menu_has_minimize_and_exit_actions(self, qapp):
        utility = system_tray_utility([], MagicMock(), qapp)

        assert [action.text() for action in utility.menu.actions()] == [
            "Minimize to tray",
            "Exit",
        ]
        assert utility.tray_icon.contextMenu() is utility.menu

    def test_minimize_and_restore_only_previously_visible_windows(self, qapp):
        visible_window = QWidget()
        hidden_window = QWidget()
        visible_window.show()
        qapp.processEvents()
        utility = system_tray_utility(
            [visible_window, hidden_window], MagicMock(), qapp
        )

        utility.minimize_action.trigger()

        assert not visible_window.isVisible()
        assert not hidden_window.isVisible()

        utility.restore_windows()
        qapp.processEvents()

        assert visible_window.isVisible()
        assert not hidden_window.isVisible()
        visible_window.close()

    def test_double_click_restores_hidden_windows(self, qapp):
        window = QWidget()
        window.show()
        qapp.processEvents()
        utility = system_tray_utility([window], MagicMock(), qapp)
        utility.minimize_to_tray()

        utility.tray_icon.activated.emit(
            QSystemTrayIcon.ActivationReason.DoubleClick
        )
        qapp.processEvents()

        assert window.isVisible()
        window.close()

    def test_exit_action_uses_application_quit_callback(self, qapp):
        quit_callback = MagicMock()
        utility = system_tray_utility([], quit_callback, qapp)

        utility.exit_action.trigger()

        quit_callback.assert_called_once_with()

    def test_repeated_minimize_does_not_lose_restore_snapshot(self, qapp):
        window = QWidget()
        window.show()
        qapp.processEvents()
        utility = system_tray_utility([window], MagicMock(), qapp)

        utility.minimize_to_tray()
        utility.minimize_to_tray()
        utility.restore_windows()
        qapp.processEvents()

        assert window.isVisible()
        window.close()