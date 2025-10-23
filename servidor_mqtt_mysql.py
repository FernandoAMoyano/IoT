# =============================================================================
# Servidor MQTT-MySQL - Sistema Control de Iluminación IoT
# =============================================================================
# Este servidor recibe datos del ESP32 por MQTT y los almacena en MySQL

# =============================================================================
# IMPORTAR LIBRERÍAS
# =============================================================================

import mysql.connector
import paho.mqtt.client as mqtt
import config
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
    Conecta a la base de datos MySQL
    Retorna la conexión o None si falla
    """
    print("\n[MySQL] Intentando conexión...")
    try:
        connection = mysql.connector.connect(**config.DB_CONFIG)
        print("[MySQL] ¡Conectado exitosamente!")
        print(f"[MySQL] Base de datos: {config.DB_CONFIG['database']}")
        return connection
    except mysql.connector.Error as e:
        print(f"[MySQL] Error de conexión: {e}")
        print("[MySQL] Verifica:")
        print("  - MySQL está ejecutándose")
        print("  - Credenciales en config.py son correctas")
        print("  - Base de datos existe")
        return None


# =============================================================================
# FUNCIÓN: Guardar datos en MySQL
# =============================================================================


def guardar_datos(luminosidad, estado_led):
    """
    Guarda una lectura en la base de datos
    """
    global db_connection

    if not db_connection:
        print("[MySQL] No hay conexión a la base de datos")
        return False

    try:
        cursor = db_connection.cursor()

        # Clasificar según el umbral
        if luminosidad <= config.UMBRAL_LUZ:
            clasificacion = "LUZ_BAJA"
        else:
            clasificacion = "LUZ_ALTA"

        # Preparar consulta SQL
        sql = """
        INSERT INTO datos_luminosidad 
        (nivel_luz, estado_led, clasificacion) 
        VALUES (%s, %s, %s)
        """

        # Ejecutar consulta
        valores = (luminosidad, estado_led, clasificacion)
        cursor.execute(sql, valores)
        db_connection.commit()

        # Mostrar confirmación
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[GUARDADO] {timestamp}")
        print(f"  Luminosidad: {luminosidad}")
        print(f"  LED: {estado_led}")
        print(f"  Clasificación: {clasificacion}")
        print("-" * 50)

        cursor.close()
        return True

    except mysql.connector.Error as e:
        print(f"[MySQL] Error al guardar: {e}")
        return False


# =============================================================================
# CALLBACK: Cuando se conecta a MQTT
# =============================================================================


def on_connect(client, userdata, flags, rc):
    """
    Callback que se ejecuta cuando el cliente se conecta al broker MQTT
    """
    if rc == 0:
        print("\n[MQTT] ¡Conectado al broker!")
        print(f"[MQTT] Broker: {config.MQTT_BROKER}")
        print("[MQTT] Suscribiéndose a tópicos...")

        # Suscribirse a los tópicos
        client.subscribe(config.TOPIC_LUMINOSIDAD)
        client.subscribe(config.TOPIC_LED_ESTADO)

        print(f"  - {config.TOPIC_LUMINOSIDAD}")
        print(f"  - {config.TOPIC_LED_ESTADO}")
        print("\n[SISTEMA] Esperando datos del ESP32...")
        print("-" * 50)
    else:
        print(f"[MQTT] Error de conexión. Código: {rc}")


# =============================================================================
# CALLBACK: Cuando llega un mensaje MQTT
# =============================================================================


def on_message(client, userdata, msg):
    """
    Callback que se ejecuta cuando llega un mensaje MQTT
    """
    global datos_temp

    # Decodificar mensaje
    topic = msg.topic
    mensaje = msg.payload.decode()

    print(f"\n[RECIBIDO] {topic} = {mensaje}")

    # Procesar según el tópico
    if topic == config.TOPIC_LUMINOSIDAD:
        try:
            datos_temp["luminosidad"] = int(mensaje)
        except ValueError:
            print(f"[ERROR] Valor de luminosidad inválido: {mensaje}")
            return

    elif topic == config.TOPIC_LED_ESTADO:
        datos_temp["estado_led"] = mensaje

    # Si tenemos ambos datos, guardar en base de datos
    if datos_temp["luminosidad"] is not None and datos_temp["estado_led"] is not None:
        guardar_datos(datos_temp["luminosidad"], datos_temp["estado_led"])
        # Resetear datos temporales
        datos_temp["luminosidad"] = None
        datos_temp["estado_led"] = None


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================


def main():
    """
    Función principal del servidor
    """
    global db_connection

    print("\n" + "=" * 60)
    print(" Servidor MQTT-MySQL - Control de Iluminación IoT")
    print(" Evidencia de Aprendizaje N°3")
    print("=" * 60)

    # Conectar a MySQL
    db_connection = conectar_mysql()
    if not db_connection:
        print("\n[ERROR] No se pudo conectar a MySQL")
        print("El servidor no puede funcionar sin base de datos")
        return

    # Configurar cliente MQTT
    print("\n[MQTT] Configurando cliente...")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Servidor_Iluminacion_IoT")

    # Asignar callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Conectar al broker MQTT
    try:
        print(f"[MQTT] Conectando a {config.MQTT_BROKER}...")
        client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)

        print("\n[SISTEMA] Servidor iniciado correctamente")
        print("[SISTEMA] Presiona Ctrl+C para detener")

        # Mantener el loop activo
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
# EJECUTAR PROGRAMA
# =============================================================================

if __name__ == "__main__":
    main()
