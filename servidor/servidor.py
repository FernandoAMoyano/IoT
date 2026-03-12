# =============================================================================
# servidor.py — Servidor MQTT → MySQL
# Sistema Control de Iluminación IoT
# =============================================================================
# Recibe datos del ESP32 por MQTT y los almacena en MySQL.
# Ejecutar desde la raíz del proyecto:
#   python servidor/servidor.py
# =============================================================================

import mysql.connector
import paho.mqtt.client as mqtt
import settings
from datetime import datetime

# =============================================================================
# VARIABLES GLOBALES
# =============================================================================

db_connection = None
datos_temp = {"luminosidad": None, "estado_led": None}


# =============================================================================
# FUNCIÓN: Conectar a MySQL
# =============================================================================


def conectar_mysql():
    """
    Conecta a la base de datos MySQL.
    Retorna la conexión o None si falla.
    """
    print("\n[MySQL] Intentando conexión...")
    try:
        connection = mysql.connector.connect(**settings.DB_CONFIG)
        print("[MySQL] ¡Conectado exitosamente!")
        print(f"[MySQL] Base de datos: {settings.DB_CONFIG['database']}")
        return connection
    except mysql.connector.Error as e:
        print(f"[MySQL] Error de conexión: {e}")
        print("[MySQL] Verifica:")
        print("  - MySQL está ejecutándose")
        print("  - Credenciales en .env son correctas")
        print("  - La base de datos existe (ejecutar servidor/base_datos.sql)")
        return None


# =============================================================================
# FUNCIÓN: Guardar datos en MySQL
# =============================================================================


def guardar_datos(luminosidad, estado_led):
    """
    Inserta una lectura en la tabla datos_luminosidad.
    Clasifica automáticamente como LUZ_BAJA o LUZ_ALTA según el umbral.
    """
    global db_connection

    if not db_connection:
        print("[MySQL] No hay conexión a la base de datos")
        return False

    try:
        cursor = db_connection.cursor()

        clasificacion = "LUZ_BAJA" if luminosidad <= settings.UMBRAL_LUZ else "LUZ_ALTA"

        sql = """
        INSERT INTO datos_luminosidad 
        (nivel_luz, estado_led, clasificacion) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (luminosidad, estado_led, clasificacion))
        db_connection.commit()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[GUARDADO] {timestamp}")
        print(f"  Luminosidad:   {luminosidad}")
        print(f"  LED:           {estado_led}")
        print(f"  Clasificación: {clasificacion}")
        print("-" * 50)

        cursor.close()
        return True

    except mysql.connector.Error as e:
        print(f"[MySQL] Error al guardar: {e}")
        return False


# =============================================================================
# CALLBACK: Conexión al broker MQTT
# =============================================================================


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\n[MQTT] ¡Conectado al broker!")
        print(f"[MQTT] Broker: {settings.MQTT_BROKER}")
        print("[MQTT] Suscribiéndose a tópicos...")

        client.subscribe(settings.TOPIC_LUMINOSIDAD)
        client.subscribe(settings.TOPIC_LED_ESTADO)

        print(f"  - {settings.TOPIC_LUMINOSIDAD}")
        print(f"  - {settings.TOPIC_LED_ESTADO}")
        print("\n[SISTEMA] Esperando datos del ESP32...")
        print("-" * 50)
    else:
        print(f"[MQTT] Error de conexión. Código: {rc}")


# =============================================================================
# CALLBACK: Mensaje MQTT recibido
# =============================================================================


def on_message(client, userdata, msg):
    global datos_temp

    topic = msg.topic
    mensaje = msg.payload.decode()

    print(f"\n[RECIBIDO] {topic} = {mensaje}")

    if topic == settings.TOPIC_LUMINOSIDAD:
        try:
            datos_temp["luminosidad"] = int(mensaje)
        except ValueError:
            print(f"[ERROR] Valor de luminosidad inválido: {mensaje}")
            return

    elif topic == settings.TOPIC_LED_ESTADO:
        datos_temp["estado_led"] = mensaje

    # Guardar solo cuando llegaron ambos datos
    if datos_temp["luminosidad"] is not None and datos_temp["estado_led"] is not None:
        guardar_datos(datos_temp["luminosidad"], datos_temp["estado_led"])
        datos_temp["luminosidad"] = None
        datos_temp["estado_led"] = None


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================


def main():
    global db_connection

    print("\n" + "=" * 60)
    print(" Servidor MQTT → MySQL — Control de Iluminación IoT")
    print(" Evidencia de Aprendizaje N°3")
    print("=" * 60)

    """ Conexión a MySQL:"""
    db_connection = conectar_mysql()
    if not db_connection:
        print("\n[ERROR] No se pudo conectar a MySQL. Abortando.")
        return

    """ Creación de cliente MQTT """
    print("\n[MQTT] Configurando cliente...")
    client = mqtt.Client("Servidor_Iluminacion_IoT")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        print(f"[MQTT] Conectando a {settings.MQTT_BROKER}...")
        client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)

        print("\n[SISTEMA] Servidor iniciado. Presiona Ctrl+C para detener.")
        client.loop_forever()

    except KeyboardInterrupt:
        print("\n\n[SISTEMA] Deteniendo servidor...")
        client.disconnect()
        if db_connection:
            db_connection.close()
        print("[SISTEMA] Servidor detenido correctamente")

    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        if db_connection:
            db_connection.close()


# =============================================================================
# EJECUTAR
# =============================================================================

if __name__ == "__main__":
    main()
