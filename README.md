# Evidencia de Aprendizaje N°3 — Sistema IoT con Dashboard Web

_Escalado de Plataforma IoT con Visualización de Datos en Dashboard Web_

**INSTITUTO SUPERIOR POLITÉCNICO CÓRDOBA (ISPC)**

- Tecnicatura Superior en Desarrollo de Software
- Materia: Aproximación al Mundo del Trabajo
- Profesor: Mainero Alejandro Luis
- Alumnos: Fernando Agustín Moyano.
- Fecha de Entrega: 16 de Octubre de 2025

**Proyecto:**
Sistema IoT de Control de Iluminación Automática con Dashboard Web de Visualización en Tiempo Real utilizando Grafana.

---

## 📑 Índice

- [Descripción](#descripción)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación del Servidor](#instalación-del-servidor)
- [Uso del Sistema](#uso-del-sistema)
  - [Modo 1: Simulación con Wokwi](#modo-1-simulación-con-wokwi)
  - [Modo 2: Con Hardware Real (ESP32)](#modo-2-con-hardware-real-esp32)
- [Dashboard de Grafana](#dashboard-de-grafana)
- [Funcionamiento del Sistema](#funcionamiento-del-sistema)
- [Consultas Útiles en Grafana](#consultas-útiles-en-grafana)
- [Solución de Problemas](#solución-de-problemas)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Autores](#autores)

---

## Descripción

Sistema IoT completo que controla iluminación automática usando ESP32, sensor LDR y LED.
Los datos se transmiten por MQTT a un servidor Python que los almacena en MySQL.
Grafana visualiza el historial en tiempo real desde el navegador.

El circuito del ESP32 puede simularse en **Wokwi** sin necesidad de hardware físico.

---

## Estructura del Proyecto

```
SolucionEV-3/
├── servidor/                      ← corre en tu PC
│   ├── servidor.py                receptor MQTT + guardado en MySQL
│   ├── settings.py                configuración del servidor (lee .env)
│   ├── base_datos.sql             schema de la base de datos
│   └── requirements.txt           dependencias Python
│
├── wokwi/                         ← corre en el ESP32 (simulado en Wokwi)
│   ├── main.py                    lógica del ESP32: leer LDR, controlar LED, publicar MQTT
│   ├── settings.py                configuración del ESP32 (WiFi, pines, topics)
│   └── diagram.json               circuito del ESP32 para importar en Wokwi
│
├── docs/                          ← documentación y diagramas
│   ├── arquitectura_5_capas_compacta.wsd   diagrama PlantUML
│   └── images/                    capturas y diagramas visuales
│       ├── Arquitectura 5 capas.png
│       └── grafana1–5.jpg
│
├── .env                           ← credenciales del servidor (NO subir a Git)
├── .gitignore
└── README.md
```

---

## Instalación del Servidor

### 1. Dependencias Python

```bash
pip install -r servidor/requirements.txt
```

### 2. Base de Datos MySQL

```bash
mysql -u root -p < servidor/base_datos.sql
```

### 3. Configuración — archivo `.env`

Editá el archivo `.env` en la raíz del proyecto con tus credenciales:

```env
# MySQL
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_DATABASE=control_iluminacion

# MQTT
MQTT_BROKER=broker.hivemq.com
MQTT_PORT=1883
TOPIC_LUMINOSIDAD=Casa/Luminosidad
TOPIC_LED_ESTADO=Casa/LED_Estado

# Lógica (escala 12 bits, 0–4095)
UMBRAL_LUZ=3000
```

> ⚠️ El `.env` nunca debe subirse a repositorios públicos — ya está en `.gitignore`.

### 4. Instalación de Grafana

1. Descargar desde: https://grafana.com/grafana/download?platform=windows
2. Extraer en `C:\Grafana\`
3. Ejecutar `grafana-server.exe` desde `bin\`
4. Acceder a http://localhost:3000 (admin / admin)
5. Configurar data source MySQL
6. Crear dashboard con los paneles descritos más abajo

---

## Uso del Sistema

### Modo 1: Simulación con Wokwi

Permite probar el sistema completo sin hardware físico.
El ESP32 y sus sensores se simulan visualmente en el navegador.

#### Paso 1 — Iniciar el servidor Python

```bash
cd servidor
python servidor.py
```

Salida esperada:

```
[MySQL] ¡Conectado exitosamente!
[MQTT]  ¡Conectado al broker!
[SISTEMA] Esperando datos del ESP32...
```

#### Paso 2 — Abrir el circuito en Wokwi

1. Ir a https://wokwi.com → **New Project** → **ESP32** → **MicroPython**
2. Reemplazar `diagram.json` con el contenido de `wokwi/diagram.json`
3. Reemplazar `main.py` con el contenido de `wokwi/main.py`
4. Crear un archivo `settings.py` y pegar el contenido de `wokwi/settings.py`
5. Clic en **▶ Play**
6. Mover el **slider del LDR** para simular distintos niveles de luz
7. Observar los datos en el **Monitor Serie**

#### Paso 3 — Verificar en Grafana

```
http://localhost:3000
```

---

### Modo 2: Con Hardware Real (ESP32)

#### Circuito físico

```
ESP32  3V3   ──── LDR terminal 1
              LDR terminal 2 ──┬── ESP32 GPIO34  (ADC1)
                               │
                             10 kΩ
                               │
ESP32  GND   ──────────────────┘

ESP32  GPIO2 ──── LED (+) ──── R 220Ω ──── GND
```

> ⚠️ Usar GPIO34 para el LDR (ADC1). GPIO25 pertenece al ADC2 y se deshabilita cuando WiFi está activo.

#### Cargar el código al ESP32 con Thonny

1. Conectar el ESP32 por USB
2. Abrir Thonny → seleccionar intérprete MicroPython (ESP32)
3. Subir `wokwi/main.py` al ESP32 como **`main.py`**
4. Subir `wokwi/settings.py` al ESP32 como **`settings.py`**
5. Editar `settings.py` en el ESP32: cambiar `WIFI_SSID` y `WIFI_PASSWORD` por los de tu red real
6. Reiniciar el ESP32

#### Iniciar el servidor

```bash
cd servidor
python servidor.py
```

#### Abrir Grafana

```
http://localhost:3000
```

---

## Dashboard de Grafana

### Paneles disponibles

1. **Luminosidad en Tiempo Real** — gráfico de línea, rango 0–4095, actualización cada 5s
2. **Estado del LED** — indicador ENCENDIDO/APAGADO con código de colores
3. **Distribución Luz Alta/Baja** — gráfico circular con porcentajes
4. **Últimas 20 Lecturas** — tabla con ID, nivel de luz, estado LED, clasificación y timestamp

---

## Funcionamiento del Sistema

### Flujo de datos

```
┌──────────────┐      ┌───────────┐      ┌────────┐      ┌─────────┐
│  ESP32       │─────▶│   MQTT    │─────▶│ MySQL  │─────▶│ Grafana │
│  LDR + LED   │ WiFi │  Broker   │      │   DB   │      │Dashboard│
└──────────────┘      └───────────┘      └────────┘      └─────────┘
```

1. ESP32 lee el LDR cada 2 segundos
2. Publica luminosidad y estado del LED por MQTT
3. El servidor Python recibe los mensajes y hace INSERT en MySQL
4. Grafana consulta MySQL cada 5 segundos y actualiza los paneles

### Lógica de control

**Umbral: 3000** (escala 12 bits ADC del ESP32, rango 0–4095)

| Condición          | LED       | Clasificación |
| ------------------ | --------- | ------------- |
| luminosidad ≤ 3000 | ENCENDIDO | LUZ_BAJA      |
| luminosidad > 3000 | APAGADO   | LUZ_ALTA      |

### Arquitectura de 5 Capas IoT

1. **Capa Física:** ESP32 + Sensor LDR + LED
2. **Capa de Conectividad:** WiFi 802.11 b/g/n (2.4GHz)
3. **Capa de Red:** TCP/IP + Internet
4. **Capa de Transporte:** Protocolo MQTT v3.1.1
5. **Capa de Aplicación:** Servidor Python + MySQL + Grafana

![Arquitectura 5 capas](./docs/images/Arquitectura%205%20capas.png)

---

## Consultas Útiles en Grafana

Para cada panel: **+ → New dashboard → Add visualization → MySQL → (seleccionar tipo) → Query → Code → pegar query → Shift+Enter → Apply**

> `$__timeFilter(timestamp)` es una variable de Grafana que filtra automáticamente
> por el rango de tiempo seleccionado arriba a la derecha del dashboard.

---

### Luminosidad en tiempo real

**Visualización:** `Time series`

```sql
SELECT timestamp AS "time", nivel_luz
FROM datos_luminosidad
WHERE $__timeFilter(timestamp)
ORDER BY timestamp
```

---

### Estado del LED

**Visualización:** `Stat`

```sql
SELECT estado_led
FROM datos_luminosidad
ORDER BY timestamp DESC
LIMIT 1
```

> En opciones del panel → **Value mappings**: `ENCENDIDO` → color verde / `APAGADO` → color rojo.

---

### Distribución Luz Alta/Baja

**Visualización:** `Pie chart`

```sql
SELECT
    clasificacion,
    COUNT(*) as cantidad,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM datos_luminosidad), 2) as porcentaje
FROM datos_luminosidad
GROUP BY clasificacion;
```

---

### Últimas 20 lecturas

**Visualización:** `Table`

```sql
SELECT
    id,
    nivel_luz,
    estado_led,
    clasificacion,
    timestamp
FROM datos_luminosidad
WHERE $__timeFilter(timestamp)
ORDER BY timestamp DESC
LIMIT 20
```

---

### Queries adicionales

#### Estadísticas del día

**Visualización:** `Stat`

```sql
SELECT
    AVG(nivel_luz) as promedio,
    MIN(nivel_luz) as minimo,
    MAX(nivel_luz) as maximo,
    COUNT(*) as lecturas
FROM datos_luminosidad
WHERE DATE(timestamp) = CURDATE();
```

#### Tiempo con LED encendido

**Visualización:** `Stat`

```sql
SELECT
    COUNT(*) as lecturas_encendido,
    COUNT(*) * 2 / 60 as minutos_aproximados
FROM datos_luminosidad
WHERE estado_led = 'ENCENDIDO'
  AND timestamp >= NOW() - INTERVAL 24 HOUR;
```

---

## Solución de Problemas

### Grafana no muestra datos

1. Verificar que MySQL está corriendo
   ```bash
   # Windows: Servicios → MySQL → En ejecución
   ```
2. Grafana → Configuration → Data Sources → Save & test
3. Verificar que hay datos: `SELECT COUNT(*) FROM datos_luminosidad;`
4. Ajustar el rango de tiempo a "Last 15 minutes"

### Servidor no conecta a MySQL

```
[MySQL] ERROR: Access denied for user 'root'@'localhost'
```

Verificar contraseña en `.env` y que el usuario MySQL tiene permisos.

### ESP32 no conecta a WiFi

```
[WiFi] ERROR: No se pudo conectar
```

- Verificar `WIFI_SSID` y `WIFI_PASSWORD` en `wokwi/settings.py`
- El ESP32 solo soporta redes **2.4GHz** (no 5GHz)

### Wokwi no envía datos MQTT

- Verificar que el servidor Python está corriendo antes de iniciar Wokwi
- El broker `broker.hivemq.com` es público — si falla, puede estar saturado, esperar unos minutos

---

## Tecnologías Utilizadas

| Componente            | Tecnología                                     |
| --------------------- | ---------------------------------------------- |
| Microcontrolador      | ESP32 DevKit C V4                              |
| Firmware              | MicroPython v1.22.0                            |
| Sensor                | LDR (fotorresistor) en GPIO34                  |
| Actuador              | LED en GPIO2                                   |
| Simulador de circuito | Wokwi                                          |
| Protocolo IoT         | MQTT v3.1.1                                    |
| Broker MQTT           | HiveMQ (broker público)                        |
| Comunicación          | WiFi 802.11 b/g/n (2.4GHz)                     |
| Backend               | Python 3.8+                                    |
| Base de datos         | MySQL 8.0+                                     |
| Visualización         | Grafana 10.0+                                  |
| Librerías Python      | paho-mqtt 1.6.1, mysql-connector-python 8.0.33 |

---

## Autores

- **Alumnos:** Fernando Agustín Moyano, Santiago Ortega
- **Materia:** Aproximación al Mundo del Trabajo
- **Profesor:** Mainero Alejandro Luis
- **Instituto:** ISPC — Tecnicatura Superior en Desarrollo de Software
- **Año:** 2025

---

## Licencia

Proyecto académico — ISPC 2025
