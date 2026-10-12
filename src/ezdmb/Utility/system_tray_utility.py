from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from ezdmb.Utility.icon_utility import getWindowIcon


class system_tray_utility:
    def __init__(self, windows, quit_callback, parent=None):
        self.windows = tuple(windows)
        self._quit_callback = quit_callback
        self._hidden_window_states = []
        self._active_window = None

        self.menu = QMenu()
        self.minimize_action = self.menu.addAction("Minimize to tray")
        self.exit_action = self.menu.addAction("Exit")
        self.minimize_action.triggered.connect(self.minimize_to_tray)
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

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.restore_windows()
