import pytest
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from ezdmb.Utility.icon_utility import getIcon, getWindowIcon


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


class TestIconUtility:
    def test_get_window_icon_returns_qicon(self, qapp):
        icon = getWindowIcon()

        assert isinstance(icon, QIcon)
        assert not icon.isNull()
        assert any(
            size.width() == 48 and size.height() == 48
            for size in icon.availableSizes()
        )

    def test_get_icon_loads_requested_resource(self, qapp):
        icon = getIcon("logo_48x48.png")

        assert isinstance(icon, QIcon)
        assert not icon.isNull()
        assert any(
            size.width() == 48 and size.height() == 48
            for size in icon.availableSizes()
        )
