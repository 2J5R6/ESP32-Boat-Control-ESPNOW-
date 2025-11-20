"""
ESP32 Boat Control - GUI Principal
Control remoto de barco con visualización 3D
"""

import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
