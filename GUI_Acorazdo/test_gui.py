"""
Script de prueba para verificar que la GUI funciona
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt

def test_gui():
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("🚤 Test - ESP32 Boat Control")
    window.setGeometry(100, 100, 800, 600)
    
    label = QLabel("✅ GUI funcionando correctamente!\n\n" + 
                   "Si ves esta ventana, PyQt6 está instalado y funcionando.\n\n" +
                   "Presiona ESC para cerrar.", window)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("""
        QLabel {
            font-size: 20px;
            padding: 50px;
            background-color: #2c3e50;
            color: white;
        }
    """)
    
    window.setCentralWidget(label)
    window.show()
    
    print("✅ Ventana de prueba abierta")
    print("Presiona CTRL+C en la terminal para cerrar")
    
    sys.exit(app.exec())

if __name__ == '__main__':
    test_gui()
