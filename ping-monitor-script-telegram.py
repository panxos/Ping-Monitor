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
import psutil
from cryptography.fernet import Fernet

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CONFIG_FILE = 'config.json'
ENCRYPTION_KEY_FILE = 'encryption_key.key'

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

def log_event(message, log_file):
    """Registra un evento en el archivo de log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a') as f:
        f.write(f"{timestamp} - {message}\n")

def print_statistics(latencies):
    """Imprime estadísticas de latencia."""
    if not latencies:
        logger.warning("No hay datos suficientes para generar estadísticas.")
        return
    
    avg_latency = statistics.mean(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)
    std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0
    
    logger.info("\nEstadísticas finales:")
    logger.info(f"Promedio: {avg_latency:.1f} ms")
    logger.info(f"Máximo: {max_latency:.1f} ms")
    logger.info(f"Mínimo: {min_latency:.1f} ms")
    logger.info(f"Desviación estándar: {std_dev:.1f} ms")
    logger.info(f"Total de pings: {len(latencies)}")

async def send_telegram_message(token, chat_id, message):
    """Envía un mensaje a través de Telegram."""
    bot = Bot(token)
    await bot.send_message(chat_id=chat_id, text=message)

def notify_telegram(token, chat_id, message):
    """Notifica a través de Telegram de forma asíncrona."""
    asyncio.run(send_telegram_message(token, chat_id, message))

def main(host, log_file, interval, threshold_yellow, threshold_red, telegram_token, telegram_chat_id):
    """Función principal del script."""
    hostname = get_hostname()
    latencies = []
    last_state = 'green'
    network_down = False
    
    def signal_handler(sig, frame):
        logger.info("\nDeteniendo el monitoreo...")
        print_statistics(latencies)
        if telegram_token and telegram_chat_id:
            notify_telegram(telegram_token, telegram_chat_id, f"Monitoreo de red detenido en {hostname}.")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    logger.info(f"Iniciando monitoreo de {host} en {hostname}. Presiona Ctrl+C para detener.")
    if telegram_token and telegram_chat_id:
        notify_telegram(telegram_token, telegram_chat_id, f"Iniciando monitoreo de {host} en {hostname}")
    
    while True:
        ping_result = ping(host)
        latency = extract_time(ping_result)
        resources = get_system_resources()
        
        if latency is not None:
            latencies.append(latency)
            output = f"Ping a {host}: {latency:.1f} ms - CPU: {resources['cpu']}% - Memoria: {resources['memory']}% - Disco: {resources['disk']}%"
            
            if latency > threshold_red:
                print_colored(output, 'red')
                if last_state != 'red':
                    log_event(f"Semáforo en ROJO: Latencia crítica de {latency:.1f} ms", log_file)
                    if telegram_token and telegram_chat_id:
                        notify_telegram(telegram_token, telegram_chat_id, 
                                        f"ALERTA en {hostname}: Latencia crítica de {latency:.1f} ms\nCPU: {resources['cpu']}% - Memoria: {resources['memory']}% - Disco: {resources['disk']}%")
                    last_state = 'red'
            elif latency > threshold_yellow:
                print_colored(output, 'yellow')
                if last_state != 'yellow':
                    log_event(f"Semáforo en AMARILLO: Latencia media de {latency:.1f} ms", log_file)
                    if telegram_token and telegram_chat_id:
                        notify_telegram(telegram_token, telegram_chat_id, 
                                        f"Advertencia en {hostname}: Latencia media de {latency:.1f} ms\nCPU: {resources['cpu']}% - Memoria: {resources['memory']}% - Disco: {resources['disk']}%")
                    last_state = 'yellow'
            else:
                print_colored(output, 'green')
                if last_state != 'green':
                    log_event(f"Semáforo en VERDE: Latencia normal de {latency:.1f} ms", log_file)
                    if telegram_token and telegram_chat_id:
                        notify_telegram(telegram_token, telegram_chat_id, 
                                        f"Red normalizada en {hostname}: Latencia de {latency:.1f} ms\nCPU: {resources['cpu']}% - Memoria: {resources['memory']}% - Disco: {resources['disk']}%")
                    last_state = 'green'
            
            if network_down:
                log_event("La red se ha recuperado", log_file)
                if telegram_token and telegram_chat_id:
                    notify_telegram(telegram_token, telegram_chat_id, f"La red se ha recuperado en {hostname}")
                network_down = False
        else:
            logger.error(f"No se pudo obtener la latencia para {host}")
            log_event(f"Fallo al obtener latencia para {host}", log_file)
            if not network_down:
                log_event("La red se ha caído", log_file)
                if telegram_token and telegram_chat_id:
                    notify_telegram(telegram_token, telegram_chat_id, 
                                    f"ALERTA: La red se ha caído en {hostname}. No se puede alcanzar {host}\nCPU: {resources['cpu']}% - Memoria: {resources['memory']}% - Disco: {resources['disk']}%")
                network_down = True
        
        time.sleep(interval)

if __name__ == "__main__":
    config = load_config()
    
    parser = argparse.ArgumentParser(description="Monitor de red avanzado con sistema de semáforo y notificaciones Telegram")
    parser.add_argument("host", help="Dirección IP o nombre de host a monitorear")
    parser.add_argument("--log", default="network_monitor.log", help="Archivo de registro")
    parser.add_argument("--interval", type=float, default=1, help="Intervalo entre pings en segundos")
    parser.add_argument("--yellow", type=float, default=100, help="Umbral para semáforo amarillo (ms)")
    parser.add_argument("--red", type=float, default=300, help="Umbral para semáforo rojo (ms)")
    parser.add_argument("--telegram_token", help="Token del bot de Telegram")
    parser.add_argument("--telegram_chat_id", help="Chat ID de Telegram")
    parser.add_argument("--save_config", action="store_true", help="Guardar la configuración actual")
    
    args = parser.parse_args()
    
    if args.telegram_token:
        config['telegram_token'] = args.telegram_token
    if args.telegram_chat_id:
        config['telegram_chat_id'] = args.telegram_chat_id
    
    if args.save_config:
        save_config(config)
        logger.info("Configuración guardada.")
    
    telegram_token = config.get('telegram_token') or args.telegram_token
    telegram_chat_id = config.get('telegram_chat_id') or args.telegram_chat_id
    
    main(args.host, args.log, args.interval, args.yellow, args.red, telegram_token, telegram_chat_id)
