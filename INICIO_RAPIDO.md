# 🚀 Inicio Rápido - Control de Barco ESP32

## ⚡ **Setup en 5 minutos**

### **1. Hardware - Conectar cables**
```
ESP32 Barco → L298N:
- GPIO 18 → IN1
- GPIO 17 → IN2  
- GPIO 16 → IN3
- GPIO 4  → IN4
- 5V → VCC
- GND → GND

L298N → Motores:
- OUT1, OUT2 → Motor Izquierdo
- OUT3, OUT4 → Motor Derecho  

L298N → Batería:
- +12V → Batería +
- GND → Batería -

🛡️ MODO FAILSAFE:
- ENA → 5V directo
- ENB → 5V directo
(Velocidad fija, funcionamiento garantizado)
```

### **2. Software - Subir códigos**

#### **ESP32 Control:**
1. Abrir `EspControl/EspControl.ino`
2. Subir al ESP32 de control
3. **Anotar la MAC** del monitor serie

#### **ESP32 Barco:**
1. Abrir `EspBarco/EspBarco.ino`
2. Subir al ESP32 del barco
3. **Anotar la MAC** del monitor serie

### **3. Configurar MACs**

#### **En EspControl.ino (línea ~15):**
```cpp
uint8_t macBarco[] = {0x98, 0xA3, 0x16, 0xE5, 0x9F, 0x90}; // ← CAMBIAR
```

#### **En EspBarco.ino (línea ~25):**
```cpp
uint8_t macControl[] = {0x24, 0x58, 0x7C, 0xCE, 0x3C, 0xCC}; // ← CAMBIAR
```

### **4. Resubir códigos actualizados**

### **5. ¡PROBAR!**

**Comandos básicos:**
- `w` = adelante
- `s` = atrás  
- `a` = izquierda
- `d` = derecha
- `p` = parar

---

## 🆘 **Solución Rápida de Problemas**

### **❌ No funciona nada:**
1. ✅ Verificar alimentación 12V en L298N
2. ✅ Conectar GND común ESP32-L298N-Batería
3. ✅ Probar ENA/ENB directo a 5V

### **❌ No hay comunicación:**
1. ✅ MACs correctamente configuradas
2. ✅ Ambos ESP32 encendidos
3. ✅ Distancia < 20m

### **❌ Motores no se mueven:**
1. ✅ Conectar ENA/ENB a 5V directo (Modo Failsafe)
2. ✅ Verificar cables IN1, IN2, IN3, IN4
3. ✅ Comando `vel 255` (velocidad máxima)

---

## 🎮 **Comandos Esenciales**

| Comando | Función |
|---------|---------|
| `w` | Adelante |
| `s` | Atrás |
| `a` | Izquierda |
| `d` | Derecha |
| `p` | Parar |
| `vel 255` | Velocidad máxima |
| `vel 100` | Velocidad baja |
| `help` | Mostrar ayuda |

---

**💡 Tip**: Si algo no funciona, usa siempre **Modo Failsafe** conectando ENA/ENB a 5V directo. ¡Funcionamiento garantizado!