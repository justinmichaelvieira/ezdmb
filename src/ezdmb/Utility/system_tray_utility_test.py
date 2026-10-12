from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import Qt
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

        assert [
            action.text()
            for action in utility.menu.actions()
            if not action.isSeparator()
        ] == [
            "Minimize Configuration Window",
            "Minimize Full Screen Window",
            "Minimize All",
            "Show Full Screen Window",
            "Show Configuration Window",
            "Show All Windows",
            "Exit",
        ]
        assert utility.tray_icon.contextMenu() is utility.menu

    def test_individual_actions_target_their_window(self, qapp):
        config_window = MagicMock()
        full_screen_window = MagicMock()
        config_window.windowState.return_value = Qt.WindowState.WindowNoState
        utility = system_tray_utility(
            [],
            MagicMock(),
            qapp,
            configuration_window=config_window,
            full_screen_window=full_screen_window,
        )

        utility.minimize_configuration_action.trigger()
        utility.minimize_full_screen_action.trigger()
        utility.show_full_screen_action.trigger()
        utility.show_configuration_action.trigger()

        config_window.showMinimized.assert_called_once_with()
        config_window.showNormal.assert_called_once_with()
        full_screen_window.showMinimized.assert_called_once_with()
        full_screen_window.showFullScreen.assert_called_once_with()

    def test_show_all_shows_full_screen_before_configuration(self, qapp):
        calls = []
        config_window = MagicMock()
        config_window.windowState.return_value = Qt.WindowState.WindowNoState
        config_window.showNormal.side_effect = lambda: calls.append("configuration")
        full_screen_window = MagicMock()
        full_screen_window.showFullScreen.side_effect = lambda: calls.append(
            "full_screen"
        )
        utility = system_tray_utility(
            [],
            MagicMock(),
            qapp,
            configuration_window=config_window,
            full_screen_window=full_screen_window,
        )

        utility.show_all_action.trigger()

        assert calls == ["full_screen", "configuration"]
        config_window.raise_.assert_called_once_with()
        config_window.activateWindow.assert_called_once_with()

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