# =============================================================================
# settings.py — Configuración del Servidor Python
# Sistema Control de Iluminación IoT
# =============================================================================
# Usado EXCLUSIVAMENTE por servidor.py
# Carga las variables desde ../.env — las credenciales nunca están hardcodeadas
#
# Variables del ESP32 (WiFi, pines, intervalos) están en wokwi/settings.py
# =============================================================================

import os
from pathlib import Path


def load_env():
    """Carga variables de entorno desde archivo .env en la raíz del proyecto"""
    env_path = Path(__file__).parent.parent / ".env"  # sube un nivel: servidor/ → raíz

    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value
    else:
        print("⚠️ Archivo .env no encontrado en la raíz del proyecto.")


load_env()

# =============================================================================
# CONFIGURACIÓN MySQL
# =============================================================================

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "control_iluminacion"),
}

# =============================================================================
# CONFIGURACIÓN MQTT
# =============================================================================

MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

TOPIC_LUMINOSIDAD = os.getenv("TOPIC_LUMINOSIDAD", "Casa/Luminosidad")
TOPIC_LED_ESTADO = os.getenv("TOPIC_LED_ESTADO", "Casa/LED_Estado")

# =============================================================================
# LÓGICA
# =============================================================================

# Umbral para clasificar LUZ_BAJA / LUZ_ALTA
# Escala 12 bits (0–4095) — consistente con el ADC del ESP32
UMBRAL_LUZ = int(os.getenv("UMBRAL_LUZ", "1500"))

# =============================================================================
# DEBUG — ejecutar este archivo directamente para verificar la configuración
# python servidor/settings.py
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("📋 CONFIGURACIÓN DEL SERVIDOR")
    print("=" * 60)
    print(f"MySQL Host:      {DB_CONFIG['host']}")
    print(f"MySQL User:      {DB_CONFIG['user']}")
    print(f"MySQL Database:  {DB_CONFIG['database']}")
    print(f"MySQL Password:  {'*' * len(DB_CONFIG['password'])}")
    print(f"MQTT Broker:     {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Topic LDR:       {TOPIC_LUMINOSIDAD}")
    print(f"Topic LED:       {TOPIC_LED_ESTADO}")
    print(f"Umbral Luz:      {UMBRAL_LUZ} (escala 0–4095)")
    print("=" * 60)
