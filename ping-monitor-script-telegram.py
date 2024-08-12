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
from cryptography.fernet import Fernet

# Configuración global
CONFIG_FILE = 'config.json'
ENCRYPTION_KEY_FILE = 'encryption_key.key'

def print_info():
    print("\033[1;32mPing-Monitor creado por P4nx0z\033[0m")
    print("\033[1;34mGitHub: https://github.com/panxos\033[0m")
    print()

def setup_logging(log_file=None):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_formatter = logging.Formatter('%(message)s')
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger

def generate_key():
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        generate_key()
    with open(ENCRYPTION_KEY_FILE, 'rb') as key_file:
        return key_file.read()

def encrypt_data(data):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        if 'telegram_token' in config:
            config['telegram_token'] = decrypt_data(config['telegram_token'])
        return config
    return {}

def save_config(config):
    config_to_save = config.copy()
    if 'telegram_token' in config_to_save:
        config_to_save['telegram_token'] = encrypt_data(config_to_save['telegram_token'])
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_to_save, f, indent=2)

def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        return result.stdout
    except subprocess.TimeoutExpired:
        return None

def extract_time(ping_output):
    if ping_output is None:
        return None
    match = re.search(r'time=(\d+(\.\d+)?)', ping_output)
    return float(match.group(1)) if match else None

def print_colored(text, color):
    colors = {
        'reset': '\033[0m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m'
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")

async def send_telegram_message(token, chat_id, message):
    bot = Bot(token)
    await bot.send_message(chat_id=chat_id, text=message)

def notify_telegram(token, chat_id, message):
    asyncio.run(send_telegram_message(token, chat_id, message))

def print_statistics(latencies):
    if not latencies:
        logging.warning("No hay datos suficientes para generar estadísticas.")
        return
    
    avg_latency = statistics.mean(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)
    std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0
    
    logging.info("\nEstadísticas finales:")
    logging.info(f"Promedio: {avg_latency:.1f} ms")
    logging.info(f"Máximo: {max_latency:.1f} ms")
    logging.info(f"Mínimo: {min_latency:.1f} ms")
    logging.info(f"Desviación estándar: {std_dev:.1f} ms")
    logging.info(f"Total de pings: {len(latencies)}")

def main(host, log_file, interval, threshold_yellow, threshold_red, telegram_token, telegram_chat_id):
    hostname = socket.gethostname()
    latencies = []
    last_state = 'green'
    
    def signal_handler(sig, frame):
        print("\nDeteniendo el monitoreo...")
        print_statistics(latencies)
        if telegram_token and telegram_chat_id:
            try:
                notify_telegram(telegram_token, telegram_chat_id, f"Monitoreo de red detenido en {hostname}.")
            except Exception as e:
                logging.error(f"No se pudo enviar notificación de finalización: {e}")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    logging.info(f"Iniciando monitoreo de {host} en {hostname}. Presiona Ctrl+C para detener.")
    if telegram_token and telegram_chat_id:
        try:
            notify_telegram(telegram_token, telegram_chat_id, f"Iniciando monitoreo de {host} en {hostname}")
        except Exception as e:
            logging.error(f"No se pudo enviar notificación inicial: {e}")
    
    while True:
        try:
            ping_result = ping(host)
            latency = extract_time(ping_result)
            
            if latency is not None:
                latencies.append(latency)
                log_data = {
                    "host": host,
                    "latency": latency,
                    "timestamp": datetime.now().isoformat()
                }
                if log_file:
                    logging.info(json.dumps(log_data))
                
                if latency > threshold_red:
                    print_colored(f"Ping a {host}: {latency:.1f} ms", 'red')
                    if last_state != 'red':
                        if telegram_token and telegram_chat_id:
                            try:
                                notify_telegram(telegram_token, telegram_chat_id, 
                                                f"ALERTA en {hostname}: Latencia crítica de {latency:.1f} ms")
                            except Exception as e:
                                logging.error(f"No se pudo enviar notificación de alerta roja: {e}")
                        last_state = 'red'
                elif latency > threshold_yellow:
                    print_colored(f"Ping a {host}: {latency:.1f} ms", 'yellow')
                    if last_state == 'green':
                        if telegram_token and telegram_chat_id:
                            try:
                                notify_telegram(telegram_token, telegram_chat_id, 
                                                f"Advertencia en {hostname}: Latencia media de {latency:.1f} ms")
                            except Exception as e:
                                logging.error(f"No se pudo enviar notificación de advertencia: {e}")
                        last_state = 'yellow'
                else:
                    print_colored(f"Ping a {host}: {latency:.1f} ms", 'green')
                    if last_state != 'green':
                        if telegram_token and telegram_chat_id:
                            try:
                                notify_telegram(telegram_token, telegram_chat_id, 
                                                f"Red normalizada en {hostname}: Latencia de {latency:.1f} ms")
                            except Exception as e:
                                logging.error(f"No se pudo enviar notificación de normalización: {e}")
                        last_state = 'green'
            else:
                print(f"No se pudo obtener la latencia para {host}")
                if telegram_token and telegram_chat_id:
                    try:
                        notify_telegram(telegram_token, telegram_chat_id, 
                                        f"ALERTA en {hostname}: No se pudo obtener la latencia para {host}")
                    except Exception as e:
                        logging.error(f"No se pudo enviar notificación de fallo de ping: {e}")
            
            time.sleep(interval)
        except Exception as e:
            logging.error(f"Error durante el monitoreo: {e}")
            time.sleep(interval)  # Espera antes de intentar de nuevo

def run_monitor():
    config = load_config()
    
    parser = argparse.ArgumentParser(description="Monitor de red avanzado con sistema de semáforo y notificaciones Telegram")
    parser.add_argument("host", help="Dirección IP o nombre de host a monitorear")
    parser.add_argument("--log", help="Archivo de registro (opcional)")
    parser.add_argument("--interval", type=float, default=1, help="Intervalo entre pings en segundos")
    parser.add_argument("--yellow", type=float, default=100, help="Umbral para semáforo amarillo (ms)")
    parser.add_argument("--red", type=float, default=300, help="Umbral para semáforo rojo (ms)")
    parser.add_argument("--telegram_token", help="Token del bot de Telegram")
    parser.add_argument("--telegram_chat_id", help="Chat ID de Telegram")
    parser.add_argument("--save_config", action="store_true", help="Guardar la configuración actual")
    
    args = parser.parse_args()
    
    setup_logging(args.log)
    
    if args.telegram_token:
        config['telegram_token'] = args.telegram_token
    if args.telegram_chat_id:
        config['telegram_chat_id'] = args.telegram_chat_id
    
    if args.save_config:
        save_config(config)
        logging.info("Configuración guardada.")
    
    telegram_token = config.get('telegram_token') or args.telegram_token
    telegram_chat_id = config.get('telegram_chat_id') or args.telegram_chat_id
    
    try:
        main(args.host, args.log, args.interval, args.yellow, args.red, telegram_token, telegram_chat_id)
    except KeyboardInterrupt:
        logging.info("Monitoreo detenido por el usuario.")
    except Exception as e:
        logging.error(f"Error inesperado: {e}", exc_info=True)
        if telegram_token and telegram_chat_id:
            try:
                notify_telegram(telegram_token, telegram_chat_id, f"Error inesperado en el monitor de red: {e}")
            except Exception as te:
                logging.error(f"No se pudo enviar notificación de error inesperado: {te}")
    finally:
        logging.info("Finalizando el programa.")

if __name__ == "__main__":
    print_info()
    run_monitor()