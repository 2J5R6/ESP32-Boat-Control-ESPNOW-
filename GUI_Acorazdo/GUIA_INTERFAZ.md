# 🚤 ESP32 Boat Control - Guía de la Interfaz Gráfica

## 📸 Descripción de la Interfaz

### Diseño Principal

La interfaz está dividida en **2 paneles principales**:

```
┌─────────────────────────────────────────────────────────────────┐
│  🚤 ESP32 Boat Control - Sistema de Control Remoto             │
├──────────────────────┬──────────────────────────────────────────┤
│                      │                                          │
│  📋 PANEL CONTROL    │    🎨 VISUALIZADOR 3D                   │
│                      │                                          │
│  ┌─────────────┐     │    ┌───────────────────────────────┐    │
│  │ 📡 Conexión │     │    │  🚤 Vista del Barco          │    │
│  │   Serial    │     │    │      (Animación en agua)     │    │
│  └─────────────┘     │    │                              │    │
│                      │    │         🌊🌊🌊                │    │
│  ┌─────────────┐     │    │      ╭───────╮              │    │
│  │ 🕹️ Control   │     │    │      │  🚤   │              │    │
│  │  Movimiento │     │    │      ╰───────╯              │    │
│  │             │     │    │         🌊🌊🌊                │    │
│  │  ⬆️ Adelante │     │    │                              │    │
│  │  ⬅️  ⬇️  ➡️  │     │    │  Ángulo: 0°                 │    │
│  │  🛑 Parar   │     │    │  Posición: (0, 0)           │    │
│  └─────────────┘     │    │  Estado: PARADO              │    │
│                      │    └───────────────────────────────┘    │
│  ┌─────────────┐     │                                          │
│  │ 🎨 Opciones │     │                                          │
│  │             │     │                                          │
│  │ ☑️ Visual 3D │     │                                          │
│  │ ☑️ Efecto H2O│     │                                          │
│  └─────────────┘     │                                          │
│                      │                                          │
│  ┌─────────────┐     │                                          │
│  │ 📋 Log      │     │                                          │
│  │ [12:30:15]  │     │                                          │
│  │ ✅ Conectado │     │                                          │
│  │ 📤 ADELANTE │     │                                          │
│  └─────────────┘     │                                          │
└──────────────────────┴──────────────────────────────────────────┘
```

---

## 🎮 Panel de Control (Izquierda)

### 1️⃣ Conexión Serial

**Elementos:**
- 🔽 **Selector de Puerto**: Lista automática de puertos COM disponibles
- 🔄 **Botón Refresh**: Actualiza la lista de puertos
- 🔌 **Botón Conectar**: Establece conexión serial a 115200 baudios
- 🟢 **Indicador de Estado**: 
  - ⚪ Desconectado (gris)
  - 🟢 Conectado (verde)

**Cómo usar:**
1. Conecta el ESP32 por USB
2. Selecciona el puerto (ej: COM3)
3. Presiona "🔌 Conectar"
4. Espera la luz verde 🟢

---

### 2️⃣ Control de Movimiento

**Botones disponibles:**

| Botón | Atajo | Comando | Color | Descripción |
|-------|-------|---------|-------|-------------|
| ⬆️ **ADELANTE** | W | `adelante` | 🟦 Azul | Avanza hacia adelante |
| ⬇️ **ATRÁS** | S | `atras` | 🟦 Azul | Retrocede |
| ⬅️ **IZQUIERDA** | A | `izquierda` | 🟦 Azul | Gira a la izquierda |
| ➡️ **DERECHA** | D | `derecha` | 🟦 Azul | Gira a la derecha |
| 🛑 **PARAR** | P | `parar` | 🟥 Rojo | Detiene motores |

**Estados visuales:**
- **Deshabilitado** (gris): Sin conexión
- **Habilitado** (azul): Listo para usar
- **Hover** (azul oscuro): Al pasar el mouse
- **Presionado** (azul muy oscuro): Al hacer clic

---

### 3️⃣ Opciones de Visualización

**Controles:**
- ☑️ **Habilitar visualización 3D**: 
  - ✅ Activado: Muestra animación del barco
  - ❌ Desactivado: Pantalla gris con texto
  
- ☑️ **Efecto de agua**:
  - ✅ Activado: Animación de olas en movimiento
  - ❌ Desactivado: Fondo azul sólido

**Cuándo deshabilitar:**
- Computadora lenta
- Para presentaciones estáticas
- Ahorro de recursos

