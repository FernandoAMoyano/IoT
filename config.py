# =============================================================================
# Archivo de Configuración - Sistema Control de Iluminación IoT
# =============================================================================
# Este archivo carga las configuraciones desde el archivo .env
# Las credenciales sensibles NO deben estar en el código

import os
from pathlib import Path

# Cargar variables de entorno desde archivo .env
def load_env():
    """Carga variables de entorno desde archivo .env"""
    env_path = Path(__file__).parent / '.env'
    
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    else:
        print("⚠️ Archivo .env no encontrado. Usando valores por defecto.")

# Cargar variables
load_env()

# =============================================================================
# CONFIGURACIÓN WiFi
# =============================================================================
WIFI_SSID = os.getenv('WIFI_SSID', 'TU_RED_WIFI')
WIFI_PASSWORD = os.getenv('WIFI_PASSWORD', 'TU_CONTRASEÑA')

# =============================================================================
# CONFIGURACIÓN MQTT
# =============================================================================
MQTT_BROKER = os.getenv('MQTT_BROKER', 'broker.hivemq.com')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))

# Tópicos MQTT
TOPIC_LUMINOSIDAD = os.getenv('TOPIC_LUMINOSIDAD', 'Casa/Luminosidad')
TOPIC_LED_ESTADO = os.getenv('TOPIC_LED_ESTADO', 'Casa/LED_Estado')

# =============================================================================
# CONFIGURACIÓN MySQL
# =============================================================================
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'control_iluminacion')
}

# =============================================================================
# CONFIGURACIÓN HARDWARE (ESP32)
# =============================================================================
# Pines GPIO
PIN_LDR = int(os.getenv('PIN_LDR', '25'))
PIN_LED = int(os.getenv('PIN_LED', '2'))

# Umbrales
UMBRAL_LUZ = int(os.getenv('UMBRAL_LUZ', '750'))

# =============================================================================
# CONFIGURACIÓN GENERAL
# =============================================================================
INTERVALO_LECTURA = int(os.getenv('INTERVALO_LECTURA', '2'))
INTENTOS_RECONEXION = int(os.getenv('INTENTOS_RECONEXION', '5'))

# =============================================================================
# MOSTRAR CONFIGURACIÓN CARGADA (para debug)
# =============================================================================
if __name__ == "__main__":
    print("="*60)
    print("📋 CONFIGURACIÓN CARGADA")
    print("="*60)
    print(f"MySQL Host: {DB_CONFIG['host']}")
    print(f"MySQL User: {DB_CONFIG['user']}")
    print(f"MySQL Database: {DB_CONFIG['database']}")
    print(f"MySQL Password: {'*' * len(DB_CONFIG['password'])}")
    print(f"MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Umbral Luz: {UMBRAL_LUZ}")
    print("="*60)
