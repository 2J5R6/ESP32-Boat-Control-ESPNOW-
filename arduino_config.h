/*
 * Configuración para el sistema de control de barco
 * Archivo para configurar direcciones MAC de los ESP32
 */

#ifndef ARDUINO_CONFIG_H
#define ARDUINO_CONFIG_H

// ===============================================
// CONFIGURACIÓN DE DIRECCIONES MAC
// ===============================================

// INSTRUCCIONES:
// 1. Sube el código EspControl.ino al ESP32 de control
// 2. Abre el monitor serie y copia la MAC que aparece
// 3. Reemplaza MAC_CONTROL con esa dirección
// 4. Sube el código EspBarco.ino al ESP32 del barco  
// 5. Abre el monitor serie y copia la MAC que aparece
// 6. Reemplaza MAC_BARCO con esa dirección
// 7. Vuelve a subir ambos códigos con las MACs correctas

// MAC del ESP32 de control (Transmisor)
// Formato: {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF}
#define MAC_CONTROL {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}

// MAC del ESP32 del barco (Receptor)
// Formato: {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF}
#define MAC_BARCO {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}

// ===============================================
// CONFIGURACIÓN DE PINES (YA DEFINIDA EN CÓDIGOS)
// ===============================================

// Pines para ESP32 del barco (L298N) - ESP32-S3 Compatible
#define MOTOR_A_IN1_PIN 18    // Motor izquierdo dirección 1
#define MOTOR_A_IN2_PIN 17    // Motor izquierdo dirección 2 (cambiado de 19)
#define MOTOR_A_ENA_PIN 5     // Motor izquierdo velocidad PWM

#define MOTOR_B_IN3_PIN 16    // Motor derecho dirección 1 (cambiado de 20)
#define MOTOR_B_IN4_PIN 4     // Motor derecho dirección 2 (cambiado de 21)
#define MOTOR_B_ENB_PIN 6     // Motor derecho velocidad PWM

// ===============================================
// CONFIGURACIÓN DE VELOCIDADES
// ===============================================

#define VELOCIDAD_MINIMA 50      // Velocidad mínima para que se muevan los motores
#define VELOCIDAD_MAXIMA 255     // Velocidad máxima (100% PWM)
#define VELOCIDAD_DEFAULT 200    // Velocidad por defecto

#endif // ARDUINO_CONFIG_H