---

### 4️⃣ Registro de Eventos

**Formato del log:**
```
[HH:MM:SS] Mensaje
```

**Tipos de mensajes:**
- `✅` Operaciones exitosas (verde)
- `❌` Errores (rojo)
- `⚠️` Advertencias (amarillo)
- `📤` Comandos enviados
- `📥` Respuestas recibidas

**Ejemplo de log:**
```
[12:30:15] ✅ Se encontraron 2 puerto(s) disponibles
[12:30:18] ✅ Conectado a COM3
[12:30:22] 📤 Comando enviado: ADELANTE
[12:30:25] 📤 Comando enviado: PARAR
```

**Botón:** 🗑️ **Limpiar log** - Borra todo el historial

---

## 🎨 Visualizador 3D (Derecha)

### Componentes Visuales

#### 1. Barra de Estado Superior
```
┌─────────────────────────────────────────────┐
│ 🚤 Vista del Barco - En Reposo              │
└─────────────────────────────────────────────┘
```

**Colores según estado:**
- 🟦 **Azul**: En reposo / Moviendo atrás
- 🟩 **Verde**: Moviendo adelante
- 🟨 **Amarillo**: Girando izquierda
- 🟧 **Naranja**: Girando derecha
- 🟥 **Rojo**: Detenido

#### 2. Escena del Agua

**Elementos:**
- 🌊 **Gradiente de agua**: De azul claro (arriba) a azul oscuro (abajo)
- 〰️ **Olas animadas**: Líneas onduladas en movimiento continuo
- ⊞ **Grid de referencia**: Cuadrícula semi-transparente
- ✚ **Cruz central**: Marca el punto de origen (0,0)

#### 3. El Barco

**Diseño simplificado:**
```
        ┌──┐
    ╭──┤██├──╮
    │  └──┘  │
    │  ▓▓▓▓  │
    ╰────●───╯
         ↑ (proa roja)
```

**Componentes:**
- **Casco blanco**: Forma naviera aerodinámica
- **Cabina azul**: Con ventanas grises
- **Proa roja**: Círculo rojo al frente (dirección)
- **Sombra**: Debajo del barco para profundidad
- **Flecha verde**: Aparece al moverse (dirección del movimiento)

#### 4. Indicadores

**Información en tiempo real:**
```
Ángulo: 45°
Posición: (150, -75)
Estado: ADELANTE
```

---

## 🎬 Animaciones

### Movimientos del Barco

| Comando | Animación | Efecto Visual |
|---------|-----------|---------------|
| **ADELANTE** | Desplazamiento hacia arriba | Barco sube (-Y), flecha verde apunta adelante |
| **ATRÁS** | Desplazamiento hacia abajo | Barco baja (+Y), flecha verde apunta atrás |
| **IZQUIERDA** | Rotación antihoraria | Barco rota -30°, giro suave |
| **DERECHA** | Rotación horaria | Barco rota +30°, giro suave |
| **PARAR** | Detención | Barco se detiene, sin flecha |

### Características de Animación

- ⏱️ **Duración**: 2 segundos por comando
- 🌊 **Interpolación suave**: Movimiento fluido (easing)
- 🔄 **Límites**: El barco se mantiene dentro de ±200 píxeles del centro
- 🎯 **Precisión**: Posición y ángulo exactos
- ♾️ **Olas continuas**: Siempre en movimiento (60 FPS)

---

## ⌨️ Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| **W** | Adelante |
| **S** | Atrás |
| **A** | Izquierda |
| **D** | Derecha |
| **P** | Parar |

> **Nota:** Los atajos solo funcionan cuando hay conexión activa

---

## 🎨 Paleta de Colores

### Colores Principales

| Elemento | Color | Código | Uso |
|----------|-------|--------|-----|
| Fondo oscuro | Gris oscuro | `#2c3e50` | Panel de control |
| Fondo medio | Gris medio | `#34495e` | Widgets |
| Primario | Azul | `#3498db` | Botones, bordes |
| Primario hover | Azul oscuro | `#2980b9` | Hover de botones |
| Éxito | Verde | `#27ae60` | Conectado |
| Advertencia | Amarillo | `#f39c12` | Warnings |
| Error | Rojo | `#e74c3c` | Errores, parar |
| Texto claro | Blanco humo | `#ecf0f1` | Texto principal |

### Agua

