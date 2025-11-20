/*
 * ESP32-S3 Control de Barco - Transmisor/Control
 * Protocolo: ESP-NOW
 * Envía comandos al ESP32 del barco
 * Control mediante consola serial
 */

#include <esp_now.h>
#include <WiFi.h>

// === DIRECCIÓN MAC DEL ESP32 BARCO ===
// MAC: 98:A3:16:E5:9F:90
uint8_t direccionMAC_Barco[] = {0x98, 0xA3, 0x16, 0xE5, 0x9F, 0x90};

// === ESTRUCTURA DE DATOS ===
typedef struct struct_message {
  char comando[32];          // "ADELANTE", "ATRAS", "IZQUIERDA", "DERECHA", "PARAR"
  int tiempo_ms;             // Tiempo de ejecución en milisegundos (0 = continuo)
  unsigned long timestamp;   // Marca de tiempo para debugging
} struct_message;

struct_message datosEnviar;
struct_message estadoBarco;

// === VARIABLES DE CONTROL ===
unsigned long ultimoComando = 0;
unsigned long ultimoEstado = 0;
bool esperandoRespuesta = false;

// Callback cuando se envían datos (versión nueva del ESP32 core)
void OnDataSent(const wifi_tx_info_t *mac_addr, esp_now_send_status_t status) {
  if (status == ESP_NOW_SEND_SUCCESS) {
    Serial.println("[TX] Comando enviado OK");
  } else {
    Serial.println("[TX] Error al enviar comando");
  }
}

// Callback cuando se reciben datos (versión nueva del ESP32 core)
void OnDataRecv(const esp_now_recv_info_t *recv_info, const uint8_t *incomingData, int len) {
  memcpy(&estadoBarco, incomingData, sizeof(estadoBarco));
  ultimoEstado = millis();
  esperandoRespuesta = false;
  
  Serial.println();
  Serial.println("[RX] ===== ESTADO DEL BARCO =====");
  Serial.print("     Estado: ");
  Serial.println(estadoBarco.comando);
  if (estadoBarco.tiempo_ms > 0) {
    Serial.print("     Tiempo restante: ");
    Serial.print(estadoBarco.tiempo_ms);
    Serial.println(" ms");
  }
  Serial.print("     Timestamp: ");
  Serial.println(estadoBarco.timestamp);
  Serial.println("     ==============================");
  Serial.println();
  Serial.print("Comando> ");
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Test básico de serial
  Serial.println("=== INICIANDO ESP32 CONTROL ===");
  delay(500);
  Serial.println("Serial OK");
  delay(500);
  
  // Configurar WiFi básico
  Serial.println("Configurando WiFi...");
  WiFi.mode(WIFI_STA);
  delay(500);
  
  Serial.print("MAC Address: ");
  Serial.println(WiFi.macAddress());
  
  // Ahora SÍ vamos a probar ESP-NOW
  Serial.println("Inicializando ESP-NOW...");
  if (esp_now_init() != ESP_OK) {
    Serial.println("[ERROR] Error al inicializar ESP-NOW");
    return;
  }
  Serial.println("ESP-NOW OK");
  
  // Configurar peer con la MAC del barco
  // MAC del barco: 98:A3:16:E5:9F:90
  uint8_t macBarco[] = {0x98, 0xA3, 0x16, 0xE5, 0x9F, 0x90};
  
  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, macBarco, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  peerInfo.ifidx = WIFI_IF_STA;
  
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("[ERROR] Error al agregar peer");
  } else {
    Serial.println("Peer agregado OK");
  }
  
  Serial.println("=== SISTEMA INICIADO ===");
  Serial.println("Comandos: test, espnow, mac");
}

