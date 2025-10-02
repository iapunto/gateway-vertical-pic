#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface para comunicación con PLCs
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class PLCInterface(ABC):
    """Interface base para comunicación con PLCs"""

    @abstractmethod
    def connect(self) -> bool:
        """Establece conexión con el PLC"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Cierra la conexión con el PLC"""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Verifica si el PLC está conectado"""
        pass

    @abstractmethod
    def send_command(self, command: int, argument: Optional[int] = None) -> Dict[str, Any]:
        """Envía un comando al PLC"""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del PLC"""
        pass

    @abstractmethod
    def get_position(self) -> int:
        """Obtiene la posición actual del carrusel"""
        pass
