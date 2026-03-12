# Referencia de Librerías — Sistema IoT de Iluminación

Documentación de todas las clases y métodos utilizados en el proyecto,
organizados por entorno de ejecución.

---

## Menú

### MicroPython (ESP32 — `wokwi/main.py`)

- [[#Pin]]
- [[#ADC]]
- [[#machine]]
- [[#utime]]
- [[#network]]
- [[#ubinascii]]
- [[#umqtt.simple]]

### Python estándar (Servidor PC — `servidor/servidor.py`)

- [[#mysql.connector]]
- [[#paho.mqtt.client]]
- [[#datetime]]

---

# MicroPython — ESP32

> Estas librerías forman parte del firmware de MicroPython.
> No requieren instalación. Solo funcionan en el ESP32 (o en Wokwi).
> Importarlas en Python estándar genera `ModuleNotFoundError`.

---

## Pin

```python
from machine import Pin
```

Controla los pines GPIO digitales del ESP32 como entrada o salida.

### Constructor

```python
Pin(id, mode, pull)
```

| Parámetro | Tipo    | Descripción                              |
| --------- | ------- | ---------------------------------------- |
| `id`      | `int`   | Número de GPIO (ej: `2`, `34`)           |
| `mode`    | `const` | `Pin.IN` = entrada / `Pin.OUT` = salida  |
| `pull`    | `const` | `Pin.PULL_UP` / `Pin.PULL_DOWN` / omitir |

```python
# Ejemplos
led    = Pin(2,  Pin.OUT)
sensor = Pin(27, Pin.IN)
boton  = Pin(0,  Pin.IN, Pin.PULL_UP)
```

### Métodos

| Método           | Parámetros         | Retorna       | Descripción                          |
| ---------------- | ------------------ | ------------- | ------------------------------------ |
| `pin.value()`    | —                  | `int` (0 ó 1) | Lee el estado actual del pin         |
| `pin.value(val)` | `val: int` (0 ó 1) | `None`        | Escribe HIGH (1) o LOW (0) en el pin |
| `pin.on()`       | —                  | `None`        | Equivale a `pin.value(1)`            |
| `pin.off()`      | —                  | `None`        | Equivale a `pin.value(0)`            |

```python
led.value(1)       # encender
led.value(0)       # apagar
estado = sensor.value()   # leer
```

---

## ADC

```python
from machine import ADC, Pin
```

Convierte una señal analógica (voltaje) en un valor digital.
En el ESP32 el ADC es de **12 bits → rango 0–4095**.

> ⚠️ Usar solo pines de **ADC1** (GPIO32–GPIO39) cuando WiFi está activo.
> Los pines de ADC2 (incluido GPIO25) se deshabilitan con WiFi.

### Constructor

```python
ADC(pin)
```

| Parámetro | Tipo  | Descripción                                |
| --------- | ----- | ------------------------------------------ |
| `pin`     | `Pin` | Objeto Pin ya creado con el GPIO analógico |

```python
ldr = ADC(Pin(34))
```

### Métodos

| Método            | Parámetros    | Retorna        | Descripción                           |
| ----------------- | ------------- | -------------- | ------------------------------------- |
| `adc.atten(attn)` | `attn: const` | `None`         | Define el rango de voltaje de entrada |
| `adc.read()`      | —             | `int` (0–4095) | Lee el valor ADC actual               |

### Constantes de atenuación para `atten()`

| Constante        | Rango de voltaje | Uso                               |
| ---------------- | ---------------- | --------------------------------- |
| `ADC.ATTN_0DB`   | 0 – 1.0 V        | Sin atenuación                    |
| `ADC.ATTN_2_5DB` | 0 – 1.34 V       | Atenuación baja                   |
| `ADC.ATTN_6DB`   | 0 – 2.0 V        | Atenuación media                  |
| `ADC.ATTN_11DB`  | 0 – 3.3 V        | **Rango completo — usar siempre** |

```python
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)   # habilitar rango completo
valor = ldr.read()          # 0 (oscuridad) – 4095 (luz máxima)
```

---

## machine

```python
import machine
```

Módulo de acceso al hardware del microcontrolador.
En el proyecto se usa exclusivamente para obtener el ID único del ESP32.

### Función usada

| Función               | Parámetros | Retorna | Descripción                   |
| --------------------- | ---------- | ------- | ----------------------------- |
| `machine.unique_id()` | —          | `bytes` | ID único del chip (6–8 bytes) |

```python
import machine
raw_id = machine.unique_id()   # b'\xd8\xa0\x1d...'
```

> Se convierte a hexadecimal con `ubinascii.hexlify()` para usarlo como `client_id` en MQTT.

---

## utime

```python
import utime
```

Módulo de tiempo de MicroPython. Equivalente a `time` en Python estándar,
con algunas diferencias de nombre en los métodos.

### Métodos usados en el proyecto

| Método               | Parámetros | Retorna | Equivalente Python    | Descripción                  |
| -------------------- | ---------- | ------- | --------------------- | ---------------------------- |
| `utime.sleep(s)`     | `s: float` | `None`  | `time.sleep(s)`       | Pausa en segundos            |
| `utime.sleep_ms(ms)` | `ms: int`  | `None`  | `time.sleep(ms/1000)` | Pausa en milisegundos        |
| `utime.sleep_us(us)` | `us: int`  | `None`  | —                     | Pausa en microsegundos       |
| `utime.ticks_ms()`   | —          | `int`   | `time.time() * 1000`  | Milisegundos desde el inicio |

```python
utime.sleep(2)          # pausa 2 segundos (equivale a delay(2000) en Arduino)
utime.sleep_ms(500)     # pausa 500 ms
t = utime.ticks_ms()    # tiempo transcurrido
```

---

## network

```python
import network
```

Gestiona las interfaces de red del ESP32 (WiFi, Ethernet).
En el proyecto se usa para conectar el ESP32 a una red WiFi.

### Clase usada: `WLAN`

```python
wlan = network.WLAN(interface)
```

| Parámetro   | Tipo    | Descripción                                                         |
| ----------- | ------- | ------------------------------------------------------------------- |
| `interface` | `const` | `network.STA_IF` = cliente WiFi / `network.AP_IF` = punto de acceso |

### Métodos de `WLAN`

| Método                    | Parámetros              | Retorna | Descripción                         |
| ------------------------- | ----------------------- | ------- | ----------------------------------- |
| `wlan.active(state)`      | `state: bool`           | `None`  | Activa o desactiva la interfaz WiFi |
| `wlan.connect(ssid, pwd)` | `ssid: str`, `pwd: str` | `None`  | Inicia la conexión a la red         |
| `wlan.isconnected()`      | —                       | `bool`  | `True` si hay conexión activa       |
| `wlan.ifconfig()`         | —                       | `tuple` | `(ip, mask, gateway, dns)`          |

```python
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wokwi-GUEST", "")
while not wlan.isconnected():
    utime.sleep(1)
ip = wlan.ifconfig()[0]   # obtener IP asignada
```

---

## ubinascii

```python
import ubinascii
```

Conversiones entre binario y ASCII. En el proyecto se usa
para convertir el ID binario del chip a una cadena hexadecimal legible.

### Método usado

| Método                    | Parámetros    | Retorna | Descripción                                        |
| ------------------------- | ------------- | ------- | -------------------------------------------------- |
| `ubinascii.hexlify(data)` | `data: bytes` | `bytes` | Convierte bytes a representación hexadecimal ASCII |

```python
import machine, ubinascii
client_id = ubinascii.hexlify(machine.unique_id())
# resultado: b'd8a01d5c3f22' — usado como ID único en MQTT
```

---

## umqtt.simple

```python
from umqtt.simple import MQTTClient
```

Implementación MQTT incluida en el firmware de MicroPython.
Permite publicar y suscribirse a tópicos en un broker MQTT.

> Documentación oficial: https://docs.micropython.org/en/latest/library/umqtt.simple.html

### Constructor `MQTTClient`

```python
MQTTClient(client_id, server, port, user, password, keepalive, ssl)
```

| Parámetro   | Tipo             | Requerido | Descripción                                      |
| ----------- | ---------------- | --------- | ------------------------------------------------ |
| `client_id` | `str` \| `bytes` | ✅        | ID único del cliente en el broker                |
| `server`    | `str`            | ✅        | Dirección del broker (ej: `"broker.hivemq.com"`) |
| `port`      | `int`            | ✅        | Puerto del broker (1883 sin TLS / 8883 con TLS)  |
| `user`      | `str`            | ❌        | Usuario (si el broker requiere autenticación)    |
| `password`  | `str`            | ❌        | Contraseña                                       |
| `keepalive` | `int`            | ❌        | Intervalo keepalive en segundos (default: 0)     |
| `ssl`       | `bool`           | ❌        | `True` para conexión TLS/SSL                     |

```python
from umqtt.simple import MQTTClient
client = MQTTClient(client_id, "broker.hivemq.com", 1883)
```

### Métodos

| Método                       | Parámetros                             | Retorna | Descripción                                      |
| ---------------------------- | -------------------------------------- | ------- | ------------------------------------------------ |
| `client.connect()`           | —                                      | `bool`  | Conecta al broker                                |
| `client.disconnect()`        | —                                      | `None`  | Cierra la conexión                               |
| `client.publish(topic, msg)` | `topic: bytes\|str`, `msg: bytes\|str` | `None`  | Publica un mensaje en un tópico                  |
| `client.subscribe(topic)`    | `topic: bytes\|str`                    | `None`  | Se suscribe a un tópico                          |
| `client.check_msg()`         | —                                      | `None`  | Verifica mensajes entrantes (no bloqueante)      |
| `client.wait_msg()`          | —                                      | `None`  | Espera un mensaje entrante (bloqueante)          |
| `client.set_callback(func)`  | `func: callable`                       | `None`  | Define la función que procesa mensajes recibidos |

```python
client = MQTTClient(client_id, "broker.hivemq.com", 1883)
client.connect()
client.publish("Casa/Luminosidad", str(valor))   # publicar
client.publish("Casa/LED_Estado",  "ENCENDIDO")
client.disconnect()
```

---

---

# Python Estándar — Servidor PC

> Estas librerías corren en tu PC con Python 3.8+.
> Se instalan con `pip install -r servidor/requirements.txt`.
> No funcionan en el ESP32.

---

## mysql.connector

```python
import mysql.connector
```

Librería oficial de MySQL para Python. Permite conectarse y ejecutar
consultas SQL sobre una base de datos MySQL.

**Instalación:** `pip install mysql-connector-python==8.0.33`

### Función de conexión

```python
mysql.connector.connect(**config)
```

| Parámetro  | Tipo  | Descripción                                      |
| ---------- | ----- | ------------------------------------------------ |
| `host`     | `str` | Dirección del servidor MySQL (ej: `"localhost"`) |
| `user`     | `str` | Usuario de la base de datos                      |
| `password` | `str` | Contraseña del usuario                           |
| `database` | `str` | Nombre de la base de datos                       |

```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mi_contraseña",
    database="control_iluminacion"
)
```

### Métodos del objeto `connection`

| Método                | Parámetros | Retorna  | Descripción                                                   |
| --------------------- | ---------- | -------- | ------------------------------------------------------------- |
| `connection.cursor()` | —          | `cursor` | Crea un cursor para ejecutar consultas                        |
| `connection.commit()` | —          | `None`   | Confirma la transacción actual (necesario tras INSERT/UPDATE) |
| `connection.close()`  | —          | `None`   | Cierra la conexión                                            |

### Métodos del objeto `cursor`

| Método                        | Parámetros                  | Retorna           | Descripción                                     |
| ----------------------------- | --------------------------- | ----------------- | ----------------------------------------------- |
| `cursor.execute(sql, params)` | `sql: str`, `params: tuple` | `None`            | Ejecuta una consulta SQL con parámetros seguros |
| `cursor.fetchall()`           | —                           | `list[tuple]`     | Retorna todas las filas del resultado           |
| `cursor.fetchone()`           | —                           | `tuple` \| `None` | Retorna la siguiente fila del resultado         |
| `cursor.close()`              | —                           | `None`            | Cierra el cursor                                |

### Excepción

| Excepción               | Cuándo ocurre                          |
| ----------------------- | -------------------------------------- |
| `mysql.connector.Error` | Cualquier error de conexión o consulta |

```python
cursor = connection.cursor()
sql = "INSERT INTO datos_luminosidad (nivel_luz, estado_led, clasificacion) VALUES (%s, %s, %s)"
cursor.execute(sql, (2500, "ENCENDIDO", "LUZ_BAJA"))
connection.commit()
cursor.close()
```

> ⚠️ Usar siempre parámetros `%s` en lugar de concatenar strings — previene inyección SQL.

---

## paho.mqtt.client

```python
import paho.mqtt.client as mqtt
```

Librería MQTT para Python estándar. Permite conectarse a un broker,
publicar mensajes y suscribirse a tópicos.

**Instalación:** `pip install paho-mqtt==1.6.1`

> ⚠️ La sintaxis del constructor cambió entre versiones:
>
> - **paho 1.x:** `mqtt.Client("nombre")`
> - **paho 2.x:** `mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "nombre")`
>   El proyecto usa **paho 1.6.1**.

### Constructor `Client`

```python
mqtt.Client(client_id, clean_session, userdata, protocol)
```

| Parámetro       | Tipo    | Descripción                                                 |
| --------------- | ------- | ----------------------------------------------------------- |
| `client_id`     | `str`   | ID único del cliente en el broker                           |
| `clean_session` | `bool`  | `True` = sesión limpia al conectar (default: `True`)        |
| `userdata`      | `any`   | Dato personalizado pasado a los callbacks (default: `None`) |
| `protocol`      | `const` | Versión MQTT (default: `mqtt.MQTTv311`)                     |

```python
client = mqtt.Client("Servidor_Iluminacion_IoT")
```

### Métodos principales

| Método                                  | Parámetros                                      | Retorna | Descripción                                                     |
| --------------------------------------- | ----------------------------------------------- | ------- | --------------------------------------------------------------- |
| `client.connect(host, port, keepalive)` | `host: str`, `port: int`, `keepalive: int`      | `None`  | Conecta al broker                                               |
| `client.disconnect()`                   | —                                               | `None`  | Desconecta del broker                                           |
| `client.publish(topic, payload)`        | `topic: str`, `payload: str\|bytes\|int\|float` | `None`  | Publica un mensaje                                              |
| `client.subscribe(topic)`               | `topic: str`                                    | `None`  | Se suscribe a un tópico                                         |
| `client.loop_forever()`                 | —                                               | `None`  | Mantiene el cliente activo bloqueando el hilo (uso en servidor) |
| `client.loop_start()`                   | —                                               | `None`  | Inicia el loop en un hilo separado (no bloqueante)              |
| `client.loop_stop()`                    | —                                               | `None`  | Detiene el loop del hilo separado                               |

### Propiedades de callback

| Propiedad              | Firma de la función                 | Descripción                    |
| ---------------------- | ----------------------------------- | ------------------------------ |
| `client.on_connect`    | `func(client, userdata, flags, rc)` | Se llama al conectar al broker |
| `client.on_message`    | `func(client, userdata, msg)`       | Se llama al recibir un mensaje |
| `client.on_disconnect` | `func(client, userdata, rc)`        | Se llama al desconectarse      |

### Objeto `msg` recibido en `on_message`

| Atributo      | Tipo    | Descripción                                         |
| ------------- | ------- | --------------------------------------------------- |
| `msg.topic`   | `str`   | Tópico del mensaje recibido                         |
| `msg.payload` | `bytes` | Contenido del mensaje (decodificar con `.decode()`) |
| `msg.qos`     | `int`   | Nivel de calidad de servicio (0, 1 ó 2)             |
| `msg.retain`  | `bool`  | `True` si es un mensaje retenido                    |

### Códigos de resultado `rc` en `on_connect`

| Código | Significado                       |
| ------ | --------------------------------- |
| `0`    | Conexión exitosa                  |
| `1`    | Versión de protocolo incorrecta   |
| `2`    | Identificador de cliente inválido |
| `3`    | Servidor no disponible            |
| `4`    | Usuario o contraseña incorrectos  |
| `5`    | No autorizado                     |

```python
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("Casa/Luminosidad")
        client.subscribe("Casa/LED_Estado")

def on_message(client, userdata, msg):
    topic   = msg.topic
    mensaje = msg.payload.decode()
    print(f"Recibido: {topic} = {mensaje}")

client = mqtt.Client("Servidor_Iluminacion_IoT")
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()
```

---

## datetime

```python
from datetime import datetime
```

Módulo de la librería estándar de Python para manejo de fechas y horas.
En el proyecto se usa para mostrar el timestamp en cada INSERT.

### Clase `datetime`

| Método                       | Parámetros     | Retorna    | Descripción                                     |
| ---------------------------- | -------------- | ---------- | ----------------------------------------------- |
| `datetime.now()`             | —              | `datetime` | Fecha y hora actual del sistema                 |
| `datetime.strftime(formato)` | `formato: str` | `str`      | Convierte la fecha a string con el formato dado |

### Códigos de formato más usados

| Código | Significado         | Ejemplo |
| ------ | ------------------- | ------- |
| `%Y`   | Año con 4 dígitos   | `2025`  |
| `%m`   | Mes con 2 dígitos   | `10`    |
| `%d`   | Día con 2 dígitos   | `16`    |
| `%H`   | Hora en formato 24h | `14`    |
| `%M`   | Minutos             | `35`    |
| `%S`   | Segundos            | `07`    |

```python
from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(timestamp)   # "2025-10-16 14:35:07"
```

---

## Resumen comparativo por entorno

| Librería           | Entorno | Propósito en el proyecto                    |
| ------------------ | ------- | ------------------------------------------- |
| `Pin`              | ESP32   | Controlar el LED y leer el PIR              |
| `ADC`              | ESP32   | Leer el valor del sensor LDR                |
| `machine`          | ESP32   | Obtener el ID único del chip                |
| `utime`            | ESP32   | Pausas entre lecturas del sensor            |
| `network`          | ESP32   | Conectarse a la red WiFi                    |
| `ubinascii`        | ESP32   | Convertir el ID del chip a string para MQTT |
| `umqtt.simple`     | ESP32   | Publicar datos al broker MQTT               |
| `mysql.connector`  | PC      | Guardar lecturas en la base de datos        |
| `paho.mqtt.client` | PC      | Recibir datos del broker MQTT               |
| `datetime`         | PC      | Registrar el timestamp de cada lectura      |
