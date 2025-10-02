#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de configuración para el Gateway Local
"""

import os
import json
import logging
from typing import Dict, Any, Optional


class ConfigManager:
    """Gestor centralizado de configuración"""

    def __init__(self, config_file: str = "gateway_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.logger = logging.getLogger(__name__)

    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde archivo o valores por defecto"""
        default_config = {
            "gateway": {
                "id": "GW-001",
                "name": "Gateway Local Principal",
                "version": "2.7.0"
            },
            "wms": {
                "endpoint": "https://wms.example.com/api/v1/gateways",
                "auth_token": "",
                "reconnect_interval": 30,
                "heartbeat_interval": 60
            },
            "network": {
                "bind_address": "0.0.0.0",
                "bind_port": 8080,
                "plc_port": 3200
            },
            "security": {
                "tls_cert": "",
                "tls_key": "",
                "ca_cert": "",
                "require_tls": False
            },
            "logging": {
                "level": "INFO",
                "file": "gateway.log",
                "max_size": 10485760,  # 10MB
                "backup_count": 5
            },
            "plcs": [
                # Ejemplo de configuración de PLCs
                # {
                #     "id": "PLC-001",
                #     "type": "delta",
                #     "ip": "192.168.1.100",
                #     "port": 3200
                # }
            ]
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                # Merge con configuración por defecto
                self._merge_config(default_config, file_config)
            except Exception as e:
                self.logger.error(f"Error cargando configuración: {e}")

        return default_config

    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Merge de configuración base con override"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def get(self, key_path: str, default=None):
        """Obtiene un valor de configuración usando notación de punto"""
        keys = key_path.split('.')
        value = self.config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key_path: str, value: Any) -> None:
        """Establece un valor de configuración usando notación de punto"""
        keys = key_path.split('.')
        config = self.config

        # Navegar hasta el penúltimo nivel
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        # Establecer el valor en el último nivel
        config[keys[-1]] = value

    def save(self, config_file: Optional[str] = None) -> bool:
        """Guarda la configuración en archivo"""
        try:
            save_path = config_file or self.config_file
            with open(save_path, 'w') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Error guardando configuración: {e}")
            return False

    def get_plc_list(self) -> list:
        """Obtiene la lista de PLCs configurados"""
        return self.config.get("plcs", [])

    def add_plc(self, plc_config: Dict[str, Any]) -> None:
        """Añade un PLC a la configuración"""
        if "plcs" not in self.config:
            self.config["plcs"] = []
        self.config["plcs"].append(plc_config)

    def remove_plc(self, plc_id: str) -> bool:
        """Elimina un PLC de la configuración"""
        if "plcs" not in self.config:
            return False

        for i, plc in enumerate(self.config["plcs"]):
            if plc.get("id") == plc_id:
                del self.config["plcs"][i]
                return True
        return False
