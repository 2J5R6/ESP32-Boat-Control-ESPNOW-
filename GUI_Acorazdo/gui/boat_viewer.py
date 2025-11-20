"""
Visualizador 3D del Barco
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QRadialGradient, QPainterPath, QImage, QPixmap
import math
import os

class BoatViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.enabled = True
        self.water_effect = True
        self.use_glb_model = False  # Nueva opción
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
        
        # Modelo 3D GLB
        self.glb_renderer = None
        self.glb_image = None
        self.glb_scale = 1.0
        
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
        
        # Dibujar barco (GLB o provisional)
        if self.use_glb_model and self.glb_image:
            self.draw_glb_boat(painter)
        else:
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
    
    def draw_glb_boat(self, painter):
        """Dibujar el barco usando modelo GLB"""
        center_x = self.width() // 2 + self.boat_x
        center_y = self.height() // 2 + self.boat_y
        
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.boat_angle)
        
        # Sombra del barco
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 50))
        shadow_size = 150 * self.glb_scale
        painter.drawEllipse(-shadow_size//2, -shadow_size//3, shadow_size, shadow_size//1.5)
        
        # Dibujar imagen del modelo 3D
        if self.glb_image:
            img_width = int(self.glb_image.width() * self.glb_scale)
            img_height = int(self.glb_image.height() * self.glb_scale)
            
            # Centrar la imagen
            target_rect = (-img_width // 2, -img_height // 2, img_width, img_height)
            painter.drawImage(*target_rect, self.glb_image)
        
        # Indicador de dirección
        if self.is_moving:
            painter.setPen(QPen(QColor(46, 204, 113), 4))
            arrow_length = 80 * self.glb_scale
            painter.drawLine(0, 0, arrow_length, 0)
            # Flecha
            painter.drawLine(arrow_length, 0, arrow_length - 15, -12)
            painter.drawLine(arrow_length, 0, arrow_length - 15, 12)
        
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
    
    def set_glb_model(self, enabled):
        """Habilitar/deshabilitar modelo GLB real"""
        self.use_glb_model = enabled
        
        if enabled and not self.glb_image:
            # Cargar modelo GLB la primera vez
            self.load_glb_model()
        
        self.update()
    
    def load_glb_model(self):
        """Cargar y renderizar el modelo GLB"""
        try:
            import trimesh
            import numpy as np
            from PIL import Image
            import io
            
            # Ruta al archivo GLB
            glb_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Public', 'Barco.glb')
            
            if not os.path.exists(glb_path):
                print(f"⚠️ No se encontró el archivo: {glb_path}")
                return
            
            # Cargar modelo
            print(f"📦 Cargando modelo 3D: {glb_path}")
            mesh = trimesh.load(glb_path)
            
            # Si es una escena, tomar la geometría principal
            if isinstance(mesh, trimesh.Scene):
                mesh = trimesh.util.concatenate([
                    trimesh.Trimesh(vertices=g.vertices, faces=g.faces)
                    for g in mesh.geometry.values()
                ])
            
            # Renderizar a imagen
            # Crear una escena con el mesh
            scene = trimesh.Scene(mesh)
            
            # Configurar vista desde arriba (vista de pájaro)
            # Rotar para vista superior
            rotation_matrix = trimesh.transformations.rotation_matrix(
                np.radians(-90),  # 90 grados
                [1, 0, 0]  # Rotar alrededor del eje X
            )
            mesh.apply_transform(rotation_matrix)
            
            # Obtener los límites del modelo
            bounds = mesh.bounds
            extents = bounds[1] - bounds[0]
            max_extent = max(extents)
            
            # Calcular escala para que se vea bien
            target_size = 200  # Tamaño objetivo en píxeles
            self.glb_scale = target_size / max_extent if max_extent > 0 else 1.0
            
            # Renderizar a imagen PNG
            png_data = mesh.export(file_type='png', resolution=[400, 400])
            
            # Convertir a QImage
            pil_image = Image.open(io.BytesIO(png_data))
            pil_image = pil_image.convert('RGBA')
            
            # Convertir PIL a QImage
            data = pil_image.tobytes('raw', 'RGBA')
            self.glb_image = QImage(data, pil_image.width, pil_image.height, QImage.Format.Format_RGBA8888)
            
            print("✅ Modelo 3D cargado correctamente")
            
        except ImportError as e:
            print(f"⚠️ Faltan dependencias para cargar modelo 3D: {e}")
            print("Ejecuta: pip install trimesh pyglet pillow")
        except Exception as e:
            print(f"❌ Error al cargar modelo GLB: {e}")
            import traceback
            traceback.print_exc()
