#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Túnel HTTP reverso para conectar Gateway Local con WMS en la nube
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, Optional, Callable
from urllib.parse import urljoin
import requests
from threading import Thread


class ReverseTunnel:
    """Túnel HTTP reverso para comunicación con WMS"""

    def __init__(self, wms_endpoint: str, auth_token: str, gateway_id: str):
        """Inicializa el túnel reverso

        Args:
            wms_endpoint: URL base del WMS
            auth_token: Token de autenticación
            gateway_id: ID único del gateway
        """
        self.wms_endpoint = wms_endpoint.rstrip('/')
        self.auth_token = auth_token
        self.gateway_id = gateway_id
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.reconnect_interval = 30  # segundos
        self.heartbeat_interval = 60  # segundos
        self.command_callback: Optional[Callable] = None
        self.worker_thread: Optional[Thread] = None

    def set_command_callback(self, callback: Callable):
        """Establece el callback para manejar comandos entrantes"""
        self.command_callback = callback

    def connect(self) -> bool:
        """Establece conexión con el servidor de túnel del WMS"""
        try:
            # Registrar el gateway en el túnel
            tunnel_url = urljoin(self.wms_endpoint, '/api/v1/tunnel/register')
            register_data = {
                'gateway_id': self.gateway_id,
                'timestamp': time.time()
            }

            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json',
                'X-Gateway-ID': self.gateway_id
            }

            response = requests.post(
                tunnel_url,
                json=register_data,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                self.logger.info("Gateway registrado en túnel reverso")
                return True
            else:
                self.logger.error(
                    f"Error registrando gateway en túnel: {response.status_code}")
                return False

        except Exception as e:
            self.logger.error(f"Error conectando al túnel reverso: {e}")
            return False

    def start(self):
        """Inicia el túnel reverso"""
        self.running = True
        self.logger.info("Iniciando túnel reverso...")

        # Conectar inicialmente
        if not self.connect():
            self.logger.error(
                "No se pudo establecer conexión inicial con el túnel")
            return

        # Iniciar workers en un hilo separado
        self.worker_thread = Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def stop(self):
        """Detiene el túnel reverso"""
        self.running = False
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=5)
        self.logger.info("Túnel reverso detenido")

    def _worker_loop(self):
        """Bucle principal de workers"""
        import time
        while self.running:
            try:
                # Ejecutar heartbeat y verificación de comandos
                self._send_heartbeat()
                self._check_commands()
                time.sleep(5)  # Ciclo cada 5 segundos
            except Exception as e:
                self.logger.error(f"Error en bucle de workers: {e}")
                time.sleep(5)

    def _send_heartbeat(self):
        """Envía heartbeat periódico"""
        try:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json',
                'X-Gateway-ID': self.gateway_id
            }

            heartbeat_url = urljoin(
                self.wms_endpoint, '/api/v1/tunnel/heartbeat')
            heartbeat_data = {
                'gateway_id': self.gateway_id,
                'timestamp': time.time()
            }

            response = requests.post(
                heartbeat_url,
                json=heartbeat_data,
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:
                self.logger.warning(
                    f"Error en heartbeat: {response.status_code}")

        except Exception as e:
            self.logger.error(f"Error en heartbeat: {e}")

    def _check_commands(self):
        """Verifica comandos pendientes del WMS"""
        try:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'X-Gateway-ID': self.gateway_id
            }

            commands_url = urljoin(
                self.wms_endpoint, '/api/v1/tunnel/commands')
            response = requests.get(commands_url, headers=headers, timeout=30)

            if response.status_code == 200:
                try:
                    commands = response.json()
                    if commands and isinstance(commands, list):
                        for command in commands:
                            self._handle_command(command)
                except json.JSONDecodeError:
                    # 204 = No content (no commands)
                    if response.status_code != 204:
                        self.logger.warning(
                            f"Error decodificando comandos: {response.status_code}")
            elif response.status_code != 204:  # 204 = No content (no commands)
                self.logger.warning(
                    f"Error obteniendo comandos: {response.status_code}")

        except Exception as e:
            self.logger.error(f"Error verificando comandos: {e}")

    def _handle_command(self, command: Dict[str, Any]):
        """Maneja un comando recibido del WMS"""
        try:
            self.logger.info(f"Comando recibido: {command}")

            if self.command_callback:
                # Ejecutar el callback para manejar el comando
                result = self.command_callback(command)

                # Enviar resultado de vuelta al WMS
                if 'id' in command:
                    self._send_command_result(command['id'], result)
            else:
                self.logger.warning(
                    "No hay callback registrado para manejar comandos")

        except Exception as e:
            self.logger.error(f"Error manejando comando: {e}")
            if 'id' in command:
                self._send_command_result(
                    command['id'],
                    {'success': False, 'error': str(e)}
                )

    def _send_command_result(self, command_id: str, result: Dict[str, Any]):
        """Envía el resultado de un comando al WMS"""
        try:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json',
                'X-Gateway-ID': self.gateway_id
            }

            result_url = urljoin(
                self.wms_endpoint,
                f'/api/v1/tunnel/commands/{command_id}/result'
            )
            result_data = {
                'command_id': command_id,
                'result': result,
                'timestamp': time.time()
            }

            response = requests.post(
                result_url,
                json=result_data,
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:
                self.logger.error(
                    f"Error enviando resultado de comando: {response.status_code}")

        except Exception as e:
            self.logger.error(f"Error enviando resultado de comando: {e}")

    def send_sensor_data(self, sensor_data: Dict[str, Any]) -> bool:
        """Envía datos de sensores al WMS a través del túnel"""
        try:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json',
                'X-Gateway-ID': self.gateway_id
            }

            sensor_url = urljoin(
                self.wms_endpoint, '/api/v1/tunnel/sensor-data')
            data = {
                'gateway_id': self.gateway_id,
                'data': sensor_data,
                'timestamp': time.time()
            }

            response = requests.post(
                sensor_url,
                json=data,
                headers=headers,
                timeout=30
            )

            return response.status_code == 200

        except Exception as e:
            self.logger.error(f"Error enviando datos de sensores: {e}")
            return False


# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    def example_command_callback(command):
        """Ejemplo de callback para manejar comandos"""
        print(f"Manejando comando: {command}")
        # Aquí iría la lógica para ejecutar el comando
        return {'success': True, 'result': 'Comando ejecutado'}

    def main():
        # Crear túnel (reemplazar con valores reales)
        tunnel = ReverseTunnel(
            wms_endpoint="https://wms.example.com",
            auth_token="tu_token_aqui",
            gateway_id="GW-001"
        )

        # Establecer callback para comandos
        tunnel.set_command_callback(example_command_callback)

        try:
            # Iniciar túnel
            tunnel.start()

            # Mantener el proceso vivo
            import time
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("Deteniendo túnel...")
        finally:
            tunnel.stop()

    # Ejecutar ejemplo
    main()
