# =============================================================================
# Simulador ESP32 - Sistema Control de Iluminación IoT
# =============================================================================
# Este simulador genera datos aleatorios que imitan el comportamiento del ESP32
# Útil para probar el sistema sin necesidad de hardware físico

# =============================================================================
# IMPORTAR LIBRERÍAS
# =============================================================================

import paho.mqtt.client as mqtt
import time
import random
import config


# =============================================================================
# FUNCIÓN: Generar lectura de sensor
# =============================================================================
def generar_lectura_sensor():
    """
    Simula una lectura del sensor LDR
    Retorna un valor aleatorio entre 200 y 1000
    """
    # Generar valor aleatorio
    luminosidad = random.randint(200, 1000)

    # Determinar estado del LED según umbral
    if luminosidad <= config.UMBRAL_LUZ:
        estado_led = "ENCENDIDO"
        emoji = "💡"
        descripcion = "Luz BAJA"
    else:
        estado_led = "APAGADO"
        emoji = "🌞"
        descripcion = "Luz ALTA"

    return luminosidad, estado_led, emoji, descripcion


# =============================================================================
# FUNCIÓN: Mostrar datos
# =============================================================================
def mostrar_datos(contador, luminosidad, estado_led, emoji, descripcion):
    """
    Muestra los datos generados en la consola
    """
    print(f"\n[Lectura #{contador}] {emoji} {descripcion}")
    print(f"  Luminosidad: {luminosidad}")
    print(f"  Estado LED: {estado_led}")
    print("-" * 50)


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def main():
    """
    Función principal del simulador
    """
    print("\n" + "=" * 60)
    print(" Simulador ESP32 - Control de Iluminación IoT")
    print(" Evidencia de Aprendizaje N°3")
    print("=" * 60)

    print(f"\n[CONFIG] Umbral de luz: {config.UMBRAL_LUZ}")
    print(f"[CONFIG] Si luminosidad <= {config.UMBRAL_LUZ}: LED ENCENDIDO")
    print(f"[CONFIG] Si luminosidad > {config.UMBRAL_LUZ}: LED APAGADO")

    # Configurar cliente MQTT
    print(f"\n[MQTT] Conectando a {config.MQTT_BROKER}...")

    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Simulador_ESP32_IoT")
        client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)

        print("[MQTT] ¡Conectado!")
        print("\n[SIMULADOR] Iniciando generación de datos...")
        print(f"[SIMULADOR] Enviando datos cada {config.INTERVALO_LECTURA} segundos")
        print("[SIMULADOR] Presiona Ctrl+C para detener\n")

        # Bucle principal de simulación
        contador = 0
        try:
            while True:
                contador += 1

                # Generar datos simulados
                luminosidad, estado_led, emoji, descripcion = generar_lectura_sensor()

                # Mostrar en consola
                mostrar_datos(contador, luminosidad, estado_led, emoji, descripcion)

                # Publicar en MQTT (igual que el ESP32)
                try:
                    client.publish(config.TOPIC_LUMINOSIDAD, str(luminosidad))
                    client.publish(config.TOPIC_LED_ESTADO, estado_led)
                    print("[MQTT] Datos enviados correctamente")
                except Exception as e:
                    print(f"[MQTT] Error al enviar: {e}")

                # Esperar antes de siguiente lectura
                time.sleep(config.INTERVALO_LECTURA)

        except KeyboardInterrupt:
            print("\n\n[SIMULADOR] Deteniendo simulación...")
            client.disconnect()
            print("[SIMULADOR] Simulador detenido correctamente")

    except Exception as e:
        print(f"\n[ERROR] No se pudo conectar al broker MQTT: {e}")
        print("[ERROR] Verifica tu conexión a internet")


# =============================================================================
# EJECUTAR PROGRAMA
# =============================================================================
if __name__ == "__main__":
    main()
