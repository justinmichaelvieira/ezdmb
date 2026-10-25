__version__ = "1.1.0"

STYLESHEET = """
QWidget {
    background-color: #f5f6f7;
    color: #20252b;
    font-size: 10pt;
}

QMainWindow {
    background-color: #f5f6f7;
}

QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #dce1e6;
}

QMenuBar::item {
    padding: 6px 10px;
}

QMenuBar::item:selected, QMenu::item:selected {
    background-color: #e7eef8;
    color: #174f91;
}

QGroupBox {
    background-color: #ffffff;
    border: 1px solid #dce1e6;
    border-radius: 5px;
    margin-top: 12px;
    padding: 12px;
    font-size: 12pt;
    font-weight: 600;
}

QGroupBox[rotationEnabled="false"] {
    background-color: #e8eaed;
}

QWidget#groupToolbar {
    background-color: transparent;
}

QRadioButton#everySecondsRadio,
QRadioButton#byScheduleRadio,
QRadioButton#noneRadio,
QLabel#secondsLabel {
    background-color: transparent;
}

QRadioButton#everySecondsRadio,
QRadioButton#byScheduleRadio,
QRadioButton#noneRadio {
    font-size: 14pt;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #343b43;
}

QPushButton {
    background-color: #ffffff;
    border: 1px solid #cbd2da;
    border-radius: 4px;
    padding: 7px 12px;
}

QPushButton:hover {
    background-color: #eef3f8;
    border-color: #8ba9c8;
}

QPushButton:pressed {
    background-color: #dce8f5;
}

QPushButton#addContentButton {
    background-color: #1f5f9f;
    border-color: #1f5f9f;
    color: #ffffff;
}

QPushButton#addContentButton:hover {
    background-color: #174f84;
}

QPushButton#deleteSelectionButton {
    color: #8a3d3a;
}

QListWidget, QDoubleSpinBox {
    background-color: #ffffff;
    border: 1px solid #cbd2da;
    border-radius: 4px;
    padding: 5px;
}

QDoubleSpinBox {
    min-height: 32px;
}

QDoubleSpinBox#rotateTimeBox {
    background-color: transparent;
}

QListWidget::item {
    padding: 6px 8px;
    border-bottom: 1px solid #edf0f2;
}

QListWidget::item:selected {
    background-color: #e5eef9;
    color: #174f91;
}

QRadioButton {
    spacing: 8px;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #68727d;
    border-radius: 8px;
    background-color: #ffffff;
}

QRadioButton::indicator:checked {
    border-color: #1f5f9f;
    background-color: #1f5f9f;
}

QRadioButton#everySecondsRadio::indicator,
QRadioButton#byScheduleRadio::indicator,
QRadioButton#noneRadio::indicator {
    width: 20px;
    height: 20px;
    border-radius: 10px;
}

QToolButton {
    color: #20252b;
    background-color: transparent;
}
"""
