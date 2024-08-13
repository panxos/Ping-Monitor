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

### Dependencias

- **Versión Básica**:
  - `subprocess`
  - `re`
  - `sys`
  - `time`
  - `platform`
  - `argparse`
  - `datetime`
  - `statistics`
  - `signal`
  - `json`
  - `logging`

- **Versión Pro (adicionales)**:
  - `python-telegram-bot`
  - `cryptography`

## 📦 Instalación

### Debian/Ubuntu

1. Actualiza e instala las dependencias del sistema:
   ```bash
   sudo apt update
   sudo apt install python3-venv python3-pip
   ```

2. Clona el repositorio:
   ```bash
   git clone https://github.com/panxos/Ping-Monitor.git
   cd Ping-Monitor
   ```

3. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv ping_monitor_env
   source ping_monitor_env/bin/activate
   ```

4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt  # Para la versión Pro
   # O
   pip install -r requirements_basic.txt  # Para la versión básica
   ```

### Arch Linux

1. Instala Python y pip:
   ```bash
   sudo pacman -S python python-pip
   ```

2. Sigue los pasos 2-4 de la instalación para Debian/Ubuntu.

### Red Hat/Fedora

1. Instala Python y pip:
   ```bash
   sudo dnf install python3 python3-pip
   ```

2. Sigue los pasos 2-4 de la instalación para Debian/Ubuntu.

### macOS

1. Instala Homebrew si no lo tienes:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Instala Python:
   ```bash
   brew install python
   ```

3. Sigue los pasos 2-4 de la instalación para Debian/Ubuntu.

### Windows

1. Descarga e instala Python desde [python.org](https://www.python.org/downloads/).

2. Abre PowerShell y sigue estos pasos:
   ```powershell
   git clone https://github.com/panxos/Ping-Monitor.git
   cd Ping-Monitor
   python -m venv ping_monitor_env
   .\ping_monitor_env\Scripts\Activate.ps1
   pip install -r requirements.txt  # O requirements_basic.txt para la versión básica
   ```

## 💻 Uso

### Activar el entorno virtual (si no está activo):
```bash
source ping_monitor_env/bin/activate  # En Unix
# O
.\ping_monitor_env\Scripts\Activate.ps1  # En Windows PowerShell
```

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

4. Uso después de guardar la configuración:
   ```bash
   python ping-monitor-script-telegram.py 8.8.8.8
   ```
   (No es necesario proporcionar el token y chat ID de Telegram si ya se guardaron previamente)

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

- **Error de módulo no encontrado**: Asegúrate de haber activado el entorno virtual y de haber instalado todas las dependencias.
- **Problemas de permisos**: Verifica que tienes permisos para ejecutar ping en tu sistema. En algunos sistemas puede requerir privilegios de administrador.
- **Errores de Telegram**: Comprueba que el token y el chat ID son correctos y que el bot tiene permisos para enviar mensajes.
- **Problemas de conexión**: Asegúrate de tener una conexión a Internet activa y que no haya firewalls bloqueando las conexiones salientes.

## 📝 Notas Adicionales

- Para detener el monitoreo, usa Ctrl+C.
- La configuración se guarda cifrada para mayor seguridad.
- Los logs en formato JSON facilitan la integración con herramientas de análisis como Grafana o ELK Stack.
- En sistemas basados en Debian, es crucial usar el entorno virtual para evitar conflictos con los paquetes del sistema.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar Ping-Monitor, no dudes en abrir un issue o enviar un pull request.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

<p align="center">
  Desarrollado con ❤️ por Francisco Aravena (P4nx0z)
</p>
