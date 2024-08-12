import subprocess
import re
import sys
import time
import platform
import argparse
from datetime import datetime
import statistics
import signal
import asyncio
from telegram import Bot
import os
import json
import socket
import logging
import gettext
import psutil
from cryptography.fernet import Fernet

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CONFIG_FILE = 'config.json'
ENCRYPTION_KEY_FILE = 'encryption_key.key'

# Configuración de internacionalización
_ = gettext.gettext
LOCALE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locales')
if os.path.exists(LOCALE_DIR):
    try:
        t = gettext.translation('ping_monitor', LOCALE_DIR, fallback=True)
        _ = t.gettext
    except Exception as e:
        logger.warning(f"No se pudo cargar la traducción: {e}")

def generate_key():
    """Genera una clave de cifrado y la guarda en un archivo."""
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    """Carga la clave de cifrado desde el archivo."""
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        generate_key()
    with open(ENCRYPTION_KEY_FILE, 'rb') as key_file:
        return key_file.read()

def encrypt_data(data):
    """Cifra los datos sensibles."""
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    """Descifra los datos sensibles."""
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

def load_config():
    """Carga la configuración desde el archivo JSON."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        if 'telegram_token' in config:
            config['telegram_token'] = decrypt_data(config['telegram_token'])
        return config
    return {}

def save_config(config):
    """Guarda la configuración en el archivo JSON, cifrando datos sensibles."""
    config_to_save = config.copy()
    if 'telegram_token' in config_to_save:
        config_to_save['telegram_token'] = encrypt_data(config_to_save['telegram_token'])
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_to_save, f, indent=2)

def get_system_resources():
    """Obtiene información sobre el uso de recursos del sistema."""
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        'cpu': cpu_percent,
        'memory': memory.percent,
        'disk': disk.percent
    }

def get_hostname():
    """Obtiene el nombre del host."""
    return socket.gethostname()

def ping(host):
    """Realiza un ping al host especificado."""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def extract_time(ping_output):
    """Extrae el tiempo de latencia del resultado del ping."""
    match = re.search(r'time=(\d+(\.\d+)?)', ping_output)
    return float(match.group(1)) if match else None

def print_colored(text, color):
    """Imprime texto coloreado en la consola."""
    colors = {
        'reset': '\033[0m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m'
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")

def beep():
    """Genera un sonido de alerta."""
    if platform.system().lower() == 'windows':
        import winsound
        winsound.Beep(1000, 500)
    else:
        print('\a', end='', flush=True)

def log_event(message, log_file):
    """Registra un evento en el archivo de log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a') as f:
        f.write(f"{timestamp} - {message}\n")

def traceroute(host):
    """Realiza un traceroute al host especificado."""
    if platform.system().lower() == 'windows':
        command = ['tracert', host]
    else:
        command = ['traceroute', host]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def print_statistics(latencies):
    """Imprime estadísticas de latencia."""
    if not latencies:
        logger.warning(_("No hay datos suficientes para generar estadísticas."))
        return
    
    avg_latency = statistics.mean(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)
    std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0
    
    logger.info(_("\nEstadísticas finales:"))
    logger.info(_("Promedio: {:.1f} ms").format(avg_latency))
    logger.info(_("Máximo: {:.1f} ms").format(max_latency))
    logger.info(_("Mínimo: {:.1f} ms").format(min_latency))
    logger.info(_("Desviación estándar: {:.1f} ms").format(std_dev))
    logger.info(_("Total de pings: {}").format(len(latencies)))

async def send_telegram_message(token, chat_id, message):
    """Envía un mensaje a través de Telegram."""
    bot = Bot(token)
    await bot.send_message(chat_id=chat_id, text=message)

def notify_telegram(token, chat_id, message):
    """Notifica a través de Telegram de forma asíncrona."""
    asyncio.run(send_telegram_message(token, chat_id, message))

