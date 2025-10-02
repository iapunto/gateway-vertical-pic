#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de descubrimiento automático de PLCs Vertical PIC
"""

import socket
import threading
import time
import logging
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress

from .delta_plc import DeltaPLC


class PLCDiscovery:
    """Clase para descubrir automáticamente PLCs en la red"""

    def __init__(self, port: int = 3200, timeout: int = 2):
        """Inicializa el descubridor de PLCs

        Args:
            port: Puerto donde escuchan los PLCs (por defecto 3200)
            timeout: Tiempo de espera para conexiones en segundos
        """
        self.port = port
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self.discovered_plcs: List[Dict[str, Any]] = []

    def scan_single_ip(self, ip: str) -> Optional[Dict[str, Any]]:
        """Escanea una única dirección IP en busca de un PLC

        Args:
            ip: Dirección IP a escanear

        Returns:
            Dict con información del PLC encontrado o None si no se encontró
        """
        try:
            # Intentar conectar al PLC
            plc = DeltaPLC(ip, self.port)
            plc.timeout = self.timeout

            if plc.connect():
                # Si la conexión es exitosa, obtener información del PLC
                status = plc.get_status()
                position = plc.get_position()

                plc_info = {
                    'ip': ip,
                    'port': self.port,
                    'connected': True,
                    'status': status,
                    'position': position,
                    'type': 'Delta AS Series',
                    'model': 'Unknown'  # Podría obtenerse con comandos adicionales
                }

                plc.disconnect()
                return plc_info
            else:
                return None

        except Exception as e:
            # No registrar errores de conexión como warnings, ya que muchas IPs no tendrán PLCs
            self.logger.debug(
                f"IP {ip} no responde en puerto {self.port}: {e}")
            return None

    def scan_ip_range(self, start_ip: str, end_ip: str, max_workers: int = 50) -> List[Dict[str, Any]]:
        """Escanea un rango de direcciones IP en busca de PLCs

        Args:
            start_ip: Dirección IP inicial del rango
            end_ip: Dirección IP final del rango
            max_workers: Número máximo de hilos para el escaneo paralelo

        Returns:
            Lista de diccionarios con información de PLCs encontrados
        """
        self.logger.info(f"Iniciando escaneo de rango {start_ip} - {end_ip}")

        # Generar lista de IPs en el rango
        ip_list = self._generate_ip_range(start_ip, end_ip)
        self.logger.info(f"Escaneando {len(ip_list)} direcciones IP")

        discovered_plcs = []

        # Usar ThreadPoolExecutor para escaneo paralelo
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Enviar todas las tareas
            future_to_ip = {
                executor.submit(self.scan_single_ip, ip): ip
                for ip in ip_list
            }

            # Recolectar resultados
            for future in as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    result = future.result()
                    if result:
                        discovered_plcs.append(result)
                        self.logger.info(f"PLC encontrado en {ip}")
                except Exception as e:
                    self.logger.error(f"Error escaneando {ip}: {e}")

        self.logger.info(
            f"Escaneo completado. {len(discovered_plcs)} PLCs encontrados")
        return discovered_plcs

    def scan_local_network(self, max_workers: int = 50) -> List[Dict[str, Any]]:
        """Escanea la red local en busca de PLCs

        Args:
            max_workers: Número máximo de hilos para el escaneo paralelo

        Returns:
            Lista de diccionarios con información de PLCs encontrados
        """
        self.logger.info("Iniciando escaneo de red local")

        # Obtener las interfaces de red locales
        local_ips = self._get_local_networks()

        all_discovered_plcs = []

        for network in local_ips:
            self.logger.info(f"Escaneando red {network}")
            try:
                # Convertir la red a formato de rango
                network_obj = ipaddress.ip_network(network, strict=False)
                # Saltar la dirección de red
                start_ip = str(network_obj.network_address + 1)
                # Saltar la dirección de broadcast
                end_ip = str(network_obj.broadcast_address - 1)

                # Escanear la red
                discovered = self.scan_ip_range(start_ip, end_ip, max_workers)
                all_discovered_plcs.extend(discovered)

            except Exception as e:
                self.logger.error(f"Error escaneando red {network}: {e}")

        self.logger.info(
            f"Escaneo de red local completado. {len(all_discovered_plcs)} PLCs encontrados")
        return all_discovered_plcs

    def _generate_ip_range(self, start_ip: str, end_ip: str) -> List[str]:
        """Genera una lista de direcciones IP en un rango

        Args:
            start_ip: Dirección IP inicial
            end_ip: Dirección IP final

        Returns:
            Lista de direcciones IP en formato string
        """
        try:
            start = ipaddress.ip_address(start_ip)
            end = ipaddress.ip_address(end_ip)

            # Verificar que ambas IPs sean del mismo tipo (IPv4 o IPv6)
            if type(start) != type(end):
                raise ValueError("Las direcciones IP deben ser del mismo tipo")

            # Generar rango de IPs
            ip_list = []
            current_int = int(start)
            end_int = int(end)

            while current_int <= end_int:
                if isinstance(start, ipaddress.IPv4Address):
                    ip_list.append(str(ipaddress.IPv4Address(current_int)))
                else:
                    ip_list.append(str(ipaddress.IPv6Address(current_int)))
                current_int += 1

            return ip_list
        except Exception as e:
            self.logger.error(
                f"Error generando rango de IPs {start_ip} - {end_ip}: {e}")
            return []

    def _get_local_networks(self) -> List[str]:
        """Obtiene las redes locales del sistema

        Returns:
            Lista de redes locales en formato CIDR
        """
        try:
            import netifaces

            networks = []

            # Obtener todas las interfaces de red
            interfaces = netifaces.interfaces()

            for interface in interfaces:
                # Obtener direcciones de la interfaz
                addrs = netifaces.ifaddresses(interface)

                # Verificar direcciones IPv4
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        addr = addr_info['addr']
                        netmask = addr_info.get('netmask')

                        # Ignorar direcciones locales y de loopback
                        if addr.startswith('127.') or addr == '0.0.0.0':
                            continue

                        # Crear red en formato CIDR
                        if netmask:
                            network = f"{addr}/{netmask}"
                            networks.append(network)

            return networks

        except ImportError:
            # Si netifaces no está disponible, usar una implementación básica
            self.logger.warning(
                "netifaces no disponible, usando implementación básica")
            return self._get_local_networks_basic()
        except Exception as e:
            self.logger.error(f"Error obteniendo redes locales: {e}")
            return self._get_local_networks_basic()

    def _get_local_networks_basic(self) -> List[str]:
        """Implementación básica para obtener redes locales

        Returns:
            Lista de redes locales comunes
        """
        # Redes locales comunes
        common_networks = [
            "192.168.0.0/24",
            "192.168.1.0/24",
            "10.0.0.0/24",
            "172.16.0.0/24"
        ]

        self.logger.info("Usando redes locales comunes para escaneo")
        return common_networks

    def quick_scan_subnet(self, subnet: str, max_workers: int = 50) -> List[Dict[str, Any]]:
        """Escaneo rápido de una subred específica

        Args:
            subnet: Subred en formato CIDR (ej: 192.168.1.0/24)
            max_workers: Número máximo de hilos para el escaneo paralelo

        Returns:
            Lista de diccionarios con información de PLCs encontrados
        """
        self.logger.info(f"Iniciando escaneo rápido de subred {subnet}")

        try:
            # Convertir subred a rango de IPs
            network = ipaddress.ip_network(subnet, strict=False)

            # Generar lista de IPs (excluyendo red y broadcast)
            ip_list = [str(ip) for ip in network.hosts()]

            discovered_plcs = []

            # Usar ThreadPoolExecutor para escaneo paralelo
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Enviar todas las tareas
                future_to_ip = {
                    executor.submit(self.scan_single_ip, ip): ip
                    for ip in ip_list
                }

                # Recolectar resultados
                for future in as_completed(future_to_ip):
                    ip = future_to_ip[future]
                    try:
                        result = future.result()
                        if result:
                            discovered_plcs.append(result)
                            self.logger.info(f"PLC encontrado en {ip}")
                    except Exception as e:
                        self.logger.error(f"Error escaneando {ip}: {e}")

            self.logger.info(
                f"Escaneo de subred {subnet} completado. {len(discovered_plcs)} PLCs encontrados")
            return discovered_plcs

        except Exception as e:
            self.logger.error(f"Error escaneando subred {subnet}: {e}")
            return []

    def save_discovery_results(self, results: List[Dict[str, Any]], filename: str = "discovered_plcs.json") -> bool:
        """Guarda los resultados del descubrimiento en un archivo JSON

        Args:
            results: Lista de resultados de descubrimiento
            filename: Nombre del archivo de salida

        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            import json

            # Agregar timestamp a los resultados
            output_data = {
                "timestamp": time.time(),
                "plcs": results
            }

            with open(filename, 'w') as f:
                json.dump(output_data, f, indent=2)

            self.logger.info(f"Resultados guardados en {filename}")
            return True

        except Exception as e:
            self.logger.error(f"Error guardando resultados: {e}")
            return False


