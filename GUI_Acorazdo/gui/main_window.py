"""
Ventana Principal de la Aplicación
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QLabel, QComboBox, QGroupBox, 
                              QTextEdit, QSplitter, QCheckBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
import serial
import serial.tools.list_ports
from .boat_viewer import BoatViewer
from .styles import MAIN_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.serial_connection = None
        self.is_connected = False
        self.log_text = None  # Inicializar antes de refresh_ports
        self.init_ui()
        
    def init_ui(self):
        """Inicializar la interfaz de usuario"""
        self.setWindowTitle("🚤 ESP32 Boat Control - Sistema de Control Remoto")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(MAIN_STYLE)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter para dividir la pantalla
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo - Controles
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)
        
        # Panel derecho - Visualizador 3D
        self.boat_viewer = BoatViewer()
        splitter.addWidget(self.boat_viewer)
        
        # Configurar tamaños del splitter
        splitter.setStretchFactor(0, 2)  # Panel de control
        splitter.setStretchFactor(1, 3)  # Visualizador 3D
        
        main_layout.addWidget(splitter)
        
        # Timer para actualizar estado
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)
        
    def create_control_panel(self):
        """Crear panel de controles"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Título
        title = QLabel("🎮 Panel de Control")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # === SECCIÓN DE CONEXIÓN ===
        connection_group = QGroupBox("📡 Conexión Serial")
        connection_layout = QVBoxLayout()
        
        # Selector de puerto
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Puerto:"))
        self.port_combo = QComboBox()
        self.refresh_ports()
        port_layout.addWidget(self.port_combo)
        
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setMaximumWidth(40)
        self.refresh_btn.clicked.connect(self.refresh_ports)
        self.refresh_btn.setToolTip("Actualizar lista de puertos")
        port_layout.addWidget(self.refresh_btn)
        connection_layout.addLayout(port_layout)
        
        # Botón de conexión
        self.connect_btn = QPushButton("🔌 Conectar")
        self.connect_btn.clicked.connect(self.toggle_connection)
        self.connect_btn.setMinimumHeight(45)
        connection_layout.addWidget(self.connect_btn)
        
        # Estado de conexión
        self.connection_status = QLabel("⚪ Desconectado")
        self.connection_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.connection_status.setStyleSheet("color: #95a5a6; font-weight: bold;")
        connection_layout.addWidget(self.connection_status)
        
        connection_group.setLayout(connection_layout)
        layout.addWidget(connection_group)
        
        # === SECCIÓN DE CONTROLES DE MOVIMIENTO ===
        movement_group = QGroupBox("🕹️ Control de Movimiento")
        movement_layout = QVBoxLayout()
        
        # Botón Adelante
        self.forward_btn = QPushButton("⬆️ ADELANTE (W)")
        self.forward_btn.setMinimumHeight(60)
        self.forward_btn.clicked.connect(lambda: self.send_command("ADELANTE"))
        self.forward_btn.setEnabled(False)
        movement_layout.addWidget(self.forward_btn)
        
        # Botones Izquierda y Derecha
        lr_layout = QHBoxLayout()
        self.left_btn = QPushButton("⬅️ IZQUIERDA (A)")
        self.left_btn.setMinimumHeight(60)
        self.left_btn.clicked.connect(lambda: self.send_command("IZQUIERDA"))
        self.left_btn.setEnabled(False)
        lr_layout.addWidget(self.left_btn)
        
        self.right_btn = QPushButton("➡️ DERECHA (D)")
        self.right_btn.setMinimumHeight(60)
        self.right_btn.clicked.connect(lambda: self.send_command("DERECHA"))
        self.right_btn.setEnabled(False)
        lr_layout.addWidget(self.right_btn)
        movement_layout.addLayout(lr_layout)
        
        # Botón Atrás
        self.backward_btn = QPushButton("⬇️ ATRÁS (S)")
        self.backward_btn.setMinimumHeight(60)
        self.backward_btn.clicked.connect(lambda: self.send_command("ATRAS"))
        self.backward_btn.setEnabled(False)
        movement_layout.addWidget(self.backward_btn)
        
        # Botón Parar
        self.stop_btn = QPushButton("🛑 PARAR (P)")
        self.stop_btn.setMinimumHeight(60)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.stop_btn.clicked.connect(lambda: self.send_command("PARAR"))
        self.stop_btn.setEnabled(False)
        movement_layout.addWidget(self.stop_btn)
        
        movement_group.setLayout(movement_layout)
        layout.addWidget(movement_group)
        
        # === SECCIÓN DE VISUALIZACIÓN 3D ===
        viewer_group = QGroupBox("🎨 Opciones de Visualización")
        viewer_layout = QVBoxLayout()
        
        self.enable_3d_checkbox = QCheckBox("Habilitar visualización 3D")
        self.enable_3d_checkbox.setChecked(True)
        self.enable_3d_checkbox.stateChanged.connect(self.toggle_3d_view)
        viewer_layout.addWidget(self.enable_3d_checkbox)
        
        self.glb_model_checkbox = QCheckBox("Usar modelo 3D real (Barco.glb)")
        self.glb_model_checkbox.setChecked(False)
        self.glb_model_checkbox.stateChanged.connect(self.toggle_glb_model)
        self.glb_model_checkbox.setToolTip("Carga el modelo 3D desde Public/Barco.glb")
        viewer_layout.addWidget(self.glb_model_checkbox)
        
        self.water_effect_checkbox = QCheckBox("Efecto de agua")
        self.water_effect_checkbox.setChecked(True)
        self.water_effect_checkbox.stateChanged.connect(self.toggle_water_effect)
        viewer_layout.addWidget(self.water_effect_checkbox)
        
        viewer_group.setLayout(viewer_layout)
        layout.addWidget(viewer_group)
        
        # === CONSOLA DE LOGS ===
        log_group = QGroupBox("📋 Registro de Eventos")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Consolas', monospace;
                font-size: 10px;
            }
        """)
        log_layout.addWidget(self.log_text)
        
        clear_log_btn = QPushButton("🗑️ Limpiar log")
        clear_log_btn.clicked.connect(self.log_text.clear)
        log_layout.addWidget(clear_log_btn)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        layout.addStretch()
        
        return panel
    
    def refresh_ports(self):
        """Actualizar lista de puertos COM disponibles"""
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(f"{port.device} - {port.description}")
        
        if self.port_combo.count() == 0:
            self.port_combo.addItem("No hay puertos disponibles")
            self.log("⚠️ No se encontraron puertos COM disponibles")
        else:
            self.log(f"✅ Se encontraron {self.port_combo.count()} puerto(s) disponible(s)")
    
    def toggle_connection(self):
        """Conectar o desconectar del puerto serial"""
        if not self.is_connected:
            # Conectar
            port_text = self.port_combo.currentText()
            if "No hay puertos" in port_text:
                self.log("❌ Selecciona un puerto válido")
                return
            
            port = port_text.split(" - ")[0]
            
            try:
                self.serial_connection = serial.Serial(port, 115200, timeout=1)
                self.is_connected = True
                self.connect_btn.setText("🔓 Desconectar")
                self.connection_status.setText("🟢 Conectado")
                self.connection_status.setStyleSheet("color: #27ae60; font-weight: bold;")
                
                # Habilitar botones de control
                self.forward_btn.setEnabled(True)
                self.backward_btn.setEnabled(True)
                self.left_btn.setEnabled(True)
                self.right_btn.setEnabled(True)
                self.stop_btn.setEnabled(True)
                
                self.log(f"✅ Conectado a {port}")
                
            except Exception as e:
                self.log(f"❌ Error al conectar: {str(e)}")
                
        else:
            # Desconectar
            if self.serial_connection:
                self.serial_connection.close()
            
            self.is_connected = False
            self.connect_btn.setText("🔌 Conectar")
            self.connection_status.setText("⚪ Desconectado")
            self.connection_status.setStyleSheet("color: #95a5a6; font-weight: bold;")
            
            # Deshabilitar botones de control
            self.forward_btn.setEnabled(False)
            self.backward_btn.setEnabled(False)
            self.left_btn.setEnabled(False)
            self.right_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            
            self.log("🔴 Desconectado")
    
    def send_command(self, command):
        """Enviar comando al ESP32"""
        if not self.is_connected or not self.serial_connection:
            self.log("⚠️ No hay conexión activa")
            return
        
        try:
            self.serial_connection.write(f"{command.lower()}\n".encode())
            self.log(f"📤 Comando enviado: {command}")
            
            # Actualizar visualización 3D
            if self.enable_3d_checkbox.isChecked():
                self.boat_viewer.animate_movement(command)
            
        except Exception as e:
            self.log(f"❌ Error al enviar comando: {str(e)}")
    
    def toggle_3d_view(self, state):
        """Habilitar/deshabilitar visualización 3D"""
        enabled = state == Qt.CheckState.Checked.value
        self.boat_viewer.set_enabled(enabled)
        self.log(f"🎨 Visualización 3D: {'Habilitada' if enabled else 'Deshabilitada'}")
    
    def toggle_water_effect(self, state):
        """Habilitar/deshabilitar efecto de agua"""
        enabled = state == Qt.CheckState.Checked.value
        self.boat_viewer.set_water_effect(enabled)
        self.log(f"🌊 Efecto de agua: {'Habilitado' if enabled else 'Deshabilitado'}")
    
    def toggle_glb_model(self, state):
        """Habilitar/deshabilitar modelo GLB real"""
        enabled = state == Qt.CheckState.Checked.value
        self.boat_viewer.set_glb_model(enabled)
        model_type = "Modelo 3D real (Barco.glb)" if enabled else "Modelo provisional"
        self.log(f"🚤 {model_type}")
    
    def log(self, message):
        """Agregar mensaje al log"""
        if self.log_text is None:  # Si aún no está inicializado
            return
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def update_status(self):
        """Actualizar estado de la aplicación"""
        # Leer datos del puerto serial si está conectado
        if self.is_connected and self.serial_connection and self.serial_connection.in_waiting:
            try:
                data = self.serial_connection.readline().decode().strip()
                if data:
                    self.log(f"📥 {data}")
            except Exception as e:
                pass  # Ignorar errores de lectura
    
    def keyPressEvent(self, event):
        """Manejar atajos de teclado"""
        if not self.is_connected:
            return
        
        key = event.key()
        if key == Qt.Key.Key_W:
            self.send_command("ADELANTE")
        elif key == Qt.Key.Key_S:
            self.send_command("ATRAS")
        elif key == Qt.Key.Key_A:
            self.send_command("IZQUIERDA")
        elif key == Qt.Key.Key_D:
            self.send_command("DERECHA")
        elif key == Qt.Key.Key_P:
            self.send_command("PARAR")
    
    def closeEvent(self, event):
        """Manejar cierre de ventana"""
        if self.is_connected:
            self.send_command("PARAR")
            self.toggle_connection()
        event.accept()
