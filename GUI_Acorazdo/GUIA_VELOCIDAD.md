# 🚤 Guía de Control de Velocidad - GUI Actualizada

## ✨ Nuevas Características

### ⚡ Control de Velocidad
La GUI ahora incluye un sistema completo de control de velocidad con:

1. **Slider de Velocidad** (0-255)
   - Gradiente visual de colores (rojo → naranja → verde)
   - Muestra velocidad actual y porcentaje
   - Actualización en tiempo real

2. **Botones de Velocidad Preestablecida**
   - 🐢 **Lento** (50) - 20% velocidad
   - 🚶 **Medio** (150) - 59% velocidad
   - 🏃 **Rápido** (200) - 78% velocidad (por defecto)
   - 🚀 **Máximo** (255) - 100% velocidad

3. **Botón "Enviar Velocidad al Barco"**
   - Envía comando `VEL:XXX` al ESP32 del barco
   - Actualización inmediata del PWM de los motores

### 🚤 Barco Reorientado
- El modelo del barco ahora **apunta hacia ARRIBA** ⬆️
- Círculo rojo en la proa indica la dirección frontal
- Flecha verde muestra dirección de movimiento cuando está activo

## 🎮 Cómo Usar

### 1. Conectar al Barco
1. Selecciona el puerto COM del ESP32 Control
2. Clic en "🔌 Conectar"
3. Espera la confirmación "🟢 Conectado"

### 2. Configurar Velocidad
**Opción A - Slider:**
- Arrastra el slider para ajustar velocidad (0-255)
- Observa el cambio de color y porcentaje

**Opción B - Botones Rápidos:**
- Clic en 🐢/🚶/🏃/🚀 para velocidad preestablecida

### 3. Enviar Velocidad
- Clic en "📤 Enviar Velocidad al Barco"
- Verifica en el log: `📤 Velocidad enviada: 200 (78%)`

### 4. Controlar Movimiento
- **⬆️ ADELANTE (W)** - Avanza con velocidad configurada
- **⬇️ ATRÁS (S)** - Retrocede
- **⬅️ IZQUIERDA (A)** - Gira a la izquierda
- **➡️ DERECHA (D)** - Gira a la derecha
- **🛑 PARAR (P)** - Detiene motores

### 5. Cambiar Velocidad en Movimiento
1. El barco está moviéndose (por ejemplo, adelante)
2. Ajusta el slider a nueva velocidad
3. Clic en "📤 Enviar Velocidad"
4. **El barco cambia velocidad INMEDIATAMENTE** sin detenerse

## 🎨 Indicadores Visuales

### Etiqueta de Velocidad
- **🔴 Rojo (0-84)**: Velocidad lenta
- **🟠 Naranja (85-169)**: Velocidad media
- **🟢 Verde (170-255)**: Velocidad alta

### Slider con Gradiente
- Barra de progreso colorida indica el rango de velocidad
- Manija azul se puede arrastrar suavemente

### Visualizador 2D/3D
- Barco apuntando hacia arriba (proa con círculo rojo)
- Flecha verde cuando está en movimiento
- Efecto de agua animado (opcional)
- Grid de referencia

## 📊 Rangos Recomendados

| Velocidad | PWM  | Uso Recomendado          |
|-----------|------|--------------------------|
| 🐢 Lento   | 50   | Maniobras precisas      |
| 🚶 Medio   | 150  | Navegación estándar     |
| 🏃 Rápido  | 200  | Velocidad de crucero    |
| 🚀 Máximo  | 255  | Máxima potencia         |

## 🔧 Integración con ESP32

### Comandos Enviados
```
VEL:50   → Velocidad 20%
VEL:150  → Velocidad 59%
VEL:200  → Velocidad 78% (default)
VEL:255  → Velocidad 100%
```

### Transiciones Suaves
El ESP32 del barco incluye:
- **Pausa al cambiar dirección** (100ms)
- **Rampa de aceleración gradual** (10 pasos)
- **Protección del motor** contra cambios bruscos

## 🎯 Tips de Uso

1. **Inicia con velocidad media (150)** para familiarizarte
2. **Usa velocidad lenta (50)** para maniobras en espacios reducidos
3. **Velocidad máxima (255)** solo para aguas abiertas
4. **Cambia velocidad mientras navegas** sin necesidad de parar
5. **Usa atajos de teclado** W/A/S/D/P para control rápido

## 🎨 Diseño Visual

- **Interfaz moderna** con colores profesionales
- **Gradientes animados** en controles
- **Log estilo terminal** con timestamps
- **Iconos emoji** para mejor UX
- **Responsive design** con splitter ajustable

## 📝 Registro de Eventos

El log muestra:
- `⚡ Velocidad configurada: 200 (78%)`
- `📤 Velocidad enviada: 200 (78%)`
- `📤 Comando enviado: ADELANTE`
- `⬆️ Moviendo ADELANTE`

---

**Disfruta del control total de tu barco con la nueva GUI mejorada! 🚤✨**
