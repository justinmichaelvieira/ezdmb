from types import SimpleNamespace

import pytest
from PySide6.QtWidgets import QApplication

from ezdmb.View.config_window import config_window


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_config_widget_fills_available_central_widget_space(qapp):
    config = SimpleNamespace(
        RotateContent=True,
        RotateContentTime=15,
        ContentArray=[],
    )
    window = config_window(config, lambda: None, lambda: None)

    window.resize(1200, 900)
    window.show()
    qapp.processEvents()

    widget_geometry = window.config_widget.geometry()
    central_geometry = window.centralWidget.rect()

    assert widget_geometry.right() == central_geometry.right() - 11
    assert widget_geometry.bottom() == central_geometry.bottom()

    window.close()