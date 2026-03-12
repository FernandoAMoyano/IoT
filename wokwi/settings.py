# =============================================================================
# settings.py — Configuración del ESP32 para Wokwi
# Sistema Control de Iluminación IoT
# =============================================================================


# ── WiFi ──────────────────────────────────────────────────────────────────────
# "Wokwi-GUEST" es la red WiFi simulada gratuita de Wokwi — sin contraseña
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# ── MQTT ──────────────────────────────────────────────────────────────────────
# Mismo broker y tópicos que el servidor — es el contrato de comunicación
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

TOPIC_LUMINOSIDAD = "Casa/Luminosidad"
TOPIC_LED_ESTADO = "Casa/LED_Estado"

# ── Hardware ──────────────────────────────────────────────────────────────────
# GPIO34 = ADC1 → compatible con WiFi activo
# GPIO25 = ADC2 → se deshabilita cuando WiFi está activo (no usar)
PIN_LDR = 34
PIN_LED = 2

# ── Lógica ────────────────────────────────────────────────────────────────────
# Escala 12 bits (0–4095) — valor por defecto del ADC del ESP32
UMBRAL_LUZ = 3000
INTERVALO_LECTURA = 2  # segundos entre lecturas
INTENTOS_RECONEXION = 5
