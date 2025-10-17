# Evidencia de Aprendizaje N°3 - Sistema IoT con Dashboard Web

### EVIDENCIA DE APRENDIZAJE N°3

_Escalado de Plataforma IoT con Visualización de Datos en Dashboard Web_

**INSTITUTO SUPERIOR POLITÉCNICO CÓRDOBA (ISPC)**

- Tecnicatura Superior en Desarrollo de Software
- Materia: Aproximación al Mundo del Trabajo
- Profesor: Mainero Alejandro Luis
- Estudiante: Fernando Moyano, Santiago Ortega
- Fecha de Entrega: 16 de Octubre de 2025

**Proyecto:**
Sistema IoT de Control de Iluminación Automática con Dashboard Web de Visualización en Tiempo Real utilizando Grafana

---

## 📑 Índice

- [Descripción](#descripción)
- [Características del Dashboard](#características-del-dashboard)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación Completa](#instalación-completa)
  - [1. Dependencias Python](#1-dependencias-python)
  - [2. Base de Datos MySQL](#2-base-de-datos-mysql)
  - [3. Configuración](#3-configuración)
  - [4. Instalación de Grafana](#4-instalación-de-grafana)
- [Uso del Sistema](#uso-del-sistema)
  - [Modo 1: Con Hardware Real (ESP32)](#modo-1-con-hardware-real-esp32)
  - [Modo 2: Sin Hardware (Simulación)](#modo-2-sin-hardware-simulación)
- [Dashboard de Grafana](#dashboard-de-grafana)
  - [Paneles Disponibles](#paneles-disponibles)
- [Funcionamiento del Sistema](#funcionamiento-del-sistema)
  - [Flujo de Datos](#flujo-de-datos)
  - [Lógica de Control](#lógica-de-control)
  - [Arquitectura de 5 Capas IoT](#arquitectura-de-5-capas-iot)
- [Consultas Útiles en Grafana](#consultas-útiles-en-grafana)
- [Solución de Problemas](#solución-de-problemas)
- [Acceso Web](#acceso-web)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Características Destacadas](#características-destacadas)
- [Autores](#autores)
- [Licencia](#licencia)

---

## Descripción

Sistema IoT completo que controla iluminación automática usando ESP32, sensor LDR, MQTT, MySQL y **Dashboard Web con Grafana** para visualización en tiempo real.

- [inidce](#-índice)

## Características del Dashboard

- **Visualización en tiempo real** de niveles de luminosidad
- **Gráficos interactivos** con histórico de datos
- **Sistema de alertas** configurables
- **Estadísticas del sistema** (promedio, máximo, mínimo)
- **Estado de dispositivos** ESP32
- **Interfaz web** accesible desde cualquier navegador

- [inidce](#-índice)

## Estructura del Proyecto

```
SolucionEV-3/
├── esp32_main.py              # Código para ESP32
├── servidor_mqtt_mysql.py     # Servidor Python con MQTT
├── simulador.py               # Simulador de hardware
├── base_datos.sql             # Script de base de datos
├── config.py                  # Configuración centralizada
├── .env                       # Variables de entorno (credenciales)
├── requirements.txt           # Dependencias Python
├── README.md                  # Este archivo
```

- [inidce](#-índice)

## Instalación Completa

### 1. Dependencias Python

```bash
pip install -r requirements.txt
```

**Dependencias:**

- `paho-mqtt==1.6.1` - Cliente MQTT
- `mysql-connector-python==8.0.33` - Conexión a MySQL

### 2. Base de Datos MySQL

```bash
mysql -u root -p < base_datos.sql
```

### 3. Configuración

**Opción A: Usando archivo .env (Recomendado)**

Crea un archivo `.env` en la raíz del proyecto:

```env
# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_DATABASE=control_iluminacion

# WiFi Configuration (para ESP32)
WIFI_SSID=TU_RED_WIFI
WIFI_PASSWORD=TU_CONTRASEÑA

# MQTT Configuration
MQTT_BROKER=broker.hivemq.com
MQTT_PORT=1883
```

**Opción B: Editando config.py directamente**

```python
WIFI_SSID = "TU_RED_WIFI"
WIFI_PASSWORD = "TU_CONTRASEÑA"

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'TU_CONTRASEÑA_MYSQL',
    'database': 'control_iluminacion'
}
```

### 4. Instalación de Grafana

Ver guía detallada en: `documentacion/instalacion_grafana.md`

**Resumen rápido:**

1. Descargar Grafana: https://grafana.com/grafana/download?platform=windows
2. Extraer en una carpeta (ej: `C:\Grafana\`)
3. Ejecutar `grafana-server.exe` desde `bin/`
4. Acceder a http://localhost:3000 (admin/admin)
5. Configurar data source MySQL
6. Crear dashboard con 6 paneles

- [inidce](#-índice)

## Uso del Sistema

### Modo 1: Con Hardware Real (ESP32)

#### A. Cargar código al ESP32

```bash
# Usar Thonny IDE
# 1. Conectar ESP32 por USB
# 2. Copiar esp32_main.py al ESP32
# 3. Copiar config.py al ESP32
# 4. Ejecutar
```

#### B. Iniciar servidor MQTT

```bash
python servidor_mqtt_mysql.py
```

#### C. Ejecutar ESP32

```bash
# En Thonny: Run → Run current script
# O presionar F5
```

#### D. Abrir Dashboard Grafana

```
http://localhost:3000
```

- [inidce](#-índice)

### Modo 2: Sin Hardware (Simulación)

#### Terminal 1 - Servidor

```bash
cd SolucionEV-3
python servidor_mqtt_mysql.py
```

Deberías ver:

```
============================================================
🚀 SERVIDOR MQTT → MySQL para Sistema IoT
============================================================
[MySQL] ✅ Conectado exitosamente
[MQTT] ✅ Conectado al broker: broker.hivemq.com
```

#### Terminal 2 - Simulador

```bash
cd SolucionEV-3
python simulador.py
```

Deberías ver:

```
============================================================
🎮 SIMULADOR ESP32 - Sistema de Iluminación
============================================================
[0001] 🌙 Luz:  654 | 💡 LED: ENCENDIDO
[0002] ☀️ Luz:  823 | ⚫ LED: APAGADO
```

#### Terminal 3 - Grafana

```bash
# Iniciar Grafana (si no está corriendo)
cd "C:\Grafana\grafana-v10.x.x\bin"
grafana-server.exe
```

#### Navegador

```
http://localhost:3000
```

- [inidce](#-índice)

## Dashboard de Grafana

### Paneles Disponibles

1. **Gráfico de Luminosidad en Tiempo Real**

   - Visualización continua de niveles de luz
   - Rango: 0-1023
   - Actualización automática cada 5 segundos
   - Tipo: Time Series (línea)

2. **Estado Actual del LED**

   - Indicador visual ENCENDIDO/APAGADO
   - Código de colores (Verde/Rojo)
   - Tipo: Stat

3. **Distribución Luz Alta/Baja**

   - Gráfico circular de clasificaciones
   - Porcentajes en tiempo real
   - Tipo: Pie Chart

4. **Últimas 20 Lecturas**

   - Tabla con historial reciente
   - Columnas: ID, Nivel Luz, Estado LED, Clasificación, Fecha/Hora
   - Tipo: Table

- [inidce](#-índice)

## Funcionamiento del Sistema

### Flujo de Datos

```
┌─────────┐      ┌──────────┐      ┌────────┐      ┌────────┐
│ ESP32   │─WiFi→│  MQTT    │─────→│ MySQL  │─────→│Grafana │
│ + LDR   │      │  Broker  │      │   DB   │      │Dashboard│
└─────────┘      └──────────┘      └────────┘      └────────┘
     │                                                    ↓
     └─────────── Control LED ←──────────────────────────┘
```

**Explicación:**

1. ESP32 lee el sensor LDR cada 2 segundos
2. Envía datos por MQTT al broker público
3. Servidor Python recibe datos y los guarda en MySQL
4. Grafana consulta MySQL cada 5 segundos
5. Dashboard muestra datos actualizados
6. Sistema de alertas monitorea condiciones críticas

### Lógica de Control

**Umbral:** 750

- **Si luminosidad ≤ 750:**

  - LED: ENCENDIDO
  - Clasificación: LUZ_BAJA
  - Color en Grafana: Amarillo/Naranja

- **Si luminosidad > 750:**
  - LED: APAGADO
  - Clasificación: LUZ_ALTA
  - Color en Grafana: Verde
- [inidce](#-índice)

### Arquitectura de 5 Capas IoT

1. **Capa Física:** ESP32 + Sensor LDR + LED
2. **Capa de Conectividad:** WiFi 802.11 b/g/n (2.4GHz)
3. **Capa de Red:** TCP/IP + Internet
4. **Capa de Transporte:** Protocolo MQTT v3.1.1
5. **Capa de Aplicación:** Servidor Python + MySQL + Grafana

- [inidce](#-índice)

## Consultas Útiles en Grafana

### Ver datos en tiempo real

```sql
SELECT
  timestamp AS "time",
  nivel_luz
FROM datos_luminosidad
WHERE $__timeFilter(timestamp)
ORDER BY timestamp
```

### Estadísticas del día

```sql
SELECT
    AVG(nivel_luz) as promedio,
    MIN(nivel_luz) as minimo,
    MAX(nivel_luz) as maximo,
    COUNT(*) as lecturas
FROM datos_luminosidad
WHERE DATE(timestamp) = CURDATE();
```

### Tiempo con LED encendido

```sql
SELECT
    COUNT(*) as lecturas_encendido,
    COUNT(*) * 2 / 60 as minutos_aproximados
FROM datos_luminosidad
WHERE estado_led = 'ENCENDIDO'
  AND timestamp >= NOW() - INTERVAL 24 HOUR;
```

### Distribución por clasificación

```sql
SELECT
  clasificacion,
  COUNT(*) as cantidad,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM datos_luminosidad), 2) as porcentaje
FROM datos_luminosidad
GROUP BY clasificacion;
```

## Solución de Problemas

- [inidce](#-índice)

### Grafana no muestra datos

1. ✅ Verificar que MySQL está corriendo

   ```bash
   # Windows: Services → MySQL → Running
   # Linux: sudo systemctl status mysql
   ```

2. ✅ Verificar conexión en Grafana → Configuration → Data Sources

   - Host: localhost:3306
   - Database: control_iluminacion
   - Hacer clic en "Save & test"

3. ✅ Ejecutar query de prueba en Explore

   ```sql
   SELECT COUNT(*) FROM datos_luminosidad;
   ```

4. ✅ Revisar que hay datos en la tabla
   ```bash
   mysql -u root -p
   USE control_iluminacion;
   SELECT * FROM datos_luminosidad LIMIT 10;
   ```

- [inidce](#-índice)

### Servidor Python no conecta a MySQL

```
[MySQL] ❌ ERROR: Access denied for user 'root'@'localhost'
```

**Solución:**

- Verificar contraseña en `.env` o `config.py`
- Verificar usuario MySQL existe y tiene permisos

### Simulador no envía datos

```
[MQTT] ❌ ERROR: Connection refused
```

**Solución:**

- Verificar conexión a internet
- El broker público puede estar saturado, esperar unos minutos
- Alternativa: instalar Mosquitto local

### Dashboard no se actualiza

1. Verificar el intervalo de refresh (arriba derecha)
   - Cambiar a "5s" o "10s"
2. Asegurarse que el time range incluye datos recientes
   - Usar "Last 15 minutes" o "Last 1 hour"
3. Hacer clic en el botón "Refresh dashboard"
4. Reiniciar Grafana si es necesario

### ESP32 no conecta a WiFi

```
[WiFi] ERROR: No se pudo conectar
```

**Solución:**

- Verificar SSID y contraseña en `config.py`
- Asegurar que la red es 2.4GHz (ESP32 no soporta 5GHz)
- Reiniciar router y ESP32

- [inidce](#-índice)

## Acceso Web

- **Grafana Dashboard:** http://localhost:3000
- **Usuario por defecto:** admin
- **Contraseña:** admin (o la que configuraste)

## Tecnologías Utilizadas

- **Hardware:** ESP32 DevKit, Sensor LDR, LED 5mm
- **Firmware:** MicroPython 1.20+
- **Protocolos:** WiFi 802.11 b/g/n, MQTT 3.1.1
- **Backend:** Python 3.8+
- **Base de Datos:** MySQL 8.0+
- **Visualización:** Grafana 10.0+
- **Broker MQTT:** HiveMQ (broker público gratuito)
- **Librerías Python:**
  - paho-mqtt 1.6.1
  - mysql-connector-python 8.0.33
- [inidce](#-índice)

## Autores

**Evidencia de Aprendizaje N°3**

- ISPC - Tecnicatura Superior en Desarrollo de Software
- Alumnos: Fernando Agustín Moyano, Santiago Ortega
- Materia: Aproximación al Mundo del Trabajo
- Profesor: Mainero Alejandro Luis
- Año: 2025

- [inidce](#-índice)

## Licencia

Proyecto académico - ISPC 2025

---
