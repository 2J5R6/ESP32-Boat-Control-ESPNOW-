/*
 * ESP32-S3 Control de Barco - Modo Sin PWM
 * ENA y ENB conectados directamente a 5V
 * Control solo por dirección (IN1, IN2, IN3, IN4)
 */

#include <WiFi.h>
#include <esp_now.h>

// === DEFINICIÓN DE PINES ===
// Motor A (Izquierdo)
#define MOTOR_A_IN1 18
#define MOTOR_A_IN2 17
// MOTOR_A_ENA conectado directo a 5V

// Motor B (Derecho)  
#define MOTOR_B_IN3 16
#define MOTOR_B_IN4 4
// MOTOR_B_ENB conectado directo a 5V

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
  
  Serial.println("\nSetup completado - Sistema funcionando");
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
  // Configurar solo pines de dirección
  Serial.println("Configurando pines de dirección...");
  pinMode(MOTOR_A_IN1, OUTPUT);
  pinMode(MOTOR_A_IN2, OUTPUT);
  pinMode(MOTOR_B_IN3, OUTPUT);
  pinMode(MOTOR_B_IN4, OUTPUT);
  
  // Inicializar en LOW (motores parados)
  digitalWrite(MOTOR_A_IN1, LOW);
  digitalWrite(MOTOR_A_IN2, LOW);
  digitalWrite(MOTOR_B_IN3, LOW);
  digitalWrite(MOTOR_B_IN4, LOW);
  
  Serial.println("✓ Motores configurados (ENA/ENB en 5V externo)");
}

void moverAdelante() {
  Serial.println("MOTORES: Adelante");
  // Motor A (Izquierdo) - Adelante
  digitalWrite(MOTOR_A_IN1, HIGH);
  digitalWrite(MOTOR_A_IN2, LOW);
  
  // Motor B (Derecho) - Adelante
  digitalWrite(MOTOR_B_IN3, HIGH);
  digitalWrite(MOTOR_B_IN4, LOW);
}

void moverAtras() {
  Serial.println("MOTORES: Atrás");
  // Motor A (Izquierdo) - Atrás
  digitalWrite(MOTOR_A_IN1, LOW);
  digitalWrite(MOTOR_A_IN2, HIGH);
  
  // Motor B (Derecho) - Atrás
  digitalWrite(MOTOR_B_IN3, LOW);
  digitalWrite(MOTOR_B_IN4, HIGH);
}

void girarIzquierda() {
  Serial.println("MOTORES: Giro Izquierda");
  // Motor A (Izquierdo) - Adelante
  digitalWrite(MOTOR_A_IN1, HIGH);
  digitalWrite(MOTOR_A_IN2, LOW);
  
  // Motor B (Derecho) - Atrás
  digitalWrite(MOTOR_B_IN3, LOW);
  digitalWrite(MOTOR_B_IN4, HIGH);
}

void girarDerecha() {
  Serial.println("MOTORES: Giro Derecha");
  // Motor A (Izquierdo) - Atrás
  digitalWrite(MOTOR_A_IN1, LOW);
  digitalWrite(MOTOR_A_IN2, HIGH);
  
  // Motor B (Derecho) - Adelante
  digitalWrite(MOTOR_B_IN3, HIGH);
  digitalWrite(MOTOR_B_IN4, LOW);
}

void pararMotores() {
  Serial.println("MOTORES: Parado");
  // Apagar todos los pines de dirección
  digitalWrite(MOTOR_A_IN1, LOW);
  digitalWrite(MOTOR_A_IN2, LOW);
  digitalWrite(MOTOR_B_IN3, LOW);
  digitalWrite(MOTOR_B_IN4, LOW);
}