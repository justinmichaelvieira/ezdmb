from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QApplication

from ezdmb.Controller.configuration import (
    default_content_groups,
    default_time_blocks,
)
from ezdmb.View import config_window


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def config():
    return SimpleNamespace(
        RotateContent=True,
        RotateContentTime=15,
        ContentArray=[],
        RotationMode="interval",
        ContentGroups=default_content_groups(),
        TimeBlocks=default_time_blocks(),
        save_config=MagicMock(),
        configUpdated=MagicMock(),
    )


class TestConfigWindow:
    def test_builds_configuration_window_and_help_actions(self, qapp, config):
        show_about = MagicMock()
        show_quickstart = MagicMock()
        window = config_window.config_window(config, show_about, show_quickstart)

        assert window.windowTitle() == "Configuration"
        central_widget = window.centralWidget()
        assert central_widget is not None
        assert central_widget.objectName() == "centralWidget"
        assert window.config_widget._config is config
        assert window.menuFile.title() == "File"
        assert window.menuHelp.title() == "Help"
        assert window.minimizeToTrayAction.text() == "Minimize All"
        assert not window.minimizeToTrayAction.icon().isNull()
        assert window.minimizeConfigurationWindowAction.text() == (
            "Minimize Configuration Window"
        )
        assert not window.minimizeConfigurationWindowAction.icon().isNull()
        assert window.minimizeFullScreenWindowAction.text() == (
            "Minimize Full Screen Window"
        )
        assert not window.minimizeFullScreenWindowAction.icon().isNull()
        assert window.showFullScreenWindowAction.text() == "Show Full Screen Window"
        assert not window.showFullScreenWindowAction.icon().isNull()

        window.showAboutAction.trigger()
        window.showQuickstartAction.trigger()

        show_about.assert_called_once_with()
        show_quickstart.assert_called_once_with()

    def test_minimize_to_tray_action_emits_request(self, qapp, config):
        minimize_to_tray = MagicMock()
        window = config_window.config_window(config, MagicMock(), MagicMock())
        window.minimizeToTrayRequested.connect(minimize_to_tray)

        window.minimizeToTrayAction.trigger()

        minimize_to_tray.assert_called_once_with()

    def test_minimize_configuration_action_minimizes_window(self, qapp, config):
        window = config_window.config_window(config, MagicMock(), MagicMock())
        window.show()
        qapp.processEvents()

        window.minimizeConfigurationWindowAction.trigger()
        qapp.processEvents()

        assert window.isMinimized()

    def test_full_screen_actions_emit_requests(self, qapp, config):
        minimize_full_screen = MagicMock()
        show_full_screen = MagicMock()
        window = config_window.config_window(config, MagicMock(), MagicMock())
        window.minimizeFullScreenWindowRequested.connect(minimize_full_screen)
        window.showFullScreenWindowRequested.connect(show_full_screen)

        window.minimizeFullScreenWindowAction.trigger()
        window.showFullScreenWindowAction.trigger()

        minimize_full_screen.assert_called_once_with()
        show_full_screen.assert_called_once_with()

    def test_bundle_menu_actions_forward_config(self, qapp, config, monkeypatch):
        export = MagicMock()
        import_content = MagicMock()
        monkeypatch.setattr(config_window, "export_bundle", export)
        monkeypatch.setattr(config_window, "import_bundle", import_content)
        window = config_window.config_window(config, MagicMock(), MagicMock())

        window.exportBundleAction.trigger()
        window.importBundleAction.trigger()

        export.assert_called_once_with(config)
        import_content.assert_called_once_with(
            window.config_widget.trigger_settings_ui_update,
            config,
        )

    def test_exit_action_requests_application_quit(self, qapp, config, monkeypatch):
        quit_app = MagicMock()
        monkeypatch.setattr(QApplication, "quit", staticmethod(quit_app))
        window = config_window.config_window(config, MagicMock(), MagicMock())

        window.exitAction.trigger()

        quit_app.assert_called_once_with()