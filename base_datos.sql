-- =============================================================================
-- Script de Base de Datos - Sistema Control de Iluminación IoT
-- =============================================================================
-- Este script crea la base de datos y la tabla necesaria para el sistema

-- =============================================================================
-- CREAR BASE DE DATOS
-- =============================================================================
CREATE DATABASE IF NOT EXISTS control_iluminacion;

-- Usar la base de datos
USE control_iluminacion;

-- =============================================================================
-- CREAR TABLA DE DATOS
-- =============================================================================
CREATE TABLE IF NOT EXISTS datos_luminosidad (
    -- ID único autoincremental para cada registro
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Nivel de luz medido por el sensor LDR (0-1023)
    nivel_luz INT NOT NULL,
    
    -- Estado del LED ('ENCENDIDO' o 'APAGADO')
    estado_led VARCHAR(10) NOT NULL,
    
    -- Clasificación automática ('LUZ_BAJA' o 'LUZ_ALTA')
    clasificacion VARCHAR(20) NOT NULL,
    
    -- Marca de tiempo automática
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índice para búsquedas rápidas por fecha
    INDEX idx_timestamp (timestamp),
    
    -- Índice para búsquedas por clasificación
    INDEX idx_clasificacion (clasificacion)
);

-- =============================================================================
-- CONSULTAS ÚTILES PARA MONITOREO
-- =============================================================================

-- Ver las últimas 10 lecturas
-- SELECT * FROM datos_luminosidad ORDER BY timestamp DESC LIMIT 10;

-- Ver estadísticas generales
-- SELECT 
--     COUNT(*) as total_lecturas,
--     AVG(nivel_luz) as promedio_luz,
--     MIN(nivel_luz) as luz_minima,
--     MAX(nivel_luz) as luz_maxima,
--     COUNT(CASE WHEN estado_led = 'ENCENDIDO' THEN 1 END) as veces_encendido,
--     COUNT(CASE WHEN estado_led = 'APAGADO' THEN 1 END) as veces_apagado
-- FROM datos_luminosidad;

-- Ver lecturas del último día
-- SELECT * FROM datos_luminosidad 
-- WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 1 DAY)
-- ORDER BY timestamp DESC;

-- Ver lecturas por clasificación
-- SELECT clasificacion, COUNT(*) as cantidad
-- FROM datos_luminosidad
-- GROUP BY clasificacion;

-- Limpiar todos los datos (CUIDADO: esto borra todo)
-- DELETE FROM datos_luminosidad WHERE id > 0;

-- =============================================================================
-- INFORMACIÓN
-- =============================================================================
-- Esta base de datos almacena:
-- - Todas las lecturas del sensor LDR
-- - Estado del LED en cada lectura
-- - Clasificación automática (luz baja/alta)
-- - Fecha y hora de cada lectura
--
-- El sistema usa un umbral de 750 para determinar:
-- - Si nivel_luz <= 750: LED ENCENDIDO (LUZ_BAJA)
-- - Si nivel_luz > 750: LED APAGADO (LUZ_ALTA)
-- =============================================================================
