# =============================================================================
# main.py — ESP32 MicroPython para Wokwi
# Sistema Control de Iluminación IoT
# =============================================================================

from machine import Pin, ADC  # type: ignore
import machine  # type: ignore
import utime  # type: ignore
import network  # type: ignore
import ubinascii  # type: ignore
from umqtt.simple import MQTTClient  # type: ignore

import settings

# =============================================================================
# CONFIGURACIÓN HARDWARE
# =============================================================================

ldr = ADC(Pin(settings.PIN_LDR))
ldr.atten(ADC.ATTN_11DB)  # Rango completo 0–3.3V → valores 0–4095

led = Pin(settings.PIN_LED, Pin.OUT)


# =============================================================================
# FUNCIÓN: Conectar a WiFi
# =============================================================================


def conectar_wifi():
    print("\n[WiFi] Iniciando conexión...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print(f"[WiFi] Conectando a: {settings.WIFI_SSID}")
        wlan.connect(settings.WIFI_SSID, settings.WIFI_PASSWORD)

        intentos = 0
        while not wlan.isconnected() and intentos < settings.INTENTOS_RECONEXION:
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
    print("\n[MQTT] Iniciando conexión...")
    try:
        client_id = ubinascii.hexlify(machine.unique_id())
        # keepalive=60: el broker espera un ping cada 60s antes de cortar la conexión
        client = MQTTClient(
            client_id, settings.MQTT_BROKER, settings.MQTT_PORT, keepalive=60
        )
        client.connect()
        print("[MQTT] ¡Conectado al broker!")
        print(f"[MQTT] Broker: {settings.MQTT_BROKER}")
        return client
    except Exception as e:
        print(f"[MQTT] Error de conexión: {e}")
        return None


# =============================================================================
# FUNCIÓN: Leer sensor LDR
# =============================================================================


def leer_luminosidad():
    """Lee el LDR. Devuelve 0–4095 (ADC 12 bits del ESP32)."""
    return ldr.read()


# =============================================================================
# FUNCIÓN: Controlar LED
# =============================================================================


def controlar_led(luminosidad):
    """
    Enciende el LED si luminosidad <= umbral (ambiente oscuro).
    Devuelve 'ENCENDIDO' o 'APAGADO'.
    """
    if luminosidad <= settings.UMBRAL_LUZ:
        led.value(1)
        return "ENCENDIDO"
    else:
        led.value(0)
        return "APAGADO"


# =============================================================================
# FUNCIÓN: Enviar datos por MQTT
# =============================================================================


def enviar_datos_mqtt(client, luminosidad, estado_led):
    if client:
        try:
            client.publish(settings.TOPIC_LUMINOSIDAD, str(luminosidad))
            client.publish(settings.TOPIC_LED_ESTADO, estado_led)
            return True
        except Exception as e:
            print(f"[MQTT] Error al enviar: {e}")
            return False
    return False


# =============================================================================
# FUNCIÓN: Reconectar MQTT
# =============================================================================


def reconectar_mqtt(client):
    """
    Intenta reconectar un cliente MQTT existente.
    Retorna True si logró reconectar, False si agotó los intentos.
    """
    for intento in range(1, settings.INTENTOS_RECONEXION + 1):
        try:
            print(
                f"[MQTT] Reconectando... intento {intento}/{settings.INTENTOS_RECONEXION}"
            )
            client.connect()
            print("[MQTT] ¡Reconectado!")
            return True
        except Exception as e:
            print(f"[MQTT] Intento {intento} fallido: {e}")
            utime.sleep(2)
    print("[MQTT] No se pudo reconectar tras varios intentos.")
    return False


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================


def main():
    print("\n" + "=" * 50)
    print(" Sistema Control de Iluminación IoT")
    print(" Evidencia de Aprendizaje N°3 — Wokwi")
    print("=" * 50 + "\n")

    if not conectar_wifi():
        print("\n[ERROR] No se pudo conectar a WiFi")
        return

    mqtt_client = conectar_mqtt()
    if not mqtt_client:
        print("\n[ADVERTENCIA] Continuando sin MQTT (solo local)")

    print("\n[SISTEMA] Iniciando bucle principal...")
    print(f"[SISTEMA] Umbral de luz: {settings.UMBRAL_LUZ} (escala 0–4095)")
    print("[SISTEMA] Mueve el slider del LDR en Wokwi para simular luz\n")

    try:
        while True:
            luminosidad = leer_luminosidad()
            estado_led = controlar_led(luminosidad)
            porcentaje = luminosidad * 100 // 4095

            print(
                f"[DATOS] Luz: {luminosidad:4d} ({porcentaje:3d}%) | LED: {estado_led}"
            )

            if mqtt_client:
                if enviar_datos_mqtt(mqtt_client, luminosidad, estado_led):
                    print("[MQTT]  Datos enviados")
                else:
                    # La conexión se cortó — intentar reconectar antes de continuar
                    print("[MQTT]  Conexión perdida. Intentando reconectar...")
                    reconectar_mqtt(mqtt_client)

            print("-" * 50)
            utime.sleep(settings.INTERVALO_LECTURA)

    except KeyboardInterrupt:
        print("\n[SISTEMA] Deteniendo...")
        led.value(0)
        if mqtt_client:
            mqtt_client.disconnect()
        print("[SISTEMA] Sistema detenido")


# =============================================================================
# EJECUTAR
# =============================================================================

main()