# Función de utilidad para uso directo
def discover_plcs_on_network(subnet: Optional[str] = None,
                             start_ip: Optional[str] = None,
                             end_ip: Optional[str] = None,
                             port: int = 3200) -> List[Dict[str, Any]]:
    """Función de conveniencia para descubrir PLCs

    Args:
        subnet: Subred en formato CIDR para escaneo (opcional)
        start_ip: IP inicial para escaneo de rango (opcional)
        end_ip: IP final para escaneo de rango (opcional)
        port: Puerto donde escuchan los PLCs (por defecto 3200)

    Returns:
        Lista de diccionarios con información de PLCs encontrados
    """
    discovery = PLCDiscovery(port=port)

    if subnet:
        return discovery.quick_scan_subnet(subnet)
    elif start_ip and end_ip:
        return discovery.scan_ip_range(start_ip, end_ip)
    else:
        return discovery.scan_local_network()


# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Crear descubridor
    discovery = PLCDiscovery()

    # Ejemplo 1: Escanear una subred específica
    print("Escaneando subred 192.168.1.0/24...")
    results = discovery.quick_scan_subnet("192.168.1.0/24")

    # Mostrar resultados
    print(f"PLCs encontrados: {len(results)}")
    for plc in results:
        print(f"  - {plc['ip']}:{plc['port']} - {plc['type']}")

    # Guardar resultados
    discovery.save_discovery_results(results)
