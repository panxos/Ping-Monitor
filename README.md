# 🌐 Ping-Monitor: Monitoreo de Red con Sistema de Semáforo

<p align="center">
  <img src="https://raw.githubusercontent.com/panxos/ConfServerDebian/main/panxos_logo.png" alt="Logo" width="200" height="200">
</p>

## 📊 Descripción

Ping-Monitor es una herramienta de línea de comandos desarrollada por Francisco Aravena (P4nx0z) para monitorear la latencia de red en tiempo real. Utiliza un sistema de semáforo visual para indicar el estado de la conexión y ofrece la opción de enviar notificaciones a través de Telegram.

## 🌟 Características

- **Sistema de Semáforo**: Visualización de la latencia en colores verde, amarillo y rojo.
- **Monitoreo Continuo**: Realiza pings constantes a un host especificado.
- **Alertas Auditivas**: Emite un sonido cuando la latencia alcanza niveles críticos.
- **Registro de Eventos**: Guarda los cambios significativos en un archivo de log.
- **Estadísticas Finales**: Muestra un resumen estadístico al finalizar el monitoreo.
- **Traceroute Opcional**: Capacidad de ejecutar un traceroute al finalizar el monitoreo.
- **Notificaciones Telegram** (versión avanzada): Envía alertas a través de Telegram.

## 🖥️ Compatibilidad

- Windows
- macOS
- Linux

## 📚 Dependencias

- Python 3.6+
- Para la versión con Telegram: `python-telegram-bot`

## 🚀 Instalación

1. Clona el repositorio:
   ```
   git clone https://github.com/panxos/Ping-Monitor.git
   ```
2. Navega al directorio del proyecto:
   ```
   cd Ping-Monitor
   ```
3. (Opcional) Para la versión con Telegram, instala la dependencia:
   ```
   pip install python-telegram-bot
   ```

## 💻 Uso

### Versión Básica

```
python ping-monitor-script.py [host] [opciones]
```

### Versión con Telegram

```
python ping-monitor-script-telegram.py [host] [opciones]
```

### Opciones Comunes:

- `host`: Dirección IP o nombre de host a monitorear (obligatorio)
- `--log`: Nombre del archivo de registro (por defecto: "network_monitor.log")
- `--interval`: Intervalo entre pings en segundos (por defecto: 1)
- `--yellow`: Umbral para la alerta amarilla en ms (por defecto: 100)
- `--red`: Umbral para la alerta roja en ms (por defecto: 300)
- `--tracer`: Ejecutar traceroute al finalizar el monitoreo

### Opciones Adicionales para la Versión con Telegram:

- `--telegram_token`: Token del bot de Telegram
- `--telegram_chat_id`: ID del chat de Telegram para recibir notificaciones

## 🔧 Configuración de Telegram (para la versión avanzada)

1. Crea un bot de Telegram con @BotFather y obtén el token.
2. Obtén tu Chat ID:
   - Envía un mensaje a tu bot.
   - Visita: `https://api.telegram.org/botTU_TOKEN/getUpdates`
   - Busca el "chat":{"id":XXXXXXXX} en la respuesta.
3. Usa el token y el chat ID como argumentos al ejecutar el script.

## 📊 Interpretación de Resultados

- **Verde**: Latencia normal (< 100 ms por defecto)
- **Amarillo**: Latencia media (100-300 ms por defecto)
- **Rojo**: Latencia crítica (> 300 ms por defecto)

## 📝 Ejemplos de Uso

### Versión Básica:
```
python ping-monitor-script.py 8.8.8.8 --interval 2 --yellow 150 --red 400
```

### Versión con Telegram:
```
python ping-monitor-script-telegram.py 8.8.8.8 --telegram_token YOUR_TOKEN --telegram_chat_id YOUR_CHAT_ID
```

## 🛠️ Personalización

Ajusta los umbrales de latencia y el intervalo de ping según tus necesidades usando las opciones de línea de comandos.

## 🚪 Finalizar el Monitoreo

Presiona `Ctrl+C` para detener el monitoreo. Se mostrará un resumen estadístico y, si se especificó, se ejecutará un traceroute.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar Ping-Monitor, no dudes en abrir un issue o enviar un pull request.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

<p align="center">
  Desarrollado con ❤️ por Francisco Aravena (P4nx0z)
</p>
