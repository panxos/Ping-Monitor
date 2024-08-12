# 🌐 Ping-Monitor: Monitoreo de Red con Sistema de Semáforo

<p align="center">
  <img src="https://raw.githubusercontent.com/panxos/ConfServerDebian/main/panxos_logo.png" alt="Logo" width="200" height="200">
</p>

## 📊 Descripción

Ping-Monitor es una herramienta de línea de comandos desarrollada por Francisco Aravena (P4nx0z) para monitorear la latencia de red en tiempo real. Utiliza un sistema de semáforo visual en la consola del servidor y ofrece notificaciones selectivas vía Telegram.

## 🌟 Características

- Sistema de Semáforo visual en consola
- Monitoreo continuo de latencia
- Notificaciones selectivas vía Telegram (versión Pro)
- Configuración cifrada y guardado de configuraciones

## 🖥️ Compatibilidad

- Windows
- macOS
- Linux (incluyendo Debian)

## 📦 Instalación

### Preparación del Entorno (Especialmente para Debian)

Debido a las políticas de gestión de paquetes en Debian, se recomienda usar un entorno virtual:

```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv ping_monitor_env
source ping_monitor_env/bin/activate
```

### Instalación de Dependencias

1. Clona el repositorio:
   ```bash
   git clone https://github.com/panxos/Ping-Monitor.git
   cd Ping-Monitor
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Uso

```bash
python ping-monitor-script-telegram.py [host] [opciones]
```

## 🔧 Opciones Disponibles

| Opción | Descripción | Valor por Defecto |
|--------|-------------|-------------------|
| `host` | IP o hostname a monitorear | (Requerido) |
| `--log` | Archivo de registro | network_monitor.log |
| `--interval` | Intervalo entre pings (seg) | 1 |
| `--yellow` | Umbral amarillo (ms) | 100 |
| `--red` | Umbral rojo (ms) | 300 |
| `--telegram_token` | Token del bot de Telegram | |
| `--telegram_chat_id` | ID del chat de Telegram | |
| `--save_config` | Guardar la configuración actual | |

## 💾 Guardado y Uso de Configuración

Para guardar la configuración:

```bash
python ping-monitor-script-telegram.py 8.8.8.8 --telegram_token YOUR_TOKEN --telegram_chat_id YOUR_CHAT_ID --save_config
```

Para usar la configuración guardada:

```bash
python ping-monitor-script-telegram.py 8.8.8.8
```

## 🎨 Visualización y Notificaciones

- **Consola**: Muestra constantemente el estado de la latencia con colores.
- **Telegram**: Envía notificaciones solo en los siguientes casos:
  1. Al iniciar el monitoreo
  2. Cuando se supera un umbral (amarillo o rojo)
  3. Cuando la latencia se recupera a verde

## 🚦 Interpretación de Colores

- 🟢 **Verde**: Latencia normal (por debajo del umbral amarillo)
- 🟡 **Amarillo**: Latencia media (entre umbral amarillo y rojo)
- 🔴 **Rojo**: Latencia crítica (por encima del umbral rojo)

## 🔔 Configuración de Telegram

1. Crea un bot de Telegram con @BotFather
2. Obtén tu Chat ID:
   - Envía un mensaje a tu bot
   - Visita: `https://api.telegram.org/botTU_TOKEN/getUpdates`
   - Busca el "chat":{"id":XXXXXXXX} en la respuesta

## 🛠️ Solución de Problemas

### Error en Debian: "externally-managed-environment"

Si encuentras este error, usa el entorno virtual como se describe en la sección de instalación.

## 📝 Notas Adicionales

- Para salir del script, presiona Ctrl+C. Se mostrarán las estadísticas finales.
- La configuración de Telegram se guarda de forma segura y cifrada.
- Asegúrate de tener permisos adecuados para ejecutar pings en tu sistema.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar Ping-Monitor, no dudes en abrir un issue o enviar un pull request.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

<p align="center">
  Desarrollado con ❤️ por Francisco Aravena (P4nx0z)
</p>
