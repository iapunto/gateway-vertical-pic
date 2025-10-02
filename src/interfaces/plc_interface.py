#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface común para todos los PLCs
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class PLCInterface(ABC):
    """Interface común para todos los PLCs"""

    @abstractmethod
    def connect(self) -> bool:
        """Establece conexión con el PLC

        Returns:
            True si la conexión fue exitosa, False en caso contrario
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Cierra la conexión con el PLC"""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Verifica si hay conexión con el PLC

        Returns:
            True si hay conexión, False en caso contrario
        """
        pass

    @abstractmethod
    def send_command(self, command: int, argument: Optional[int] = None) -> Dict[str, Any]:
        """Envía un comando al PLC y devuelve la respuesta

        Args:
            command: Código del comando
            argument: Argumento opcional del comando

        Returns:
            Diccionario con la respuesta del PLC
        """
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del PLC

        Returns:
            Diccionario con el estado del PLC
        """
        pass

    @abstractmethod
    def move_to_position(self, position: int) -> Dict[str, Any]:
        """Mueve el carrusel a una posición específica

        Args:
            position: Posición a la que mover el carrusel

        Returns:
            Diccionario con el resultado de la operación
        """
        pass
