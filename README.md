# 🌐 Ping-Monitor: Monitoreo de Red con Sistema de Semáforo

<p align="center">
  <img src="https://raw.githubusercontent.com/panxos/ConfServerDebian/main/panxos_logo.png" alt="Logo" width="200" height="200">
</p>

## 📊 Descripción

Ping-Monitor es una herramienta de línea de comandos desarrollada por Francisco Aravena (P4nx0z) para monitorear la latencia de red en tiempo real. Utiliza un sistema de semáforo visual para indicar el estado de la conexión y está disponible en dos versiones:

- 🔹 **Versión Básica**: Monitoreo simple y efectivo
- 🔷 **Versión Pro con Telegram**: Notificaciones avanzadas + Monitoreo de recursos del sistema

## 🌟 Características

### Versión Básica
- Sistema de Semáforo visual
- Monitoreo continuo de latencia
- Registro de eventos
- Estadísticas de latencia

### Versión Pro (Incluye todo lo anterior más)
- Notificaciones vía Telegram
- Monitoreo de recursos del sistema (CPU, Memoria, Disco)
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

### Opciones Comunes

| Opción | Descripción | Valor por Defecto |
|--------|-------------|-------------------|
| `host` | IP o hostname a monitorear | (Requerido) |
| `--log` | Archivo de registro | network_monitor.log |
| `--interval` | Intervalo entre pings (seg) | 1 |
| `--yellow` | Umbral amarillo (ms) | 100 |
| `--red` | Umbral rojo (ms) | 300 |

### Opciones Adicionales (Versión Pro)

| Opción | Descripción |
|--------|-------------|
| `--telegram_token` | Token del bot de Telegram |
| `--telegram_chat_id` | ID del chat de Telegram |
| `--save_config` | Guardar la configuración actual en un archivo |

## 💾 Guardado y Uso de Configuración (Versión Pro)

La versión Pro permite guardar y cargar configuraciones, facilitando el uso repetido sin tener que ingresar el token de Telegram y el chat ID cada vez.

### Guardando la Configuración

```bash
python ping-monitor-script-telegram.py 8.8.8.8 --telegram_token YOUR_TOKEN --telegram_chat_id YOUR_CHAT_ID --save_config
```

Esto crea un archivo `config.json` cifrado en el directorio del script.

### Usando la Configuración Guardada

Una vez guardada la configuración, ejecuta el script sin especificar el token y el chat ID:

```bash
python ping-monitor-script-telegram.py 8.8.8.8
```

### Actualizando la Configuración

Para actualizar, ejecuta el script con los nuevos valores y la opción `--save_config`.

### Seguridad

- La configuración se guarda cifrada para proteger tu token de Telegram.
- La clave de cifrado se almacena en `encryption_key.key`. Mantén este archivo seguro.

**Nota**: Ten cuidado con los archivos de configuración y la clave de cifrado en entornos compartidos.

## 📊 Ejemplos de Uso

### Versión Básica
```bash
python ping-monitor-script.py 8.8.8.8 --interval 2 --yellow 150 --red 400
```

### Versión Pro con Telegram
```bash
python ping-monitor-script-telegram.py 8.8.8.8 --telegram_token YOUR_TOKEN --telegram_chat_id YOUR_CHAT_ID --save_config
```

## 🎨 Interpretación de Colores

- 🟢 **Verde**: Latencia normal (por debajo del umbral amarillo)
- 🟡 **Amarillo**: Latencia media (entre umbral amarillo y rojo)
- 🔴 **Rojo**: Latencia crítica (por encima del umbral rojo)

## 🔔 Configuración de Telegram (Versión Pro)

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
- La versión Pro guarda la configuración de Telegram de forma segura y cifrada.
- Asegúrate de tener permisos adecuados para ejecutar pings en tu sistema.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar Ping-Monitor, no dudes en abrir un issue o enviar un pull request.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

<p align="center">
  Desarrollado con ❤️ por Francisco Aravena (P4nx0z)
</p>