def main(host, log_file, interval, threshold_yellow, threshold_red, do_traceroute, telegram_token, telegram_chat_id):
    """Función principal del script."""
    hostname = get_hostname()
    latencies = []
    last_state = 'green'
    network_down = False
    
    def signal_handler(sig, frame):
        logger.info(_("\nDeteniendo el monitoreo..."))
        print_statistics(latencies)
        if do_traceroute:
            logger.info(_("\nEjecutando traceroute final:"))
            logger.info(traceroute(host))
        if telegram_token and telegram_chat_id:
            notify_telegram(telegram_token, telegram_chat_id, _("Monitoreo de red detenido en {}").format(hostname))
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    logger.info(_("Iniciando monitoreo de {} en {}. Presiona Ctrl+C para detener.").format(host, hostname))
    if telegram_token and telegram_chat_id:
        notify_telegram(telegram_token, telegram_chat_id, _("Iniciando monitoreo de {} en {}").format(host, hostname))
    
    while True:
        ping_result = ping(host)
        latency = extract_time(ping_result)
        resources = get_system_resources()
        
        if latency is not None:
            latencies.append(latency)
            output = _("Ping a {}: {:.1f} ms - CPU: {}% - Memoria: {}% - Disco: {}%").format(
                host, latency, resources['cpu'], resources['memory'], resources['disk'])
            
            if latency > threshold_red:
                print_colored(output, 'red')
                beep()
                if last_state != 'red':
                    log_event(_("Semáforo en ROJO: Latencia crítica de {:.1f} ms").format(latency), log_file)
                    if telegram_token and telegram_chat_id:
                        notify_telegram(telegram_token, telegram_chat_id, 
                                        _("ALERTA en {}: Latencia crítica de {:.1f} ms\nCPU: {}% - Memoria: {}% - Disco: {}%").format(
                                            hostname, latency, resources['cpu'], resources['memory'], resources['disk']))
                    last_state = 'red'
            elif latency > threshold_yellow:
                print_colored(output, 'yellow')
                if last_state != 'yellow':
                    log_event(_("Semáforo en AMARILLO: Latencia media de {:.1f} ms").format(latency), log_file)
                    if telegram_token and telegram_chat_id:
                        notify_telegram(telegram_token, telegram_chat_id, 
                                        _("Advertencia en {}: Latencia media de {:.1f} ms\nCPU: {}% - Memoria: {}% - Disco: {}%").format(
                                            hostname, latency, resources['cpu'], resources['memory'], resources['disk']))
                    last_state = 'yellow'
            else:
                print_colored(output, 'green')
                if last_state != 'green':
                    log_event(_("Semáforo en VERDE: Latencia normal de {:.1f} ms").format(latency), log_file)
                    if telegram_token and telegram_chat_id:
                        notify_telegram(telegram_token, telegram_chat_id, 
                                        _("Red normalizada en {}: Latencia de {:.1f} ms\nCPU: {}% - Memoria: {}% - Disco: {}%").format(
                                            hostname, latency, resources['cpu'], resources['memory'], resources['disk']))
                    last_state = 'green'
            
            if network_down:
                log_event(_("La red se ha recuperado"), log_file)
                if telegram_token and telegram_chat_id:
                    notify_telegram(telegram_token, telegram_chat_id, _("La red se ha recuperado en {}").format(hostname))
                network_down = False
        else:
            logger.error(_("No se pudo obtener la latencia para {}").format(host))
            log_event(_("Fallo al obtener latencia para {}").format(host), log_file)
            if not network_down:
                log_event(_("La red se ha caído"), log_file)
                if telegram_token and telegram_chat_id:
                    notify_telegram(telegram_token, telegram_chat_id, 
                                    _("ALERTA: La red se ha caído en {}. No se puede alcanzar {}\nCPU: {}% - Memoria: {}% - Disco: {}%").format(
                                        hostname, host, resources['cpu'], resources['memory'], resources['disk']))
                network_down = True
        
        time.sleep(interval)

if __name__ == "__main__":
    config = load_config()
    
    parser = argparse.ArgumentParser(description=_("Monitor de red avanzado con sistema de semáforo y notificaciones Telegram"))
    parser.add_argument("host", help=_("Dirección IP o nombre de host a monitorear"))
    parser.add_argument("--log", default="network_monitor.log", help=_("Archivo de registro"))
    parser.add_argument("--interval", type=float, default=1, help=_("Intervalo entre pings en segundos"))
    parser.add_argument("--yellow", type=float, default=100, help=_("Umbral para semáforo amarillo (ms)"))
    parser.add_argument("--red", type=float, default=300, help=_("Umbral para semáforo rojo (ms)"))
    parser.add_argument("--tracer", action="store_true", help=_("Ejecutar traceroute al finalizar"))
    parser.add_argument("--telegram_token", help=_("Token del bot de Telegram"))
    parser.add_argument("--telegram_chat_id", help=_("Chat ID de Telegram"))
    parser.add_argument("--save_config", action="store_true", help=_("Guardar la configuración actual"))
    
    args = parser.parse_args()
    
    if args.telegram_token:
        config['telegram_token'] = args.telegram_token
    if args.telegram_chat_id:
        config['telegram_chat_id'] = args.telegram_chat_id
    
    if args.save_config:
        save_config(config)
        logger.info(_("Configuración guardada."))
    
    telegram_token = config.get('telegram_token') or args.telegram_token
    telegram_chat_id = config.get('telegram_chat_id') or args.telegram_chat_id
    
    main(args.host, args.log, args.interval, args.yellow, args.red, args.tracer, telegram_token, telegram_chat_id)
