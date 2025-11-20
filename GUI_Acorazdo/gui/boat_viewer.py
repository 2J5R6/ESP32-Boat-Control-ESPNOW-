"""
Visualizador 3D del Barco
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QRadialGradient, QPainterPath
import math
import os

class BoatViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.enabled = True
        self.water_effect = True
        self.boat_x = 0
        self.boat_y = 0
        self.boat_angle = 0
        self.wave_offset = 0
        self.current_command = "PARADO"
        
        # Estado de animación
        self.is_moving = False
        self.target_x = 0
        self.target_y = 0
        self.target_angle = 0
        
        self.init_ui()
        
        # Timer para animación continua
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(16)  # ~60 FPS
        
    def init_ui(self):
        """Inicializar interfaz"""
        self.setMinimumSize(800, 600)
        layout = QVBoxLayout(self)
        
        # Etiqueta de estado
        self.status_label = QLabel("🚤 Vista del Barco - En Reposo")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: rgba(52, 152, 219, 0.8);
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
    
    def paintEvent(self, event):
        """Dibujar la escena"""
        if not self.enabled:
            self.draw_disabled_view()
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dibujar agua
        if self.water_effect:
            self.draw_water(painter)
        else:
            painter.fillRect(self.rect(), QColor(52, 152, 219))
        
        # Dibujar grid de referencia
        self.draw_grid(painter)
        
        # Dibujar barco
        self.draw_boat(painter)
        
        # Dibujar indicadores
        self.draw_indicators(painter)
    
    def draw_disabled_view(self):
        """Dibujar vista deshabilitada"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(44, 62, 80))
        
        painter.setPen(QColor(149, 165, 166))
        painter.setFont(painter.font())
        font = painter.font()
        font.setPointSize(20)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, 
                        "Visualización 3D Deshabilitada")
    
    def draw_water(self, painter):
        """Dibujar efecto de agua animado"""
        width = self.width()
        height = self.height()
        
        # Gradiente de agua
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0, QColor(41, 128, 185))  # Azul claro
        gradient.setColorAt(0.5, QColor(52, 152, 219))  # Azul medio
        gradient.setColorAt(1, QColor(21, 67, 96))  # Azul oscuro
        
        painter.fillRect(self.rect(), gradient)
        
        # Olas animadas
        painter.setPen(QPen(QColor(255, 255, 255, 40), 2))
        for i in range(0, height, 30):
            path = QPainterPath()
            y = i + self.wave_offset
            path.moveTo(0, y)
            
            for x in range(0, width, 20):
                wave_y = y + math.sin((x + self.wave_offset) * 0.05) * 8
                path.lineTo(x, wave_y)
            
            painter.drawPath(path)
    
    def draw_grid(self, painter):
        """Dibujar cuadrícula de referencia"""
        width = self.width()
        height = self.height()
        
        painter.setPen(QPen(QColor(255, 255, 255, 30), 1, Qt.PenStyle.DotLine))
        
        # Líneas verticales
        for x in range(0, width, 50):
            painter.drawLine(x, 0, x, height)
        
        # Líneas horizontales
        for y in range(0, height, 50):
            painter.drawLine(0, y, width, y)
        
        # Cruz central
        painter.setPen(QPen(QColor(255, 255, 255, 60), 2))
        painter.drawLine(width // 2, 0, width // 2, height)
        painter.drawLine(0, height // 2, width, height // 2)
    
    def draw_boat(self, painter):
        """Dibujar el barco (versión provisional/simple)"""
        center_x = self.width() // 2 + self.boat_x
        center_y = self.height() // 2 + self.boat_y
        
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.boat_angle)
        
        # Sombra del barco
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 50))
        painter.drawEllipse(-40, -25, 80, 50)
        
        # Cuerpo del barco (forma de barco simplificada)
        painter.setPen(QPen(QColor(44, 62, 80), 3))
        painter.setBrush(QColor(236, 240, 241))
        
        # Casco principal
        path = QPainterPath()
        path.moveTo(-35, 0)
        path.lineTo(-25, -15)
        path.lineTo(25, -15)
        path.lineTo(35, 0)
        path.lineTo(25, 15)
        path.lineTo(-25, 15)
        path.closeSubpath()
        
        painter.drawPath(path)
        
        # Cabina
        painter.setBrush(QColor(52, 152, 219))
        painter.drawRect(-15, -10, 30, 20)
        
        # Ventanas
        painter.setBrush(QColor(127, 140, 141))
        painter.drawRect(-10, -7, 8, 6)
        painter.drawRect(2, -7, 8, 6)
        
        # Proa (frente)
        painter.setBrush(QColor(231, 76, 60))
        painter.drawEllipse(30, -5, 10, 10)
        
        # Indicador de dirección
        if self.is_moving:
            painter.setPen(QPen(QColor(46, 204, 113), 3))
            painter.drawLine(0, 0, 45, 0)
            # Flecha
            painter.drawLine(45, 0, 38, -7)
            painter.drawLine(45, 0, 38, 7)
        
        painter.restore()
    
    def draw_indicators(self, painter):
        """Dibujar indicadores de posición y ángulo"""
        # Indicador de ángulo
        painter.setPen(QColor(255, 255, 255, 200))
        painter.drawText(10, 30, f"Ángulo: {int(self.boat_angle)}°")
        painter.drawText(10, 50, f"Posición: ({int(self.boat_x)}, {int(self.boat_y)})")
        painter.drawText(10, 70, f"Estado: {self.current_command}")
    
    def update_animation(self):
        """Actualizar animación"""
        # Actualizar offset de olas
        if self.water_effect:
            self.wave_offset = (self.wave_offset + 1) % 360
        
        # Animación suave de movimiento
        if self.is_moving:
            # Interpolar posición
            diff_x = self.target_x - self.boat_x
            diff_y = self.target_y - self.boat_y
            diff_angle = self.target_angle - self.boat_angle
            
            # Normalizar ángulo
            while diff_angle > 180:
                diff_angle -= 360
            while diff_angle < -180:
                diff_angle += 360
            
            # Movimiento suave
            self.boat_x += diff_x * 0.1
            self.boat_y += diff_y * 0.1
            self.boat_angle += diff_angle * 0.1
            
            # Verificar si llegó al objetivo
            if abs(diff_x) < 1 and abs(diff_y) < 1 and abs(diff_angle) < 1:
                self.boat_x = self.target_x
                self.boat_y = self.target_y
                self.boat_angle = self.target_angle
        
        self.update()
    
    def animate_movement(self, command):
        """Animar movimiento según comando"""
        self.current_command = command
        self.is_moving = True
        
        move_distance = 50
        
        if command == "ADELANTE":
            self.target_y -= move_distance
            self.status_label.setText("🚤 Moviendo ADELANTE ⬆️")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(46, 204, 113, 0.8);
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
            
        elif command == "ATRAS":
            self.target_y += move_distance
            self.status_label.setText("🚤 Moviendo ATRÁS ⬇️")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(52, 152, 219, 0.8);
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
            
        elif command == "IZQUIERDA":
            self.target_angle -= 30
            self.status_label.setText("🚤 Girando IZQUIERDA ⬅️")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(241, 196, 15, 0.8);
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
            
        elif command == "DERECHA":
            self.target_angle += 30
            self.status_label.setText("🚤 Girando DERECHA ➡️")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(230, 126, 34, 0.8);
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
            
        elif command == "PARAR":
            self.is_moving = False
            self.status_label.setText("🚤 DETENIDO 🛑")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(231, 76, 60, 0.8);
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
        
        # Mantener el barco dentro de límites
        max_offset = 200
        self.target_x = max(-max_offset, min(max_offset, self.target_x))
        self.target_y = max(-max_offset, min(max_offset, self.target_y))
        
        # Timer para volver a reposo
        QTimer.singleShot(2000, self.return_to_idle)
    
    def return_to_idle(self):
        """Volver al estado de reposo"""
        if self.current_command != "PARAR":
            self.is_moving = False
            self.status_label.setText("🚤 Vista del Barco - En Reposo")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(52, 152, 219, 0.8);
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
    
    def set_enabled(self, enabled):
        """Habilitar/deshabilitar visualización"""
        self.enabled = enabled
        self.update()
    
    def set_water_effect(self, enabled):
        """Habilitar/deshabilitar efecto de agua"""
        self.water_effect = enabled
        self.update()
