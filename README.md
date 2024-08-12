# 🌐 Ping-Monitor con Sistema de Semáforo

<p align="center">
  <img src="https://raw.githubusercontent.com/panxos/ConfServerDebian/main/panxos_logo.png" alt="Logo" width="200" height="200">
</p>

## 📊 Descripción

Ping-Monitor es un script de Python que proporciona un monitor de red en tiempo real con un sistema de semáforo visual. Diseñado por Francisco Aravena (P4nx0z) para administradores de sistemas y entusiastas de la red, este monitor ofrece una forma sencilla y efectiva de vigilar la latencia de red y detectar problemas de conectividad.

## 🌟 Características

- **Sistema de Semáforo**: Visualización de la latencia en colores verde, amarillo y rojo.
- **Monitoreo Continuo**: Realiza pings constantes a un host especificado.
- **Alertas Auditivas**: Emite un sonido cuando la latencia alcanza niveles críticos.
- **Registro de Eventos**: Guarda los cambios significativos en un archivo de log.
- **Estadísticas Finales**: Muestra un resumen estadístico al finalizar el monitoreo.
- **Traceroute Opcional**: Capacidad de ejecutar un traceroute al finalizar el monitoreo.

## 🖥️ Compatibilidad

Ping-Monitor es compatible con los siguientes sistemas operativos:
- Windows
- macOS
- Linux

## 📚 Dependencias

Ping-Monitor utiliza las siguientes bibliotecas de Python:
- `subprocess`
- `re`
- `sys`
- `time`
- `platform`
- `argparse`
- `datetime`
- `statistics`
- `signal`

Todas estas bibliotecas son parte de la biblioteca estándar de Python, por lo que no se requiere instalación adicional.

## 🚀 Instalación y Uso

### Opción 1: Clonar el repositorio

1. Clona este repositorio:
   ```
   git clone https://github.com/panxos/Ping-Monitor.git
   ```
2. Navega al directorio del proyecto:
   ```
   cd Ping-Monitor
   ```
3. Ejecuta el script:
   ```
   python ping-monitor-script.py [host] [opciones]
   ```

### Opción 2: Ejecución al vuelo

Puedes ejecutar el script directamente sin clonar el repositorio usando `curl` y `python`:

```bash
curl -s https://raw.githubusercontent.com/panxos/Ping-Monitor/main/ping-monitor-script.py | python - [host] [opciones]
```

Nota: Asegúrate de tener `curl` instalado en tu sistema para usar esta opción.

### Opciones:

- `host`: Dirección IP o nombre de host a monitorear (obligatorio)
- `--log`: Nombre del archivo de registro (por defecto: "network_monitor.log")
- `--interval`: Intervalo entre pings en segundos (por defecto: 1)
- `--yellow`: Umbral para la alerta amarilla en ms (por defecto: 100)
- `--red`: Umbral para la alerta roja en ms (por defecto: 300)
- `--tracer`: Ejecutar traceroute al finalizar el monitoreo

### Ejemplo:

```
python ping-monitor-script.py 8.8.8.8 --log mi_monitoreo.log --interval 2 --yellow 150 --red 400 --tracer
```

## 📈 Interpretación de Resultados

- **Verde**: Latencia normal (por debajo del umbral amarillo)
- **Amarillo**: Latencia media (entre el umbral amarillo y rojo)
- **Rojo**: Latencia crítica (por encima del umbral rojo)

El script emitirá un sonido cuando la latencia alcance el nivel rojo.

## 🛠️ Personalización

Puedes ajustar los umbrales de latencia y el intervalo de ping según tus necesidades específicas utilizando las opciones de línea de comandos.

## 📝 Registro

El script genera un archivo de log que registra los cambios significativos en la latencia. Esto es útil para el análisis posterior y la detección de patrones a largo plazo.

## 🚪 Salida

Para detener el monitoreo, presiona `Ctrl+C`. El script mostrará un resumen estadístico y, si se especificó la opción `--tracer`, ejecutará un traceroute final.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar Ping-Monitor, no dudes en abrir un issue o enviar un pull request.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

<p align="center">
  Desarrollado con ❤️ por Francisco Aravena (P4nx0z)
</p>
