# =============================================================================
# Código ESP32 - Sistema Control de Iluminación IoT
# =============================================================================

# Este código se ejecuta en el ESP32 con MicroPython
# Lee el sensor LDR, controla el LED y envía datos por MQTT

# =============================================================================
# IMPORTAR LIBRERÍAS
# =============================================================================


from machine import Pin, ADC  # type: ignore
import utime  # type: ignore
import network  # type: ignore
import ubinascii  # type: ignore
from umqtt.simple import MQTTClient  # type: ignore

# Importar configuración
import config

# =============================================================================
# CONFIGURACIÓN HARDWARE
# =============================================================================


# Configurar sensor LDR (Analógico)
ldr = ADC(Pin(config.PIN_LDR))
ldr.width(ADC.WIDTH_10BIT)  # Resolución 10 bits (0-1023)
ldr.atten(ADC.ATTN_11DB)  # Rango completo de voltaje

# Configurar LED (Digital)
led = Pin(config.PIN_LED, Pin.OUT)


# =============================================================================
# FUNCIÓN: Conectar a WiFi
# =============================================================================


def conectar_wifi():
    """
    Conecta el ESP32 a la red WiFi configurada
    Reintenta hasta conseguir conexión
    """
    print("\n[WiFi] Iniciando conexión...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print(f"[WiFi] Conectando a: {config.WIFI_SSID}")
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

        # Esperar conexión
        intentos = 0
        while not wlan.isconnected() and intentos < config.INTENTOS_RECONEXION:
            print(".", end="")
            utime.sleep(1)
            intentos += 1

        if wlan.isconnected():
            print("\n[WiFi] ¡Conectado!")
            print(f"[WiFi] IP: {wlan.ifconfig()[0]}")
            return True
        else:
            print("\n[WiFi] Error: No se pudo conectar")
            return False
    else:
        print("[WiFi] Ya estaba conectado")
        return True


# =============================================================================
# FUNCIÓN: Conectar a MQTT
# =============================================================================


def conectar_mqtt():
    """
    Conecta al broker MQTT
    Retorna el cliente MQTT o None si falla
    """
    print("\n[MQTT] Iniciando conexión...")
    try:
        # Generar ID único para el cliente
        client_id = ubinascii.hexlify(machine.unique_id())  # type: ignore  # noqa: F821

        # Crear cliente MQTT
        client = MQTTClient(client_id, config.MQTT_BROKER, config.MQTT_PORT)

        # Conectar
        client.connect()
        print("[MQTT] ¡Conectado al broker!")
        print(f"[MQTT] Broker: {config.MQTT_BROKER}")
        return client

    except Exception as e:
        print(f"[MQTT] Error de conexión: {e}")
        return None


# =============================================================================
# FUNCIÓN: Leer sensor LDR
# =============================================================================


def leer_luminosidad():
    """
    Lee el valor del sensor LDR
    Retorna un valor entre 0 y 1023
    """
    valor = ldr.read()
    return valor


# =============================================================================
# FUNCIÓN: Controlar LED
# =============================================================================


def controlar_led(luminosidad):
    """
    Controla el LED según el nivel de luminosidad
    Si luz < umbral: enciende LED
    Si luz >= umbral: apaga LED
    Retorna el estado del LED ("ENCENDIDO" o "APAGADO")
    """
    if luminosidad <= config.UMBRAL_LUZ:
        led.value(1)  # Encender LED
        return "ENCENDIDO"
    else:
        led.value(0)  # Apagar LED
        return "APAGADO"


# =============================================================================
# FUNCIÓN: Enviar datos por MQTT
# =============================================================================


def enviar_datos_mqtt(client, luminosidad, estado_led):
    """
    Envía datos al broker MQTT
    """
    if client:
        try:
            # Enviar luminosidad
            client.publish(config.TOPIC_LUMINOSIDAD, str(luminosidad))

            # Enviar estado del LED
            client.publish(config.TOPIC_LED_ESTADO, estado_led)

            return True

        except Exception as e:
            print(f"[MQTT] Error al enviar: {e}")
            return False
    return False


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================


def main():
    """
    Función principal del programa
    """
    print("\n" + "=" * 50)
    print(" Sistema Control de Iluminación IoT")
    print(" Evidencia de Aprendizaje N°3")
    print("=" * 50 + "\n")

    # Conectar a WiFi
    if not conectar_wifi():
        print("\n[ERROR] No se pudo conectar a WiFi")
        print("Verifica las credenciales en config.py")
        return

    # Conectar a MQTT
    mqtt_client = conectar_mqtt()
    if not mqtt_client:
        print("\n[ADVERTENCIA] Continuando sin MQTT")
        print("El sistema funcionará localmente")

    print("\n[SISTEMA] Iniciando bucle principal...")
    print("[SISTEMA] Presiona Ctrl+C para detener\n")

    # Bucle principal
    try:
        while True:
            # Leer sensor
            luminosidad = leer_luminosidad()

            # Controlar LED
            estado_led = controlar_led(luminosidad)

            # Mostrar información
            print(f"[DATOS] Luz: {luminosidad} | LED: {estado_led}")

            # Enviar por MQTT
            if mqtt_client:
                if enviar_datos_mqtt(mqtt_client, luminosidad, estado_led):
                    print("[MQTT] Datos enviados correctamente")
                else:
                    print("[MQTT] Error al enviar datos")

            print("-" * 50)

            # Esperar antes de siguiente lectura
            utime.sleep(config.INTERVALO_LECTURA)

    except KeyboardInterrupt:
        print("\n\n[SISTEMA] Deteniendo sistema...")
        led.value(0)  # Apagar LED
        if mqtt_client:
            mqtt_client.disconnect()
        print("[SISTEMA] Sistema detenido correctamente")


# =============================================================================
# EJECUTAR PROGRAMA
# =============================================================================

if __name__ == "__main__":
    main()
