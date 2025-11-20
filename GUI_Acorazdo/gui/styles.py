"""
Estilos de la aplicación
"""

MAIN_STYLE = """
QMainWindow {
    background-color: #2c3e50;
}

QWidget {
    background-color: #34495e;
    color: #ecf0f1;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}

QGroupBox {
    background-color: #2c3e50;
    border: 2px solid #3498db;
    border-radius: 8px;
    margin-top: 10px;
    padding: 15px;
    font-weight: bold;
    font-size: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 5px 10px;
    background-color: #3498db;
    color: white;
    border-radius: 4px;
}

QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #1f6391;
}

QPushButton:disabled {
    background-color: #7f8c8d;
    color: #bdc3c7;
}

QComboBox {
    background-color: #2c3e50;
    color: #ecf0f1;
    border: 2px solid #3498db;
    border-radius: 5px;
    padding: 8px;
    font-size: 12px;
}

QComboBox:hover {
    border: 2px solid #2980b9;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #ecf0f1;
    width: 0;
    height: 0;
}

QComboBox QAbstractItemView {
    background-color: #2c3e50;
    color: #ecf0f1;
    selection-background-color: #3498db;
    border: 1px solid #3498db;
}

QLabel {
    color: #ecf0f1;
    background-color: transparent;
}

QCheckBox {
    color: #ecf0f1;
    spacing: 8px;
    padding: 5px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid #3498db;
    background-color: #2c3e50;
}

QCheckBox::indicator:checked {
    background-color: #3498db;
    border: 2px solid #2980b9;
}

QCheckBox::indicator:checked::after {
    content: '✓';
    color: white;
    font-weight: bold;
}

QTextEdit {
    background-color: #1e1e1e;
    color: #00ff00;
    border: 2px solid #3498db;
    border-radius: 5px;
    padding: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
}

QScrollBar:vertical {
    background-color: #2c3e50;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #3498db;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #2980b9;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QSplitter::handle {
    background-color: #3498db;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #2980b9;
}
"""
