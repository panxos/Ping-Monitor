import subprocess
import re
import sys
import time
import platform
import argparse
from datetime import datetime
import statistics
import signal

# Configuración de logging básico
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

def main(host, log_file, interval, threshold_yellow, threshold_red):
    """Función principal del script."""
    latencies = []
    last_state = 'green'
    
    def signal_handler(sig, frame):
        logger.info("\nDeteniendo el monitoreo...")
        print_statistics(latencies)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    logger.info(f"Iniciando monitoreo de {host}. Presiona Ctrl+C para detener.")
    
    while True:
        ping_result = ping(host)
        latency = extract_time(ping_result)
        
        if latency is not None:
            latencies.append(latency)
            output = f"Ping a {host}: {latency:.1f} ms"
            
            if latency > threshold_red:
                print_colored(output, 'red')
                if last_state != 'red':
                    log_event(f"Semáforo en ROJO: Latencia crítica de {latency:.1f} ms", log_file)
                    last_state = 'red'
            elif latency > threshold_yellow:
                print_colored(output, 'yellow')
                if last_state != 'yellow':
                    log_event(f"Semáforo en AMARILLO: Latencia media de {latency:.1f} ms", log_file)
                    last_state = 'yellow'
            else:
                print_colored(output, 'green')
                if last_state != 'green':
                    log_event(f"Semáforo en VERDE: Latencia normal de {latency:.1f} ms", log_file)
                    last_state = 'green'
        else:
            logger.error(f"No se pudo obtener la latencia para {host}")
            log_event(f"Fallo al obtener latencia para {host}", log_file)
        
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor de red con sistema de semáforo")
    parser.add_argument("host", help="Dirección IP o nombre de host a monitorear")
    parser.add_argument("--log", default="network_monitor.log", help="Archivo de registro")
    parser.add_argument("--interval", type=float, default=1, help="Intervalo entre pings en segundos")
    parser.add_argument("--yellow", type=float, default=100, help="Umbral para semáforo amarillo (ms)")
    parser.add_argument("--red", type=float, default=300, help="Umbral para semáforo rojo (ms)")
    
    args = parser.parse_args()
    
    main(args.host, args.log, args.interval, args.yellow, args.red)
