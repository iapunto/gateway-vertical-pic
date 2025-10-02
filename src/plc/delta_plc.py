#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementación específica para PLC Delta AS Series
"""

import socket
import time
import struct
from typing import Dict, Any, Optional
from interfaces.plc_interface import PLCInterface


class DeltaPLC(PLCInterface):
    """Implementación específica para PLC Delta AS Series"""

    def __init__(self, ip: str, port: int = 3200):
        """Inicializa la conexión con el PLC

        Args:
            ip: Dirección IP del PLC
            port: Puerto del PLC (por defecto 3200)
        """
        self.ip = ip
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.connected = False

    def connect(self) -> bool:
        """Establece conexión con el PLC"""
        try:
            if self.socket:
                self.socket.close()

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)  # 5 segundos de timeout
            self.socket.connect((self.ip, self.port))
            self.connected = True
            return True
        except Exception as e:
            print(f"Error conectando a PLC {self.ip}:{self.port} - {e}")
            self.connected = False
            return False

    def disconnect(self) -> None:
        """Cierra la conexión con el PLC"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            self.connected = False

    def is_connected(self) -> bool:
        """Verifica si hay conexión con el PLC"""
        return self.connected

    def send_command(self, command: int, argument: Optional[int] = None) -> Dict[str, Any]:
        """Envía un comando al PLC y devuelve la respuesta

        Args:
            command: Código del comando (0=ESTADO, 1=MUEVETE)
            argument: Argumento opcional del comando (posición para MUEVETE)

        Returns:
            Diccionario con la respuesta del PLC
        """
        if not self.connected or self.socket is None:
            return {"success": False, "error": "PLC no conectado"}

        try:
            start_time = time.time()

            # Formato del mensaje:
            # 2 bytes: comando
            # 2 bytes: argumento (si aplica)
            if argument is not None:
                message = struct.pack('>HH', command, argument)
            else:
                message = struct.pack('>H', command)

            # Enviar comando
            self.socket.send(message)

            # Recibir respuesta (8 bytes: 2 de estado + 2 de posición + 4 de tiempo)
            response = self.socket.recv(8)
            status, position, timestamp = struct.unpack('>HHI', response)

            end_time = time.time()
            response_time = end_time - start_time

            return {
                "success": True,
                "status_code": status,
                "position": position,
                "timestamp": timestamp,
                "response_time": response_time
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del PLC"""
        return self.send_command(0)  # Comando 0 = ESTADO

    def move_to_position(self, position: int) -> Dict[str, Any]:
        """Mueve el carrusel a una posición específica"""
        return self.send_command(1, position)  # Comando 1 = MUEVETE
