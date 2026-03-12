-- =============================================================================
-- base_datos.sql — Schema de Base de Datos
-- Sistema Control de Iluminación IoT
-- =============================================================================
-- Ejecutar una sola vez para crear la base de datos y la tabla:
--   mysql -u root -p < servidor/base_datos.sql
-- =============================================================================

CREATE DATABASE IF NOT EXISTS control_iluminacion;
USE control_iluminacion;

-- =============================================================================
-- TABLA PRINCIPAL
-- =============================================================================

CREATE TABLE IF NOT EXISTS datos_luminosidad (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    nivel_luz      INT          NOT NULL,               -- 0–4095 (ADC 12 bits del ESP32)
    estado_led     VARCHAR(10)  NOT NULL,               -- 'ENCENDIDO' o 'APAGADO'
    clasificacion  VARCHAR(20)  NOT NULL,               -- 'LUZ_BAJA' o 'LUZ_ALTA'
    timestamp      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_timestamp     (timestamp),
    INDEX idx_clasificacion (clasificacion)
);

-- =============================================================================
-- LÓGICA DE CLASIFICACIÓN (referencia)
-- =============================================================================
-- Umbral: 3000 (escala 12 bits, 0–4095)
--   nivel_luz <= 3000 → LED ENCENDIDO → clasificacion = 'LUZ_BAJA'
--   nivel_luz >  3000 → LED APAGADO  → clasificacion = 'LUZ_ALTA'

-- =============================================================================
-- CONSULTAS ÚTILES
-- =============================================================================

-- Últimas 10 lecturas:
-- SELECT * FROM datos_luminosidad ORDER BY timestamp DESC LIMIT 10;

-- Estadísticas generales:
-- SELECT
--     COUNT(*) as total_lecturas,
--     AVG(nivel_luz) as promedio_luz,
--     MIN(nivel_luz) as luz_minima,
--     MAX(nivel_luz) as luz_maxima,
--     COUNT(CASE WHEN estado_led = 'ENCENDIDO' THEN 1 END) as veces_encendido,
--     COUNT(CASE WHEN estado_led = 'APAGADO'   THEN 1 END) as veces_apagado
-- FROM datos_luminosidad;

-- Lecturas del último día:
-- SELECT * FROM datos_luminosidad
-- WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 1 DAY)
-- ORDER BY timestamp DESC;

-- Distribución por clasificación:
-- SELECT clasificacion, COUNT(*) as cantidad
-- FROM datos_luminosidad GROUP BY clasificacion;

-- Limpiar todos los datos (CUIDADO):
-- TRUNCATE TABLE datos_luminosidad;
