#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptador para mantener compatibilidad con la API existente
"""

from typing import Dict, Any, Optional

# Corregir la importación
from src.core.gateway_core import GatewayCore


class APIAdapter:
    """Adaptador para mantener compatibilidad con la API existente"""

    def __init__(self, gateway_core: GatewayCore):
        self.gateway_core = gateway_core

    def get_status(self, machine_id: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene el estado de un PLC o todos los PLCs"""
        if machine_id:
            # Obtener estado de un PLC específico
            return self.gateway_core.get_plc_status(machine_id)
        else:
            # Obtener estado de todos los PLCs
            all_status = {}
            for plc_id in self.gateway_core.plcs.keys():
                all_status[plc_id] = self.gateway_core.get_plc_status(plc_id)
            return {
                "success": True,
                "data": all_status
            }

    def send_command(self, command: int, argument: Optional[int] = None,
                     machine_id: Optional[str] = None) -> Dict[str, Any]:
        """Envía un comando a un PLC"""
        if machine_id:
            # Enviar comando a un PLC específico
            return self.gateway_core.send_plc_command(machine_id, command, argument)
        else:
            # Enviar comando al primer PLC disponible
            if self.gateway_core.plcs:
                first_plc_id = list(self.gateway_core.plcs.keys())[0]
                return self.gateway_core.send_plc_command(first_plc_id, command, argument)
            else:
                return {"error": "No hay PLCs disponibles", "success": False}

    def get_machines(self) -> Dict[str, Any]:
        """Obtiene la lista de máquinas disponibles"""
        plc_list = []
        for plc_id, plc in self.gateway_core.plcs.items():
            plc_list.append({
                "id": plc_id,
                "type": "PLC",
                "status": "connected" if plc.is_connected() else "disconnected"
            })

        return {
            "success": True,
            "data": plc_list
        }

    def move_to_position(self, position: int, machine_id: Optional[str] = None) -> Dict[str, Any]:
        """Mueve un carrusel a una posición específica"""
        # Comando 1 = MUEVETE
        return self.send_command(1, position, machine_id)
