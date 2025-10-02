#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementación específica para PLC Delta AS Series
"""

import socket
import struct
import time
import logging
import random
from typing import Dict, Any, Optional
from gateway.src.interfaces.plc_interface import PLCInterface


class DeltaPLC(PLCInterface):
    """Implementación para PLC Delta AS Series"""

    def __init__(self, ip: str, port: int = 3200):
        self.ip = ip
        self.port = port
        self.sock = None
        self.timeout = 5.0
        self.logger = logging.getLogger(__name__)
        self.max_retries = 3
        self.base_backoff = 0.5

    def connect(self) -> bool:
        """Establece conexión TCP/IP con el PLC Delta"""
        if self.sock:
            return True

        for attempt in range(1, self.max_retries + 1):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(self.timeout)
                self.sock.connect((self.ip, self.port))
                self.logger.info(
                    f"Conexión establecida con PLC Delta en {self.ip}:{self.port}")
                return True
            except (socket.timeout, ConnectionRefusedError, OSError) as e:
                self.logger.warning(
                    f"Intento {attempt}: Error de conexión con PLC Delta: {str(e)}")
                self.disconnect()
                if attempt < self.max_retries:
                    backoff = self.base_backoff * \
                        (2 ** (attempt - 1)) + random.uniform(0, 0.2)
                    time.sleep(backoff)
        self.logger.error(
            f"No se pudo conectar al PLC Delta tras {self.max_retries} intentos.")
        return False

    def disconnect(self) -> None:
        """Cierra la conexión con el PLC Delta"""
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
            except OSError:
                pass
            finally:
                self.sock = None

    def is_connected(self) -> bool:
        """Verifica si el PLC Delta está conectado"""
        return self.sock is not None

    def send_command(self, command: int, argument: Optional[int] = None) -> Dict[str, Any]:
        """Envía un comando al PLC Delta"""
        if not self.sock:
            return {'error': 'No hay conexión activa con el PLC', 'success': False}

        # Validar comando
        if not isinstance(command, int) or not (0 <= command <= 255):
            return {'error': 'Comando debe ser un entero entre 0 y 255', 'success': False}

        if argument is not None and (not isinstance(argument, int) or not (0 <= argument <= 255)):
            return {'error': 'Argumento debe ser un entero entre 0 y 255', 'success': False}

        for attempt in range(1, self.max_retries + 1):
            try:
                data = struct.pack('B', command)
                if argument is not None:
                    data += struct.pack('B', argument)
                self.sock.sendall(data)

                # Recibir respuesta
                response_data = self.sock.recv(2)
                if len(response_data) < 2:
                    return {'error': 'Respuesta incompleta del PLC', 'success': False}
                status, position = struct.unpack('BB', response_data)

                return {
                    'status_code': status,
                    'position': position,
                    'success': True
                }
            except (socket.timeout, BrokenPipeError, OSError) as e:
                self.logger.warning(
                    f"Intento {attempt}: Error enviando datos al PLC: {str(e)}")
                self.disconnect()
                if attempt < self.max_retries:
                    if self.connect():
                        backoff = self.base_backoff * \
                            (2 ** (attempt - 1)) + random.uniform(0, 0.2)
                        time.sleep(backoff)
                        continue
                return {'error': f"Error enviando datos: {str(e)}", 'success': False}

        return {'error': 'Máximo número de reintentos alcanzado', 'success': False}

    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del PLC Delta"""
        try:
            if not self.sock:
                if not self.connect():
                    return {'error': 'No se pudo conectar al PLC', 'success': False}
            return self.send_command(0)  # Comando STATUS
        except Exception as e:
            self.logger.error(f"Error obteniendo estado: {str(e)}")
            return {'error': str(e), 'success': False}

    def get_position(self) -> int:
        """Obtiene la posición actual del carrusel"""
        status = self.get_status()
        return status.get('position', -1)
