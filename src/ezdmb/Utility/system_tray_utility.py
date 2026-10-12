from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from ezdmb.Utility.icon_utility import getWindowIcon


class system_tray_utility:
    def __init__(
        self,
        windows,
        quit_callback,
        parent=None,
        *,
        configuration_window=None,
        full_screen_window=None,
    ):
        self.windows = tuple(windows)
        self.configuration_window = configuration_window
        self.full_screen_window = full_screen_window
        self._quit_callback = quit_callback
        self._hidden_window_states = []
        self._active_window = None

        self.menu = QMenu()
        self.minimize_configuration_action = self.menu.addAction(
            "Minimize Configuration Window"
        )
        self.minimize_full_screen_action = self.menu.addAction(
            "Minimize Full Screen Window"
        )
        self.minimize_action = self.menu.addAction("Minimize All")
        self.show_full_screen_action = self.menu.addAction("Show Full Screen Window")
        self.show_configuration_action = self.menu.addAction(
            "Show Configuration Window"
        )
        self.show_all_action = self.menu.addAction("Show All Windows")
        self.menu.addSeparator()
        self.exit_action = self.menu.addAction("Exit")
        self.minimize_action.triggered.connect(self.minimize_to_tray)
        self.minimize_configuration_action.triggered.connect(
            self.minimize_configuration_window
        )
        self.minimize_full_screen_action.triggered.connect(
            self.minimize_full_screen_window
        )
        self.show_full_screen_action.triggered.connect(self.show_full_screen_window)
        self.show_configuration_action.triggered.connect(
            self.show_configuration_window
        )
        self.show_all_action.triggered.connect(self.show_all_windows)
        self.exit_action.triggered.connect(self._quit_callback)

        self.tray_icon = QSystemTrayIcon(getWindowIcon(), parent)
        self.tray_icon.setToolTip("ezdmb")
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self._on_activated)

    def show(self):
        self.tray_icon.show()

    def minimize_to_tray(self):
        if self._hidden_window_states:
            return

        app = QApplication.instance()
        self._active_window = app.activeWindow() if app is not None else None
        self._hidden_window_states = [
            (window, window.windowState())
            for window in self.windows
            if window.isVisible()
        ]
        for window, _ in self._hidden_window_states:
            window.hide()

    def restore_windows(self):
        windows_to_restore = self._hidden_window_states
        self._hidden_window_states = []

        for window, state in windows_to_restore:
            if state & Qt.WindowState.WindowFullScreen:
                window.showFullScreen()
            elif state & Qt.WindowState.WindowMaximized:
                window.showMaximized()
            elif state & Qt.WindowState.WindowMinimized:
                window.showMinimized()
            else:
                window.show()

        if self._active_window in (window for window, _ in windows_to_restore):
            self._active_window.raise_()
            self._active_window.activateWindow()
        self._active_window = None

    def minimize_configuration_window(self):
        self._minimize_window(self.configuration_window)

    def minimize_full_screen_window(self):
        self._minimize_window(self.full_screen_window)

    def show_full_screen_window(self):
        if self.full_screen_window is None:
            return
        self.full_screen_window.showFullScreen()
        self.full_screen_window.raise_()
        self.full_screen_window.activateWindow()
        self._update_saved_state(self.full_screen_window)

    def show_configuration_window(self):
        if self.configuration_window is None:
            return
        self._show_window(self.configuration_window)
        self._update_saved_state(self.configuration_window)

    def show_all_windows(self):
        self.show_full_screen_window()
        self.show_configuration_window()

    def _minimize_window(self, window):
        if window is None:
            return
        window.showMinimized()
        self._update_saved_state(window)

    @staticmethod
    def _show_window(window):
        state = window.windowState()
        if state & Qt.WindowState.WindowFullScreen:
            window.showFullScreen()
        elif state & Qt.WindowState.WindowMaximized:
            window.showMaximized()
        else:
            window.showNormal()
        window.raise_()
        window.activateWindow()

    def _update_saved_state(self, window):
        self._hidden_window_states = [
            (saved_window, window.windowState() if saved_window is window else state)
            for saved_window, state in self._hidden_window_states
        ]

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.restore_windows()
