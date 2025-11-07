# 🚤 Sistema de Control de Barco ESP32 con ESP-NOW

<div align="center">
  <img src="https://img.shields.io/badge/ESP32-S3-red?style=for-the-badge" alt="ESP32-S3">
  <img src="https://img.shields.io/badge/Protocol-ESP--NOW-blue?style=for-the-badge" alt="ESP-NOW">
  <img src="https://img.shields.io/badge/Range-20m-green?style=for-the-badge" alt="20m Range">
  <img src="https://img.shields.io/badge/Motors-L298N-orange?style=for-the-badge" alt="L298N">
</div>

## 📋 **Descripción**

Sistema de control remoto profesional para embarcación usando dos ESP32-S3 comunicándose mediante protocolo ESP-NOW. Permite control bidireccional con comandos de movimiento, velocidad variable y confirmación de estado en tiempo real.

## ⚡ **Características Principales**

- 🔄 **Comunicación bidireccional** ESP-NOW (hasta 20m)
- 🎮 **Control completo de movimiento** (adelante, atrás, giros)
- ⚙️ **Control de velocidad PWM** (0-255)
- ⏱️ **Comandos temporales** con duración específica
- 📡 **Feedback en tiempo real** del estado del barco
- 🔧 **Configuración flexible** de pines y parámetros
- 🛡️ **Modo failsafe** sin conexión ENA/ENB

## 🔧 **Hardware Requerido**

| Componente | Descripción | Cantidad |
|------------|-------------|----------|
| **ESP32-S3** | Microcontrolador con WiFi | 2 |
| **L298N** | Módulo puente H dual | 1 |
| **Motorreductores** | Motores DC con reductora | 2 |
| **Batería 12V** | Alimentación para motores | 1 |
| **Cables Dupont** | Conexiones | 10-15 |

## 📐 **Esquema de Conexiones**

### ESP32 Barco ↔ L298N
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   ESP32-S3  │    │    L298N    │    │   MOTORES   │
│   (BARCO)   │    │  PUENTE H   │    │             │
├─────────────┤    ├─────────────┤    ├─────────────┤
│ GPIO 18 ────┼────┤ IN1         │    │             │
│ GPIO 17 ────┼────┤ IN2         │    │ Motor A ────┤ OUT1, OUT2
│ GPIO 16 ────┼────┤ IN3         │    │ (Izq)       │
│ GPIO 4  ────┼────┤ IN4         │    │             │
│             │    │             │    │             │
│ 5V      ────┼────┤ VCC         │    │ Motor B ────┤ OUT3, OUT4
│ GND     ────┼────┤ GND         │    │ (Der)       │
│             │    │             │    │             │
│ [OPCIONAL]  │    │ ENA ════════╪════┤ 5V Direct   │
│ GPIO 2  ────┼────┤ ENB ════════╪════┤ 5V Direct   │
│             │    │             │    │             │
│             │    │ +12V ───────┼────┤ BATERÍA +   │
│             │    │ GND  ───────┼────┤ BATERÍA -   │
└─────────────┘    └─────────────┘    └─────────────┘
```

### ⚠️ **Configuraciones de Velocidad**

El sistema soporta **dos modos de operación**:

#### **Modo 1: Control PWM (Recomendado)**
- **ENA** → GPIO 2 (Control PWM)
- **ENB** → GPIO 15 (Control PWM)
- ✅ **Control de velocidad variable** (0-255)
- ✅ **Consumo eficiente** de batería

#### **Modo 2: Velocidad Fija (Failsafe)**
- **ENA** → 5V directo
- **ENB** → 5V directo  
- ✅ **Velocidad máxima constante**
- ✅ **Funcionamiento garantizado**
- ⚠️ **Mayor consumo** de batería

> **💡 Tip**: Si tienes problemas con PWM, usa el **Modo 2** conectando ENA/ENB directamente a 5V. El sistema funcionará a velocidad fija pero de manera confiable.

## 🚀 **Configuración Rápida**

### 1. **Obtener Direcciones MAC**

```bash
# 1. Sube EspControl.ino al ESP32 de control
# 2. Abre Monitor Serie (115200 bps)
# 3. Copia la MAC mostrada: "MAC Address: XX:XX:XX:XX:XX:XX"

