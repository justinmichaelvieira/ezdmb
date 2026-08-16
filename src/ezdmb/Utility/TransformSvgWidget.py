from PySide6.QtGui import QPainter, QTransform
from PySide6.QtWidgets import QWidget
from PySide6.QtSvg import QSvgRenderer

class TransformSvgWidget(QWidget):
    def __init__(self, svg_file):
        super().__init__()
        self.renderer = QSvgRenderer(svg_file)
        self.setMinimumSize(200, 200)
        self.transform = QTransform()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setTransform(self.transform)
        self.renderer.render(painter)

    def set_scale(self, scale_factor):
        self.transform = QTransform()
        self.transform.scale(scale_factor, scale_factor)
        self.update()

    def set_rotation(self, angle):
        self.transform = QTransform()
        self.transform.rotate(angle)
        self.update()
