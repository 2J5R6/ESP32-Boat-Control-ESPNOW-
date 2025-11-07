/*
 * ESP32-S3 Control de Barco 
 */

#include <WiFi.h>
#include <esp_now.h>

// === DEFINICIÓN DE PINES ===
// Motor A (Izquierdo)
#define MOTOR_A_IN1 18
#define MOTOR_A_IN2 17
#define MOTOR_A_ENA 2   // Si quieres pruebas, no lo conectes aún

// Motor B (Derecho)  
#define MOTOR_B_IN3 16
#define MOTOR_B_IN4 4
#define MOTOR_B_ENB 15  // Si quieres pruebas, no lo conectes aún

// === CONFIGURACIÓN LEDC PARA ESP32-S3 ===
#define PWM_FREQ 1000        // 1 KHz
#define PWM_RESOLUTION 8     // 8 bits (0-255)
#define VELOCIDAD_MOTOR 200  // Velocidad por defecto

// === DECLARACIONES DE FUNCIONES ===
void configurarMotores();
void moverAdelante();
void moverAtras();
void girarIzquierda();
void girarDerecha();
void pararMotores();

// Callback para recibir datos
void OnDataRecv(const esp_now_recv_info_t *recv_info, const uint8_t *incomingData, int len) {
  Serial.println();
  Serial.print("[ESP-NOW] Mensaje recibido: ");
  
  // Convertir datos a String
  String mensaje = "";
  for (int i = 0; i < len; i++) {
    mensaje += (char)incomingData[i];
  }
  Serial.println(mensaje);
  
  // Procesar comandos de motores
  if (mensaje == "ADELANTE") {
    Serial.println("-> Ejecutando ADELANTE");
    moverAdelante();
  } else if (mensaje == "ATRAS") {
    Serial.println("-> Ejecutando ATRAS");
    moverAtras();
  } else if (mensaje == "IZQUIERDA") {
    Serial.println("-> Ejecutando IZQUIERDA");
    girarIzquierda();
  } else if (mensaje == "DERECHA") {
    Serial.println("-> Ejecutando DERECHA");
    girarDerecha();
  } else if (mensaje == "PARAR") {
    Serial.println("-> Ejecutando PARAR");
    pararMotores();
  } else {
    Serial.println("-> Comando no reconocido para motores");
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("=== INICIANDO ESP32 BARCO ===");
  delay(100);
  Serial.println("Serial OK");
  delay(100);
  
  // Paso 1: WiFi básico (ya funcionó)
  Serial.println("Iniciando WiFi...");
  WiFi.mode(WIFI_STA);
  delay(500);
  Serial.println("WiFi iniciado OK");
  
  Serial.print("MAC Address: ");
  Serial.println(WiFi.macAddress());
  
  // Paso 2: Agregar ESP-NOW
  Serial.println("Iniciando ESP-NOW...");
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error iniciando ESP-NOW");
    return;
  }
  Serial.println("ESP-NOW iniciado OK");
  
  // Registrar callback
  esp_now_register_recv_cb(OnDataRecv);
  Serial.println("Callback registrado OK");
  
  // Paso 3: Configurar motores
  Serial.println("Configurando motores...");
  configurarMotores();
  Serial.println("Motores configurados OK");
  
  // === PRUEBA AUTOMÁTICA DE MOTORES ===
  Serial.println("\n=== INICIANDO PRUEBA DE MOTORES ===");
  
  Serial.println("Prueba 1: Motor A adelante...");
  digitalWrite(MOTOR_A_IN1, HIGH);
  digitalWrite(MOTOR_A_IN2, LOW);
  ledcWrite(MOTOR_A_ENA, 200);
  delay(2000);
  ledcWrite(MOTOR_A_ENA, 0);
  digitalWrite(MOTOR_A_IN1, LOW);
  Serial.println("Motor A parado");
  
  delay(1000);
  
  Serial.println("Prueba 2: Motor B adelante...");
  digitalWrite(MOTOR_B_IN3, HIGH);
  digitalWrite(MOTOR_B_IN4, LOW);
  ledcWrite(MOTOR_B_ENB, 200);
  delay(2000);
  ledcWrite(MOTOR_B_ENB, 0);
  digitalWrite(MOTOR_B_IN3, LOW);
  Serial.println("Motor B parado");
  
  delay(1000);
  
  Serial.println("Prueba 3: Ambos motores adelante...");
  moverAdelante();
  delay(2000);
  pararMotores();
  
  Serial.println("=== PRUEBA DE MOTORES COMPLETADA ===\n");
  
  Serial.println("Setup completado - Sistema completo funcionando");
  Serial.println("Esperando comandos de movimiento...");
}

void loop() {
  static unsigned long ultimoMensaje = 0;
  
  if (millis() - ultimoMensaje >= 2000) {
    Serial.print("Sistema activo - ");
    Serial.print(millis()/1000);
    Serial.println(" segundos");
    ultimoMensaje = millis();
  }
  
  delay(100);
}

