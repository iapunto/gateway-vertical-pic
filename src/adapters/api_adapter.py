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
            status = self.gateway_core.get_status()
            plc_status = status.get("plcs", {}).get(machine_id, {})
            return {
                "success": True,
                "data": {machine_id: plc_status}
            }
        else:
            # Obtener estado de todos los PLCs
            status = self.gateway_core.get_status()
            return {
                "success": True,
                "data": status.get("plcs", {})
            }

    def send_command(self, command: int, argument: Optional[int] = None,
                     machine_id: Optional[str] = None) -> Dict[str, Any]:
        """Envía un comando a un PLC"""
        # Mapear comandos numéricos a comandos de texto
        command_map = {
            0: "STATUS",
            1: "MOVE",
            2: "START",
            3: "STOP",
            4: "RESET"
        }

        command_name = command_map.get(command, "STATUS")

        if machine_id:
            # Enviar comando a un PLC específico
            return self.gateway_core.send_command(command_name, argument, machine_id)
        else:
            # Enviar comando a todos los PLCs
            return self.gateway_core.send_command(command_name, argument)

    def get_machines(self) -> Dict[str, Any]:
        """Obtiene la lista de máquinas disponibles"""
        status = self.gateway_core.get_status()
        plc_list = []
        for plc_id, plc_info in status.get("plcs", {}).items():
            plc_list.append({
                "id": plc_id,
                "type": "PLC",
                "status": "connected" if plc_info.get("connected", False) else "disconnected"
            })

        return {
            "success": True,
            "data": plc_list
        }

    def move_to_position(self, position: int, machine_id: Optional[str] = None) -> Dict[str, Any]:
        """Mueve un carrusel a una posición específica"""
        # Comando 1 = MUEVETE
        return self.send_command(1, position, machine_id)