void loop() {
  // Verificar entrada por Serial
  if (Serial.available()) {
    String entrada = Serial.readStringUntil('\n');
    entrada.trim();
    
    Serial.print("Recibido: ");
    Serial.println(entrada);
    
    if (entrada == "test") {
      Serial.println("Test OK - Serial funcionando!");
    } else if (entrada == "mac") {
      Serial.print("Mi MAC: ");
      Serial.println(WiFi.macAddress());
    } else if (entrada == "espnow") {
      Serial.println("Enviando mensaje de prueba...");
      enviarMensajePrueba();
    } else if (entrada == "w" || entrada == "adelante") {
      Serial.println("Enviando comando ADELANTE...");
      enviarComandoSimple("ADELANTE");
    } else if (entrada == "s" || entrada == "atras") {
      Serial.println("Enviando comando ATRAS...");
      enviarComandoSimple("ATRAS"); 
    } else if (entrada == "a" || entrada == "izquierda") {
      Serial.println("Enviando comando IZQUIERDA...");
      enviarComandoSimple("IZQUIERDA");
    } else if (entrada == "d" || entrada == "derecha") {
      Serial.println("Enviando comando DERECHA...");
      enviarComandoSimple("DERECHA");
    } else if (entrada == "p" || entrada == "parar") {
      Serial.println("Enviando comando PARAR...");
      enviarComandoSimple("PARAR");
    } else {
      Serial.println("Comandos: test, mac, espnow, w, s, a, d, p");
    }
  }
  
  delay(100);
}

// Función para enviar mensaje de prueba
void enviarMensajePrueba() {
  // Mensaje simple de prueba
  String mensaje = "HOLA BARCO";
  uint8_t macBarco[] = {0x98, 0xA3, 0x16, 0xE5, 0x9F, 0x90}; // MAC real del barco
  
  esp_err_t result = esp_now_send(macBarco, (uint8_t*)mensaje.c_str(), mensaje.length());
  
  if (result == ESP_OK) {
    Serial.println("Mensaje enviado OK");
  } else {
    Serial.println("Error enviando mensaje");
  }
}

// Función simplificada para enviar comandos (sin velocidad)
void enviarComandoSimple(String comando) {
  uint8_t macBarco[] = {0x98, 0xA3, 0x16, 0xE5, 0x9F, 0x90}; // MAC real del barco
  
  esp_err_t result = esp_now_send(macBarco, (uint8_t*)comando.c_str(), comando.length());
  
  if (result == ESP_OK) {
    Serial.println("Comando enviado OK");
  } else {
    Serial.println("Error enviando comando");
  }
}

// === PROCESAMIENTO DE COMANDOS ===
void procesarComando(String cmd) {
  cmd.toUpperCase();
  Serial.println();
  Serial.print("[CMD] Procesando: ");
  Serial.println(cmd);
  
  // Comandos de ayuda
  if (cmd == "HELP" || cmd == "AYUDA" || cmd == "?" || cmd == "H") {
    mostrarAyuda();
    return;
  }
  
  // Comando para obtener estado
  if (cmd == "ESTADO" || cmd == "STATUS" || cmd == "S") {
    mostrarEstadoBarco();
    return;
  }
  
  // Comando para obtener MAC del barco
  if (cmd == "MAC") {
    mostrarMACBarco();
    return;
  }
  
  // Comandos de movimiento básicos
  if (cmd == "W" || cmd == "ADELANTE") {
    enviarComando("ADELANTE", 0);
  }
  else if (cmd == "S" || cmd == "ATRAS") {
    enviarComando("ATRAS", 0);
  }
  else if (cmd == "A" || cmd == "IZQUIERDA") {
    enviarComando("IZQUIERDA", 0);
  }
  else if (cmd == "D" || cmd == "DERECHA") {
    enviarComando("DERECHA", 0);
  }
  else if (cmd == "PARAR" || cmd == "STOP" || cmd == "P") {
    enviarComando("PARAR", 0);
  }
  
  // Comandos con tiempo (formato: "ADELANTE 2000" = adelante por 2 segundos)
  else if (cmd.indexOf(' ') > 0) {
    int espacioIndex = cmd.indexOf(' ');
    String movimiento = cmd.substring(0, espacioIndex);
    String tiempoStr = cmd.substring(espacioIndex + 1);
    int tiempo = tiempoStr.toInt();
    
    if (tiempo > 0) {
      if (movimiento == "ADELANTE" || movimiento == "W") {
        enviarComando("ADELANTE", tiempo);
      }
      else if (movimiento == "ATRAS" || movimiento == "S") {
        enviarComando("ATRAS", tiempo);
      }
      else if (movimiento == "IZQUIERDA" || movimiento == "A") {
        enviarComando("IZQUIERDA", tiempo);
      }
      else if (movimiento == "DERECHA" || movimiento == "D") {
        enviarComando("DERECHA", tiempo);
      }
      else {
        Serial.println("[ERROR] Comando no reconocido");
        mostrarAyuda();
      }
    } else {
      Serial.println("[ERROR] Tiempo debe ser mayor a 0");
    }
  }
  else {
    Serial.println("[ERROR] Comando no reconocido");
    mostrarAyuda();
  }
}