# 4. Sube EspBarco.ino al ESP32 del barco  
# 5. Abre Monitor Serie (115200 bps)
# 6. Copia la MAC mostrada: "MAC Address: XX:XX:XX:XX:XX:XX"
```

### 2. **Configurar MACs en Código**

**En `EspControl.ino` línea ~15:**
```cpp
uint8_t macBarco[] = {0x98, 0xA3, 0x16, 0xE5, 0x9F, 0x90}; // ← Cambiar por MAC real del barco
```

**En `EspBarco.ino` línea ~25:**  
```cpp
uint8_t macControl[] = {0x24, 0x58, 0x7C, 0xCE, 0x3C, 0xCC}; // ← Cambiar por MAC real del control
```

### 3. **Resubir Códigos**
Sube ambos códigos nuevamente con las MACs actualizadas.

## 🎮 **Manual de Comandos**

### **Movimiento Básico**
| Comando | Acción | Ejemplo |
|---------|--------|---------|
| `w` / `adelante` | Avanzar continuo | `w` |
| `s` / `atras` | Retroceder continuo | `s` |
| `a` / `izquierda` | Girar izquierda continuo | `a` |
| `d` / `derecha` | Girar derecha continuo | `d` |
| `p` / `parar` | Detener motores | `p` |

### **Movimiento Temporal**
| Comando | Acción | Ejemplo |
|---------|--------|---------|
| `adelante [ms]` | Avanzar por tiempo específico | `adelante 2000` |
| `atras [ms]` | Retroceder por tiempo específico | `atras 1500` |
| `izquierda [ms]` | Girar izquierda por tiempo | `izquierda 1000` |
| `derecha [ms]` | Girar derecha por tiempo | `derecha 800` |

### **Control de Velocidad**
| Comando | Acción | Rango | Ejemplo |
|---------|--------|-------|---------|
| `vel [0-255]` | Establecer velocidad PWM | 0-255 | `vel 150` |
| `lento` | Velocidad baja (100) | - | `lento` |
| `medio` | Velocidad media (180) | - | `medio` |
| `rapido` | Velocidad alta (255) | - | `rapido` |

### **Información y Diagnóstico**
| Comando | Acción | Respuesta |
|---------|--------|-----------|
| `estado` | Estado actual del barco | Velocidad, último comando |
| `mac` | Mostrar MAC configurada | Dirección MAC del barco |
| `help` / `?` | Mostrar ayuda | Lista de comandos |

## 📊 **Funcionamiento del Sistema**

### **ESP32 Control (Transmisor)**
- 📤 **Transmite** comandos via ESP-NOW
- 🖥️ **Interfaz** de consola serie (115200 bps)
- 📡 **Alcance** de hasta 20m con antena
- ✅ **Confirmación** de recepción de comandos

### **ESP32 Barco (Receptor)**  
- 📥 **Recibe** comandos del control
- ⚙️ **Ejecuta** movimientos y ajustes
- 🔄 **Envía** confirmación de estado
- 🛡️ **Auto-stop** en comandos temporales

### **Lógica de Movimientos**

| Movimiento | Motor Izq (A) | Motor Der (B) | Resultado |
|------------|---------------|---------------|-----------|
| **Adelante** | IN1=1, IN2=0 | IN3=1, IN4=0 | ⬆️ Avance recto |
| **Atrás** | IN1=0, IN2=1 | IN3=0, IN4=1 | ⬇️ Retroceso recto |
| **Izquierda** | IN1=0, IN2=1 | IN3=1, IN4=0 | ↺ Giro antihorario |
| **Derecha** | IN1=1, IN2=0 | IN3=0, IN4=1 | ↻ Giro horario |
| **Parar** | IN1=0, IN2=0 | IN3=0, IN4=0 | ⏹️ Detención |

## 🛠️ **Solución de Problemas**

### ❌ **Sin Comunicación ESP-NOW**
```bash
# Síntomas: Comandos no llegan al barco
✅ Verificar MACs correctamente configuradas
✅ Comprobar distancia (máximo 20m)  
✅ Reiniciar ambos ESP32
✅ Verificar monitor serie: "Callback registrado OK"
```

### ❌ **Motores No Responden**
```bash
# Síntomas: Recibe comandos pero motores inmóviles
✅ Verificar alimentación 12V al L298N
✅ Comprobar conexión GND común ESP32-L298N
✅ Probar ENA/ENB conectados directo a 5V (Modo Failsafe)
✅ Verificar cables sueltos
✅ Usar comando: vel 255 (velocidad máxima)
```

### ❌ **Movimiento Errático**
```bash
# Síntomas: Movimientos impredecibles
✅ Verificar conexiones IN1, IN2, IN3, IN4
✅ Comprobar polaridad de motores
✅ Revisar alimentación estable
✅ Probar con velocidades más bajas
```

### ❌ **Alcance Limitado**
```bash
# Síntomas: Funciona solo de cerca
✅ Verificar antena del ESP32 de control
✅ Evitar obstáculos metálicos
✅ Minimizar interferencias WiFi
✅ Comprobar alimentación estable
```

## 📁 **Estructura del Proyecto**

```
CodigoControl/
├── 📄 README.md                    # Esta documentación
├── 📄 arduino_config.h             # Configuración de MACs y pines
├── 📄 requirements.txt             # Dependencias Python (futuras)
├── 📄 install.py                   # Script de instalación (futuro)
├── 📄 INICIO_RAPIDO.md             # Guía de inicio rápido
│
├── 🗂️ EspControl/                  # ESP32 Transmisor
│   └── 📄 EspControl.ino           # Código principal del control
│
├── 🗂️ EspBarco/                    # ESP32 Receptor 
│   ├── 📄 EspBarco.ino             # Código principal del barco
│   └── 📄 EspBarco_Simple.ino      # Versión simplificada
│
├── 🗂️ EspControl_Prueba/           # Códigos de testing
│   └── 📄 EspControl_Prueba.ino    # Pruebas de comunicación
│
└── 🐍 Python GUI/                  # Interface gráfica (futuro)
    ├── 📄 control_barco_gui.py     # GUI principal
    ├── 📄 control_barco_consola.py # Versión consola
    └── 📄 control_barco_simple.py  # Versión básica
