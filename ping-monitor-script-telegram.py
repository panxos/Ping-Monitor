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

# ... [Mantener las funciones de cifrado y configuración como estaban] ...

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

async def send_telegram_message(token, chat_id, message):
    """Envía un mensaje a través de Telegram."""
    bot = Bot(token)
    await bot.send_message(chat_id=chat_id, text=message)

def notify_telegram(token, chat_id, message):
    """Notifica a través de Telegram de forma asíncrona."""
    asyncio.run(send_telegram_message(token, chat_id, message))

def main(host, log_file, interval, threshold_yellow, threshold_red, telegram_token, telegram_chat_id):
    """Función principal del script."""
    hostname = socket.gethostname()
    latencies = []
    last_state = 'green'
    
    def signal_handler(sig, frame):
        print("\nDeteniendo el monitoreo...")
        print_statistics(latencies)
        if telegram_token and telegram_chat_id:
            notify_telegram(telegram_token, telegram_chat_id, f"Monitoreo de red detenido en {hostname}.")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"Iniciando monitoreo de {host} en {hostname}. Presiona Ctrl+C para detener.")
    if telegram_token and telegram_chat_id:
        notify_telegram(telegram_token, telegram_chat_id, f"Iniciando monitoreo de {host} en {hostname}")
    
    while True:
        ping_result = ping(host)
        latency = extract_time(ping_output)
        
        if latency is not None:
            latencies.append(latency)
            output = f"Ping a {host}: {latency:.1f} ms"
            
            if latency > threshold_red:
                print_colored(output, 'red')
                if last_state != 'red':
                    if telegram_token and telegram_chat_id:
                        notify_telegram(telegram_token, telegram_chat_id, 
                                        f"ALERTA en {hostname}: Latencia crítica de {latency:.1f} ms")
                    last_state = 'red'
            elif latency > threshold_yellow:
                print_colored(output, 'yellow')
                if last_state == 'green':
                    if telegram_token and telegram_chat_id:
                        notify_telegram(telegram_token, telegram_chat_id, 
                                        f"Advertencia en {hostname}: Latencia media de {latency:.1f} ms")
                    last_state = 'yellow'
            else:
                print_colored(output, 'green')
                if last_state != 'green':
                    if telegram_token and telegram_chat_id:
                        notify_telegram(telegram_token, telegram_chat_id, 
                                        f"Red normalizada en {hostname}: Latencia de {latency:.1f} ms")
                    last_state = 'green'
        else:
            print(f"No se pudo obtener la latencia para {host}")
        
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
        print("Configuración guardada.")
    
    telegram_token = config.get('telegram_token') or args.telegram_token
    telegram_chat_id = config.get('telegram_chat_id') or args.telegram_chat_id
    
    main(args.host, args.log, args.interval, args.yellow, args.red, telegram_token, telegram_chat_id)
