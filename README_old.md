# Sistema de Control de Barco con ESP-NOW

Sistema de control remoto para barco usando dos ESP32-S3 comunicándose por protocolo ESP-NOW.

## Componentes

- **ESP32-S3 Control**: Transmisor con antena adicional (20m de alcance)
- **ESP32-S3 Barco**: Receptor conectado al sistema de motores
- **L298N**: Módulo puente H para control de motores
- **2 Motorreductores**: Para movimiento de las aspas del barco

## Conexiones ESP32 del Barco

```
ESP32-S3 → L298N
GPIO 18  → IN1  (Motor A Dirección 1)
GPIO 19  → IN2  (Motor A Dirección 2)
GPIO 20  → IN3  (Motor B Dirección 1)
GPIO 21  → IN4  (Motor B Dirección 2)
GPIO 5   → ENA  (Motor A Velocidad PWM)
GPIO 6   → ENB  (Motor B Velocidad PWM)

Alimentación:
Batería + → L298N +12V
Batería - → L298N GND
ESP32 GND → L298N GND (IMPORTANTE: Tierra común)

Motores:
Motor Izquierdo → L298N Motor A (OUT1, OUT2)
Motor Derecho   → L298N Motor B (OUT3, OUT4)
```

## Configuración Inicial

### Paso 1: Obtener direcciones MAC

1. **ESP32 Control**:
   - Sube `EspControl/EspControl.ino`
   - Abre monitor serie (115200 baudios)
   - Copia la dirección MAC que aparece

2. **ESP32 Barco**:
   - Sube `EspBarco/EspBarco.ino` 
   - Abre monitor serie (115200 baudios)
   - Copia la dirección MAC que aparece

### Paso 2: Configurar MACs en el código

1. En `EspControl/EspControl.ino`, línea ~25:
   ```cpp
   uint8_t direccionMAC_Barco[] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF};
   ```
   Reemplaza con la MAC real del ESP32 del barco.

2. En `EspBarco/EspBarco.ino`, línea ~60:
   ```cpp
   uint8_t direccionMAC_Control[] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF};
   ```
   Reemplaza con la MAC real del ESP32 de control.

### Paso 3: Subir códigos actualizados

Vuelve a subir ambos códigos con las MACs correctas.

## Comandos Disponibles

### Movimiento Básico
- `w` o `adelante` - Mover adelante (continuo)
- `s` o `atras` - Mover atrás (continuo)  
- `a` o `izquierda` - Girar izquierda (continuo)
- `d` o `derecha` - Girar derecha (continuo)
- `parar` o `p` - Parar motores

### Movimiento con Tiempo
- `adelante 2000` - Adelante por 2 segundos
- `derecha 1500` - Girar derecha por 1.5 segundos
- `atras 3000` - Atrás por 3 segundos

### Configuración
- `vel 150` - Establecer velocidad (0-255)
- `estado` - Mostrar estado actual del barco
- `mac` - Mostrar MAC configurada

### Ayuda
- `help`, `ayuda`, `h`, `?` - Mostrar ayuda

## Funcionamiento

### ESP32 Control
- Recibe comandos por consola serie
- Transmite comandos al barco vía ESP-NOW
- Muestra estado del barco en tiempo real
- Alcance: hasta 20 metros con antena adicional

### ESP32 Barco
- Recibe comandos del control
- Controla motores mediante PWM y dirección
- Envía confirmación de estado
- Ejecuta comandos temporales automáticamente

## Movimientos del Barco

- **Adelante**: Ambos motores hacia adelante
- **Atrás**: Ambos motores hacia atrás  
- **Izquierda**: Motor izquierdo atrás, derecho adelante
- **Derecha**: Motor izquierdo adelante, derecho atrás
- **Parar**: Ambos motores detenidos

## Solución de Problemas

### Sin comunicación
1. Verificar que las MACs estén correctamente configuradas
2. Comprobar que ambos ESP32 estén encendidos
3. Verificar la distancia (máximo 20m)
4. Usar comando `mac` para verificar configuración

### Motores no funcionan
1. Verificar conexiones según diagrama
2. Comprobar tierra común entre ESP32 y L298N
3. Verificar alimentación de 12V al L298N
4. Probar con velocidades más altas (`vel 255`)

### Respuesta lenta
1. Reducir distancia entre ESP32s
2. Verificar interferencias WiFi
3. Revisar alimentación estable

## Archivos del Proyecto

- `EspControl/EspControl.ino` - Código del ESP32 transmisor
- `EspBarco/EspBarco.ino` - Código del ESP32 receptor
- `arduino_config.h` - Configuración de MACs y pines
- `README.md` - Este archivo de documentación