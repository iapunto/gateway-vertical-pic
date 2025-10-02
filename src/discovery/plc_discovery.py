#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de descubrimiento automático de PLCs en la red
"""

import socket
import threading
import time
import ipaddress
from typing import List, Dict, Optional, Callable, Any
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


class PLCDetector:
    """Detector de PLCs en la red"""

    def __init__(self, port: int = 3200, timeout: int = 2):
        self.port = port
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self.found_devices = []
        self.is_scanning = False

    def scan_single_ip(self, ip: str) -> Optional[Dict[str, Any]]:
        """Escanear una única dirección IP para detectar PLC"""
        try:
            # Crear socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)

            # Intentar conectar
            result = sock.connect_ex((ip, self.port))
            sock.close()

            if result == 0:
                # Puerto abierto, posible PLC
                self.logger.info(f"Dispositivo encontrado en {ip}:{self.port}")
                return {
                    "ip": ip,
                    "port": self.port,
                    "type": "delta",  # Por defecto asumimos Delta
                    "status": "online"
                }
            return None

        except Exception as e:
            self.logger.debug(f"Error escaneando {ip}: {e}")
            return None

    def scan_ip_range(self, start_ip: str, end_ip: str,
                      progress_callback: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """Escanear un rango de direcciones IP"""
        self.is_scanning = True
        self.found_devices = []

        try:
            # Convertir IPs a objetos ipaddress
            start = ipaddress.IPv4Address(start_ip)
            end = ipaddress.IPv4Address(end_ip)

            # Generar lista de IPs
            ips = [str(ipaddress.IPv4Address(int(start) + i))
                   for i in range(int(end) - int(start) + 1)]

            total_ips = len(ips)
            scanned = 0

            # Usar ThreadPoolExecutor para escaneo paralelo
            with ThreadPoolExecutor(max_workers=50) as executor:
                # Crear tareas para cada IP
                future_to_ip = {executor.submit(
                    self.scan_single_ip, ip): ip for ip in ips}

                # Procesar resultados a medida que se completan
                for future in as_completed(future_to_ip):
                    ip = future_to_ip[future]
                    try:
                        result = future.result()
                        if result:
                            self.found_devices.append(result)

                        scanned += 1
                        if progress_callback:
                            progress_callback(scanned, total_ips, result)

                    except Exception as e:
                        self.logger.error(f"Error procesando {ip}: {e}")
                        scanned += 1
                        if progress_callback:
                            progress_callback(scanned, total_ips, None)

            self.is_scanning = False
            return self.found_devices

        except Exception as e:
            self.logger.error(f"Error en escaneo de rango: {e}")
            self.is_scanning = False
            return []

    def scan_subnet(self, subnet: str,
                    progress_callback: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """Escanear una subred completa"""
        try:
            network = ipaddress.IPv4Network(subnet, strict=False)
            hosts = list(network.hosts())

            # Convertir a strings
            ip_list = [str(ip) for ip in hosts]

            total_ips = len(ip_list)
            scanned = 0
            self.found_devices = []

            # Usar ThreadPoolExecutor para escaneo paralelo
            with ThreadPoolExecutor(max_workers=50) as executor:
                # Crear tareas para cada IP
                future_to_ip = {executor.submit(
                    self.scan_single_ip, ip): ip for ip in ip_list}

                # Procesar resultados a medida que se completan
                for future in as_completed(future_to_ip):
                    ip = future_to_ip[future]
                    try:
                        result = future.result()
                        if result:
                            self.found_devices.append(result)

                        scanned += 1
                        if progress_callback:
                            progress_callback(scanned, total_ips, result)

                    except Exception as e:
                        self.logger.error(f"Error procesando {ip}: {e}")
                        scanned += 1
                        if progress_callback:
                            progress_callback(scanned, total_ips, None)

            return self.found_devices

        except Exception as e:
            self.logger.error(f"Error en escaneo de subred: {e}")
            return []

    def stop_scan(self):
        """Detener el escaneo"""
        self.is_scanning = False


class PLCDiscoveryService:
    """Servicio de descubrimiento de PLCs"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.detector = PLCDetector()
        self.is_discovering = False

    def discover_plcs(self, target: str = "192.168.1.0/24",
                      discovery_type: str = "subnet",
                      progress_callback: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """Descubrir PLCs en la red

        Args:
            target: Rango de IPs o subred a escanear
            discovery_type: Tipo de descubrimiento ("subnet", "range")
            progress_callback: Callback para reportar progreso

        Returns:
            Lista de dispositivos encontrados
        """
        self.is_discovering = True

        try:
            if discovery_type == "subnet":
                devices = self.detector.scan_subnet(target, progress_callback)
            elif discovery_type == "range":
                # Para rango, necesitamos separar inicio y fin
                if "-" in target:
                    start_ip, end_ip = target.split("-")
                    devices = self.detector.scan_ip_range(
                        start_ip.strip(), end_ip.strip(), progress_callback)
                else:
                    self.logger.error("Formato de rango inválido")
                    devices = []
            else:
                self.logger.error(
                    f"Tipo de descubrimiento no soportado: {discovery_type}")
                devices = []

            self.is_discovering = False
            return devices

        except Exception as e:
            self.logger.error(f"Error en descubrimiento de PLCs: {e}")
            self.is_discovering = False
            return []

    def stop_discovery(self):
        """Detener el proceso de descubrimiento"""
        self.is_discovering = False
        self.detector.stop_scan()


def main():
    """Función de prueba para el descubrimiento de PLCs"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Descubrimiento de PLCs en la red")
    parser.add_argument("--target", default="192.168.1.0/24",
                        help="Subred o rango a escanear")
    parser.add_argument("--type", default="subnet",
                        choices=["subnet", "range"],
                        help="Tipo de escaneo")

    args = parser.parse_args()

    # Configurar logging
    logging.basicConfig(level=logging.INFO)

    # Crear servicio de descubrimiento
    discovery_service = PLCDiscoveryService()

    def progress_callback(current, total, device):
        """Callback para mostrar progreso"""
        percentage = (current / total) * 100
        if device:
            print(
                f"Progreso: {percentage:.1f}% - Dispositivo encontrado: {device['ip']}")
        else:
            print(f"Progreso: {percentage:.1f}% - Escaneando...")

    print(f"Iniciando descubrimiento en {args.target}")
    devices = discovery_service.discover_plcs(
        target=args.target,
        discovery_type=args.type,
        progress_callback=progress_callback
    )

    print(f"\nDispositivos encontrados: {len(devices)}")
    for device in devices:
        print(f"  - {device['ip']}:{device['port']} ({device['type']})")


if __name__ == "__main__":
    main()
