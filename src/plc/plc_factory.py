#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fábrica para crear instancias de PLCs según el tipo
"""

from typing import Dict, Any

# Corregir las importaciones
from interfaces.plc_interface import PLCInterface
from plc.delta_plc import DeltaPLC


class PLCFactory:
    """Fábrica para crear instancias de PLCs"""

    # Mapeo de tipos de PLC a sus implementaciones
    PLC_TYPES = {
        'delta': DeltaPLC,
        'Delta': DeltaPLC,
        'DELTA': DeltaPLC
    }

    @classmethod
    def create_plc(cls, plc_type: str, ip: str, port: int = 3200) -> PLCInterface:
        """Crea una instancia de PLC según el tipo especificado"""
        plc_class = cls.PLC_TYPES.get(plc_type)
        if not plc_class:
            raise ValueError(f"Tipo de PLC no soportado: {plc_type}")

        return plc_class(ip, port)

    @classmethod
    def register_plc_type(cls, plc_type: str, plc_class):
        """Registra un nuevo tipo de PLC"""
        cls.PLC_TYPES[plc_type] = plc_class

    @classmethod
    def get_supported_types(cls) -> list:
        """Retorna los tipos de PLC soportados"""
        return list(cls.PLC_TYPES.keys())
