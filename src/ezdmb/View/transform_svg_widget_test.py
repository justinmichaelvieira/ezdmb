from math import isclose

import pytest
from PySide6.QtCore import QPointF
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication

from ezdmb.View.transform_svg_widget import transform_svg_widget


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


class TestTransformSvgWidget:
    def test_loads_svg_and_enforces_minimum_size(self, tmp_path, qapp):
        svg_file = tmp_path / "shape.svg"
        svg_file.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="10">'
            '<rect width="20" height="10" fill="red"/></svg>',
            encoding="utf-8",
        )
        widget = transform_svg_widget(str(svg_file))

        assert isinstance(widget.renderer, QSvgRenderer)
        assert widget.renderer.isValid()
        assert widget.minimumWidth() == 200
        assert widget.minimumHeight() == 200

    def test_scale_and_rotation_replace_transform(self, tmp_path, qapp):
        svg_file = tmp_path / "shape.svg"
        svg_file.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"/>',
            encoding="utf-8",
        )
        widget = transform_svg_widget(str(svg_file))

        widget.set_scale(2.5)

        assert isclose(widget.transform.m11(), 2.5)
        assert isclose(widget.transform.m22(), 2.5)
        assert isclose(widget.transform.m12(), 0.0)

        widget.set_rotation(90)
        mapped_point = widget.transform.map(QPointF(1, 0))

        assert isclose(mapped_point.x(), 0.0, abs_tol=1e-9)
        assert isclose(mapped_point.y(), 1.0, abs_tol=1e-9)