```

## 🔄 **Versiones y Actualizaciones**

### **v1.0.0** - Sistema Base ✅
- [x] Comunicación ESP-NOW bidireccional
- [x] Control básico de movimientos  
- [x] Comandos de consola serie
- [x] Configuración de velocidad PWM

### **v1.1.0** - Funciones Avanzadas ✅  
- [x] Comandos temporales con duración
- [x] Feedback de estado en tiempo real
- [x] Modo failsafe sin ENA/ENB
- [x] Múltiples formatos de comando

### **v2.0.0** - En Desarrollo 🚧
- [ ] Interface gráfica Python
- [ ] Control por joystick/gamepad
- [ ] Telemetría avanzada
- [ ] Grabación de secuencias

## 📞 **Soporte y Contribución**

- 📧 **Issues**: Reportar problemas en GitHub Issues
- 🔧 **Pull Requests**: Contribuciones bienvenidas
- 📖 **Wiki**: Documentación extendida (próximamente)
- 💬 **Discusiones**: GitHub Discussions

## 📝 **Licencia**

Este proyecto está bajo Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

<div align="center">
  <b>🚤 Desarrollado para aplicaciones de robótica marina y control remoto</b><br>
  <i>ESP32-S3 + ESP-NOW + L298N = Control Professional</i>
</div>