// === ENVÍO DE COMANDOS ===
void enviarComando(String cmd, int tiempo) {
  strcpy(datosEnviar.comando, cmd.c_str());
  datosEnviar.tiempo_ms = tiempo;
  datosEnviar.timestamp = millis();
  
  esp_err_t result = esp_now_send(direccionMAC_Barco, (uint8_t *) &datosEnviar, sizeof(datosEnviar));
  
  Serial.println("=== ENVIANDO COMANDO ===");
  Serial.print("Comando: ");
  Serial.println(cmd);
  Serial.print("Tiempo: ");
  if (tiempo > 0) {
    Serial.print(tiempo);
    Serial.println(" ms");
  } else {
    Serial.println("Continuo");
  }
  
  if (result == ESP_OK) {
    Serial.println("[TX] Comando enviado OK");
    esperandoRespuesta = true;
    ultimoComando = millis();
  } else {
    Serial.println("[TX] Error al enviar comando");
  }
  Serial.println("========================");
}

// === FUNCIONES DE AYUDA ===
void mostrarAyuda() {
  Serial.println();
  Serial.println("================== COMANDOS DISPONIBLES ==================");
  Serial.println("MOVIMIENTO:");
  Serial.println("  w / adelante    - Mover adelante");
  Serial.println("  s / atras       - Mover atrás");
  Serial.println("  a / izquierda   - Girar izquierda");
  Serial.println("  d / derecha     - Girar derecha");
  Serial.println("  parar / p       - Parar motores");
  Serial.println();
  Serial.println("MOVIMIENTO CON TIEMPO:");
  Serial.println("  adelante 2000   - Adelante por 2 segundos");
  Serial.println("  derecha 1500    - Girar derecha por 1.5 segundos");
  Serial.println();
  Serial.println("CONFIGURACIÓN:");
  Serial.println("  estado          - Mostrar estado actual del barco");
  Serial.println("  mac             - Mostrar MAC configurada del barco");
  Serial.println();
  Serial.println("AYUDA:");
  Serial.println("  help / ayuda / h / ? - Mostrar esta ayuda");
  Serial.println("========================================================");
  Serial.println();
  Serial.println("NOTA: Control a velocidad fija (ENA/ENB no conectados)");
  Serial.print("Comando> ");
}

void mostrarEstadoBarco() {
  if (ultimoEstado == 0) {
    Serial.println("[INFO] No se ha recibido estado del barco aún");
    return;
  }
  
  unsigned long tiempoSinEstado = millis() - ultimoEstado;
  Serial.println();
  Serial.println("======= ESTADO ACTUAL DEL BARCO =======");
  Serial.print("Estado: ");
  Serial.println(estadoBarco.comando);
  Serial.print("Tiempo sin comunicación: ");
  Serial.print(tiempoSinEstado / 1000.0);
  Serial.println(" segundos");
  
  if (tiempoSinEstado > 10000) {
    Serial.println("[ADVERTENCIA] Sin comunicación por más de 10 segundos");
  }
  
  Serial.println("======================================");
  Serial.println();
}

void mostrarMACBarco() {
  Serial.println();
  Serial.print("[INFO] MAC del barco configurada: ");
  for(int i=0; i<6; i++) {
    Serial.printf("%02X", direccionMAC_Barco[i]);
    if(i<5) Serial.print(":");
  }
  Serial.println();
  Serial.println("[NOTA] Si no hay comunicación, verifica que esta MAC");
  Serial.println("       coincida con la MAC real del ESP32 del barco");
  Serial.println();
}
