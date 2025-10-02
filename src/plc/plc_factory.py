#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fábrica para crear instancias de PLCs
"""

from typing import Dict, Type
from interfaces.plc_interface import PLCInterface
from plc.delta_plc import DeltaPLC

# Registro de tipos de PLCs disponibles
PLC_TYPES: Dict[str, Type[PLCInterface]] = {
    "delta": DeltaPLC,
    # Se pueden añadir más tipos de PLCs aquí
}


class PLCFactory:
    """Fábrica para crear instancias de PLCs"""

    @staticmethod
    def create_plc(plc_type: str, ip: str, port: int = 3200) -> PLCInterface:
        """Crea una instancia de PLC del tipo especificado

        Args:
            plc_type: Tipo de PLC a crear
            ip: Dirección IP del PLC
            port: Puerto del PLC

        Returns:
            Instancia del PLC especificado

        Raises:
            ValueError: Si el tipo de PLC no está soportado
        """
        # Convertir a minúsculas para hacerlo case-insensitive
        plc_type_lower = plc_type.lower()

        if plc_type_lower not in PLC_TYPES:
            raise ValueError(f"Tipo de PLC no soportado: {plc_type}")

        # Crear instancia usando type.__call__
        plc_class = PLC_TYPES[plc_type_lower]
        return plc_class.__call__(ip, port)