| Capa | Color | Código |
|------|-------|--------|
| Superficie | Azul claro | `#2980b9` |
| Media | Azul medio | `#3498db` |
| Profunda | Azul oscuro | `#154360` |

---

## 🖼️ Diseño Responsivo

La interfaz se adapta al tamaño de ventana:

- **Mínimo**: 1200 x 800 px
- **Recomendado**: 1400 x 900 px
- **Pantalla completa**: Soportado

**Splitter ajustable:**
- Arrastra la línea divisoria para ajustar el tamaño de los paneles
- Panel control: 40% del ancho
- Visualizador: 60% del ancho

---

## 🎯 Flujo de Uso Típico

### Para Control Rápido

1. **Conexión rápida** (5 segundos):
   ```
   1. Seleccionar puerto → 2. Conectar → 3. Listo
   ```

2. **Control con teclado**:
   ```
   W = Adelante
   A/D = Girar
   S = Atrás
   P = Parar
   ```

### Para Presentación/Demo

1. **Configurar visualización**:
   - ✅ Habilitar visualización 3D
   - ✅ Activar efecto de agua
   - Maximizar ventana

2. **Usar botones grandes**:
   - Clics en los botones grandes del panel
   - La animación 3D mostrará el movimiento
   - El log registra todos los comandos

---

## 💡 Tips y Trucos

### Optimización

- **PC lenta?** → Desactiva el efecto de agua
- **Muy lenta?** → Desactiva la visualización 3D completa
- **Solo logs?** → Arrastra el splitter para agrandar el panel de control

### Debugging

- **No se mueve el barco real?** → Revisa el log de eventos
- **Comandos no llegan?** → Verifica la conexión serial
- **Puerto ocupado?** → Cierra Arduino IDE u otras aplicaciones

### Presentaciones

1. Maximiza la ventana
2. Activa todas las opciones visuales
3. Usa el teclado para control rápido
4. El log muestra actividad en tiempo real

---

## 🔧 Configuración Avanzada

### Modificar Velocidad del Puerto

Edita `main_window.py`, línea de conexión:
```python
self.serial_connection = serial.Serial(port, 115200, timeout=1)
                                            ^^^^^^ Cambia aquí
```

### Ajustar Velocidad de Animación

Edita `boat_viewer.py`:
```python
self.animation_timer.start(16)  # 16ms = ~60 FPS
                           ^^    # Aumenta para ralentizar
```

### Personalizar Colores

Edita `styles.py` para cambiar toda la paleta de colores.

---

## 📊 Especificaciones Técnicas

| Característica | Valor |
|----------------|-------|
| Framework | PyQt6 |
| Puerto Serial | 115200 baud |
| FPS Animación | 60 |
| Timeout Serial | 1 segundo |
| Resolución mínima | 1200x800 |
| Formato de comandos | Texto plano UTF-8 |

---

## 🎓 Para el Póster

### Elementos Clave a Destacar

1. **📸 Captura de pantalla**: Interfaz completa en acción
2. **🎨 Diseño profesional**: Colores modernos, iconos claros
3. **🚤 Visualización 3D**: Animación del barco en agua
4. **🎮 Control intuitivo**: Botones grandes + teclado
5. **📡 Conexión directa**: USB → ESP32 en tiempo real
6. **📋 Monitoreo**: Log de eventos con timestamps

### Capturas Recomendadas

```
┌─────────────────────────────────────────┐
│ 1. Interfaz completa en reposo          │
│    (Mostrar diseño limpio)               │
├─────────────────────────────────────────┤
│ 2. Barco en movimiento                   │
│    (Animación con flecha verde)          │
├─────────────────────────────────────────┤
│ 3. Panel de control activo               │
│    (Botones azules, estado verde)        │
├─────────────────────────────────────────┤
│ 4. Log con actividad                     │
│    (Varios comandos registrados)         │
└─────────────────────────────────────────┘
```

---

## ✨ Características Destacables

✅ **Interfaz Profesional** - Diseño moderno con PyQt6  
✅ **Control Dual** - Botones grandes + atajos de teclado  
✅ **Visualización 3D** - Animaciones fluidas del barco  
✅ **Efecto de Agua** - Olas animadas realistas  
✅ **Conexión Serial** - Comunicación directa con ESP32  
✅ **Log en Tiempo Real** - Historial completo de eventos  
✅ **Opciones Configurables** - Adaptar según necesidades  
✅ **Responsive** - Panel ajustable con splitter  

---

**¡Listo para tu presentación! 🎉**
