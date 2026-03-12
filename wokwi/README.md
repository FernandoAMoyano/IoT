# Wokwi — Simulación del Sistema de Iluminación IoT

Carpeta con los tres archivos necesarios para correr el proyecto en Wokwi.
No se necesita ningún otro archivo del proyecto para esta simulación.

---

## Archivos

| Archivo | Función |
|---|---|
| `diagram.json` | Circuito: ESP32 + LDR + LED + resistencia |
| `main.py` | Código MicroPython del ESP32 |
| `config.py` | Configuración adaptada para MicroPython/Wokwi |

---

## Cómo usarlo

1. Ir a **https://wokwi.com**
2. Clic en **New Project** → **ESP32** → **MicroPython**
3. Reemplazar el contenido de `diagram.json` con el de esta carpeta
4. Reemplazar el contenido de `main.py` con el de esta carpeta
5. Crear un archivo nuevo llamado `config.py` y pegar el contenido
6. Clic en **▶ Play**
7. Mover el **slider del LDR** para simular diferentes niveles de luz
8. Ver los resultados en el **Monitor Serie**

---

## Circuito

```
ESP32  3V3   ──── LDR sensor VCC
ESP32  GND   ──── LDR sensor GND
LDR sensor AO ── ESP32 GPIO34   ← lectura analógica (ADC1)

ESP32  GPIO2 ──── LED (+)
             LED (−) ──── R220Ω ──── ESP32 GND
```

---

## Salida esperada en Monitor Serie

```
==================================================
 Sistema Control de Iluminación IoT
 Evidencia de Aprendizaje N°3 — Wokwi
==================================================

[WiFi] Conectando a: Wokwi-GUEST
[WiFi] ¡Conectado!
[MQTT] ¡Conectado al broker!

[SISTEMA] Umbral de luz: 750
[SISTEMA] Mueve el slider del LDR en Wokwi para simular luz

[DATOS] Luz:  512 ( 12%) | LED: ENCENDIDO
[MQTT]  Datos enviados
--------------------------------------------------
[DATOS] Luz: 3200 ( 78%) | LED: APAGADO
[MQTT]  Datos enviados
--------------------------------------------------
```

---

## Diferencias con el proyecto original

| Punto | Proyecto original | Esta versión Wokwi |
|---|---|---|
| `config.py` | Usa `os` y `.env` (Python estándar) | Solo variables simples (MicroPython) |
| `PIN_LDR` | GPIO25 (ADC2, bug con WiFi) | GPIO34 (ADC1, correcto) |
| WiFi SSID | Red real del usuario | `Wokwi-GUEST` (red simulada) |
| `simulador.py` | Necesario sin hardware | No necesario — Wokwi lo reemplaza |
| `if __name__ == "__main__"` | Presente | Removido (no aplica en MicroPython) |
