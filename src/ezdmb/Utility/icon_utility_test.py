from pathlib import Path
from xml.etree import ElementTree

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
    def test_resource_manifest_sources_exist_in_images_directory(self):
        manifest = Path(__file__).parents[1] / "View" / "resources.qrc"
        resource_files = ElementTree.parse(manifest).getroot().findall(".//file")

        assert resource_files
        assert all(
            resource_file.text and resource_file.text.startswith("images/")
            for resource_file in resource_files
        )
        assert all(
            (manifest.parent / resource_file.text).is_file()
            for resource_file in resource_files
        )

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
