# ESP32 Boat Control - GUI

Interfaz gráfica profesional para control remoto del barco ESP32 via ESP-NOW.

## 📦 Instalación

### Requisitos
- Python 3.8 o superior
- Entorno virtual (recomendado)

### Instalar dependencias

```bash
# Crear entorno virtual (si no existe)
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## 🚀 Uso

```bash
python main.py
```

## ✨ Características

- 🎮 **Control Intuitivo**: Botones grandes con atajos de teclado (W/A/S/D/P)
- 🚤 **Visualización 3D**: Vista del barco con animaciones en tiempo real
- 🌊 **Efecto de Agua**: Animación de olas para mayor realismo
- 📡 **Conexión Serial**: Comunicación directa con ESP32
- 📋 **Registro de Eventos**: Consola de logs con timestamps
- ⚙️ **Opciones Configurables**: Habilitar/deshabilitar visualización 3D y efectos

## 🎨 Interfaz

### Panel de Control
- **Conexión Serial**: Selección automática de puertos COM
- **Controles de Movimiento**: 
  - ⬆️ Adelante (W)
  - ⬇️ Atrás (S)
  - ⬅️ Izquierda (A)
  - ➡️ Derecha (D)
  - 🛑 Parar (P)

### Visualización 3D
- Representación gráfica del barco en agua
- Animaciones suaves de movimiento y rotación
- Indicadores de posición y ángulo
- Efecto de agua con olas animadas

## 🔧 Configuración

### Velocidad del Puerto Serial
Por defecto: **115200 baudios**

### Comandos Enviados
- `adelante` - Mover hacia adelante
- `atras` - Mover hacia atrás
- `izquierda` - Girar a la izquierda
- `derecha` - Girar a la derecha
- `parar` - Detener motores

## 🐛 Solución de Problemas

### No se detectan puertos COM
1. Verificar que el ESP32 esté conectado
2. Instalar drivers CH340/CP2102 si es necesario
3. Presionar el botón "🔄" para actualizar la lista

### Error al conectar
1. Cerrar otros programas que usen el puerto (Arduino IDE, etc.)
2. Verificar que la velocidad sea 115200 baudios
3. Reiniciar el ESP32

### Visualización 3D lenta
1. Deshabilitar el efecto de agua
2. Deshabilitar la visualización 3D completamente
3. Cerrar otras aplicaciones pesadas

## 📄 Licencia

Parte del proyecto ESP32-Boat-Control-ESPNOW
