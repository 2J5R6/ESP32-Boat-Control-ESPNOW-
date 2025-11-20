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
- 🚤 **Visualización Dual**: 
  - Modelo provisional 2D simple (por defecto)
  - Modelo 3D real desde archivo GLB (opcional)
- 🌊 **Efecto de Agua**: Animación de olas para mayor realismo
- 📡 **Conexión Serial**: Comunicación directa con ESP32
- 📋 **Registro de Eventos**: Consola de logs con timestamps
- ⚙️ **Opciones Configurables**: 
  - Habilitar/deshabilitar visualización 3D
  - Cambiar entre modelo provisional y modelo GLB real
  - Activar/desactivar efectos de agua

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

#### Modo Provisional (Por defecto)
- Representación gráfica simple del barco en agua
- Rápido y ligero
- No requiere dependencias adicionales

#### Modo Modelo Real (Opcional)
- Carga el modelo 3D desde `Public/Barco.glb`
- Visualización realista del barco real
- Requiere: trimesh, pyglet, pillow, numpy
- Activar con checkbox: ☑️ "Usar modelo 3D real (Barco.glb)"

**Características comunes:**
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

## 📦 Modelo 3D

El archivo `Public/Barco.glb` contiene el modelo 3D real del barco. Para usarlo:

1. Asegúrate de que las dependencias estén instaladas: `pip install -r requirements.txt`
2. En la interfaz, activa: ☑️ "Usar modelo 3D real (Barco.glb)"
3. El modelo se cargará automáticamente la primera vez

**Nota**: Si no activas esta opción, la aplicación usará el modelo provisional 2D que es más rápido y ligero.

## 🐛 Solución de Problemas

### No se detectan puertos COM
1. Verificar que el ESP32 esté conectado
2. Instalar drivers CH340/CP2102 si es necesario
3. Presionar el botón "🔄" para actualizar la lista

### Error al conectar
1. Cerrar otros programas que usen el puerto (Arduino IDE, etc.)
2. Verificar que la velocidad sea 115200 baudios
3. Reiniciar el ESP32

### Error al cargar modelo GLB
1. Verifica que el archivo `Public/Barco.glb` exista
2. Instala las dependencias: `pip install trimesh pyglet pillow numpy`
3. Si falla, usa el modelo provisional desactivando la opción

### Visualización 3D lenta
1. Deshabilitar el efecto de agua
2. Usar modelo provisional en lugar del GLB
3. Deshabilitar la visualización 3D completamente
4. Cerrar otras aplicaciones pesadas

## 📄 Licencia

Parte del proyecto ESP32-Boat-Control-ESPNOW