// === FUNCIONES DE CONTROL DE MOTORES ===

void configurarMotores() {
  // Configurar pines digitales
  Serial.println("Configurando pines digitales...");
  pinMode(MOTOR_A_IN1, OUTPUT);
  pinMode(MOTOR_A_IN2, OUTPUT);
  pinMode(MOTOR_B_IN3, OUTPUT);
  pinMode(MOTOR_B_IN4, OUTPUT);
  
  digitalWrite(MOTOR_A_IN1, LOW);
  digitalWrite(MOTOR_A_IN2, LOW);
  digitalWrite(MOTOR_B_IN3, LOW);
  digitalWrite(MOTOR_B_IN4, LOW);
  
  // Configurar LEDC PWM para ESP32-S3
  Serial.println("Configurando LEDC PWM...");
  
  if (ledcAttach(MOTOR_A_ENA, PWM_FREQ, PWM_RESOLUTION)) {
    Serial.println("✓ PWM Motor A (ENA) configurado");
  } else {
    Serial.println("✗ ERROR PWM Motor A");
    return;
  }
  
  if (ledcAttach(MOTOR_B_ENB, PWM_FREQ, PWM_RESOLUTION)) {
    Serial.println("✓ PWM Motor B (ENB) configurado");
  } else {
    Serial.println("✗ ERROR PWM Motor B");
    return;
  }
  
  // Inicializar PWM en 0
  ledcWrite(MOTOR_A_ENA, 0);
  ledcWrite(MOTOR_B_ENB, 0);
  
  Serial.println("✓ Motores configurados con LEDC");
}

void moverAdelante() {
  Serial.println("MOTORES: Adelante");
  // Motor A (Izquierdo) - Adelante
  digitalWrite(MOTOR_A_IN1, HIGH);
  digitalWrite(MOTOR_A_IN2, LOW);
  ledcWrite(MOTOR_A_ENA, VELOCIDAD_MOTOR);  // USAR LEDC
  
  // Motor B (Derecho) - Adelante
  digitalWrite(MOTOR_B_IN3, HIGH);
  digitalWrite(MOTOR_B_IN4, LOW);
  ledcWrite(MOTOR_B_ENB, VELOCIDAD_MOTOR);  // USAR LEDC
}

void moverAtras() {
  Serial.println("MOTORES: Atrás");
  // Motor A (Izquierdo) - Atrás
  digitalWrite(MOTOR_A_IN1, LOW);
  digitalWrite(MOTOR_A_IN2, HIGH);
  ledcWrite(MOTOR_A_ENA, VELOCIDAD_MOTOR);  // USAR LEDC
  
  // Motor B (Derecho) - Atrás
  digitalWrite(MOTOR_B_IN3, LOW);
  digitalWrite(MOTOR_B_IN4, HIGH);
  ledcWrite(MOTOR_B_ENB, VELOCIDAD_MOTOR);  // USAR LEDC
}

void girarIzquierda() {
  Serial.println("MOTORES: Giro Izquierda");
  // Motor A (Izquierdo) - Atrás
  digitalWrite(MOTOR_A_IN1, LOW);
  digitalWrite(MOTOR_A_IN2, HIGH);
  ledcWrite(MOTOR_A_ENA, VELOCIDAD_MOTOR);  // USAR LEDC
  
  // Motor B (Derecho) - Adelante
  digitalWrite(MOTOR_B_IN3, HIGH);
  digitalWrite(MOTOR_B_IN4, LOW);
  ledcWrite(MOTOR_B_ENB, VELOCIDAD_MOTOR);  // USAR LEDC
}

void girarDerecha() {
  Serial.println("MOTORES: Giro Derecha");
  // Motor A (Izquierdo) - Adelante
  digitalWrite(MOTOR_A_IN1, HIGH);
  digitalWrite(MOTOR_A_IN2, LOW);
  ledcWrite(MOTOR_A_ENA, VELOCIDAD_MOTOR);  // USAR LEDC
  
  // Motor B (Derecho) - Atrás
  digitalWrite(MOTOR_B_IN3, LOW);
  digitalWrite(MOTOR_B_IN4, HIGH);
  ledcWrite(MOTOR_B_ENB, VELOCIDAD_MOTOR);  // USAR LEDC
}

void pararMotores() {
  Serial.println("MOTORES: Parado");
  // Apagar todos los pines de forma segura
  digitalWrite(MOTOR_A_IN1, LOW);
  digitalWrite(MOTOR_A_IN2, LOW);
  digitalWrite(MOTOR_B_IN3, LOW);
  digitalWrite(MOTOR_B_IN4, LOW);
  ledcWrite(MOTOR_A_ENA, 0);   // USAR LEDC para parar
  ledcWrite(MOTOR_B_ENB, 0);   // USAR LEDC para parar
}