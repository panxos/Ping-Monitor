# 🌐 Ping-Monitor: Monitor de Red con Sistema de Semáforo

<p align="center">
  <img src="https://raw.githubusercontent.com/panxos/ConfServerDebian/main/panxos_logo.png" alt="Logo" width="200" height="200">
</p>

## 📊 Descripción

Ping-Monitor es una herramienta de línea de comandos desarrollada por Francisco Aravena (P4nx0z) para monitorear la latencia de red en tiempo real. Utiliza un sistema de semáforo visual para indicar el estado de la conexión y está disponible en dos versiones:

- 🔹 **Versión Básica**: Monitoreo simple y efectivo
- 🔷 **Versión Pro con Telegram**: Incluye notificaciones vía Telegram

## 🌟 Características

- Sistema de Semáforo visual (Verde, Amarillo, Rojo)
- Monitoreo continuo de latencia
- Estadísticas detalladas
- Logging opcional a archivo
- Configuración guardable y cifrada
- Notificaciones Telegram (versión Pro)

## 🖥️ Requisitos

- Python 3.6+
- pip (gestor de paquetes de Python)

## 📦 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/panxos/Ping-Monitor.git
   cd Ping-Monitor
   ```

2. Instala las dependencias:
   - Para la versión básica:
     ```bash
     pip install -r requirements_basic.txt
     ```
   - Para la versión Pro con Telegram:
     ```bash
     pip install -r requirements.txt
     ```

## 💻 Uso

### Versión Básica
```bash
python ping-monitor-script.py [host] [opciones]
```

### Versión Pro con Telegram
```bash
python ping-monitor-script-telegram.py [host] [opciones]
```

## 🔧 Opciones Disponibles

| Opción | Descripción | Valor por Defecto |
|--------|-------------|-------------------|
| `host` | IP o hostname a monitorear | (Requerido) |
| `--log` | Archivo de registro (opcional) | None |
| `--interval` | Intervalo entre pings (segundos) | 1 |
| `--yellow` | Umbral para semáforo amarillo (ms) | 100 |
| `--red` | Umbral para semáforo rojo (ms) | 300 |
| `--telegram_token` | Token del bot de Telegram | None |
| `--telegram_chat_id` | Chat ID de Telegram | None |
| `--save_config` | Guardar la configuración actual | False |

## 📊 Ejemplos de Uso

1. Monitoreo básico:
   ```bash
   python ping-monitor-script.py 8.8.8.8
   ```

2. Con logging y umbrales personalizados:
   ```bash
   python ping-monitor-script.py 8.8.8.8 --log ping_log.json --yellow 150 --red 400
   ```

3. Versión Pro con notificaciones Telegram:
   ```bash
   python ping-monitor-script-telegram.py 8.8.8.8 --telegram_token YOUR_TOKEN --telegram_chat_id YOUR_CHAT_ID --save_config
   ```

## 📄 Ejemplo de Salida de Log

Cuando se usa la opción `--log`, el archivo de log tendrá un formato JSON similar a este:

```json
{"timestamp": "2024-08-12T18:30:15.123456", "host": "8.8.8.8", "latency": 25.4}
{"timestamp": "2024-08-12T18:30:16.234567", "host": "8.8.8.8", "latency": 30.2}
{"timestamp": "2024-08-12T18:30:17.345678", "host": "8.8.8.8", "latency": 28.7}
```

## 🎨 Interpretación de Colores

- 🟢 **Verde**: Latencia normal (por debajo del umbral amarillo)
- 🟡 **Amarillo**: Latencia media (entre umbral amarillo y rojo)
- 🔴 **Rojo**: Latencia crítica (por encima del umbral rojo)

## 🔔 Configuración de Telegram (Versión Pro)

1. Crea un bot de Telegram con @BotFather y obtén el token.
2. Obtén tu Chat ID:
   - Envía un mensaje a tu bot.
   - Visita: `https://api.telegram.org/botTU_TOKEN/getUpdates`
   - Busca el "chat":{"id":XXXXXXXX} en la respuesta.

## 🛠️ Solución de Problemas

- **Error de módulo no encontrado**: Asegúrate de haber instalado todas las dependencias.
- **Problemas de permisos**: Verifica que tienes permisos para ejecutar ping en tu sistema.
- **Errores de Telegram**: Comprueba que el token y el chat ID son correctos.

## 📝 Notas Adicionales

- Para detener el monitoreo, usa Ctrl+C.
- La configuración se guarda cifrada para mayor seguridad.
- Los logs en formato JSON facilitan la integración con herramientas de análisis.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar Ping-Monitor, no dudes en abrir un issue o enviar un pull request.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

<p align="center">
  Desarrollado con ❤️ por Francisco Aravena (P4nx0z)
</p>
