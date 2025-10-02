#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API REST para el Gateway Local
"""

from adapters.api_adapter import APIAdapter
from core.gateway_core import GatewayCore
import sys
import os
import json
import logging
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from flask.logging import default_handler

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class GatewayAPI:
    """API REST para el Gateway Local"""

    def __init__(self, config_file: str = "gateway_config.json"):
        self.app = Flask(__name__)
        self.gateway = GatewayCore(config_file)
        self.adapter = APIAdapter(self.gateway)
        self._setup_logging()
        self._setup_routes()

    def _setup_logging(self) -> None:
        """Configura el logging para la API"""
        # Eliminar el handler por defecto
        self.app.logger.removeHandler(default_handler)

        # Configurar nivel de logging
        log_level = self.gateway.config_manager.get("logging.level", "INFO")
        if isinstance(log_level, str):
            self.app.logger.setLevel(
                getattr(logging, log_level.upper(), logging.INFO))
        else:
            self.app.logger.setLevel(logging.INFO)

    def _setup_routes(self) -> None:
        """Configura las rutas de la API"""
        self.app.add_url_rule('/api/v1/status', 'get_status',
                              self.get_status, methods=['GET'])
        self.app.add_url_rule('/api/v1/status/<machine_id>',
                              'get_machine_status', self.get_machine_status, methods=['GET'])
        self.app.add_url_rule('/api/v1/machines', 'get_machines',
                              self.get_machines, methods=['GET'])
        self.app.add_url_rule('/api/v1/command', 'send_command',
                              self.send_command, methods=['POST'])
        self.app.add_url_rule('/api/v1/move/<int:position>',
                              'move_to_position', self.move_to_position, methods=['POST'])
        self.app.add_url_rule('/api/v1/start', 'start_gateway',
                              self.start_gateway, methods=['POST'])
        self.app.add_url_rule('/api/v1/stop', 'stop_gateway',
                              self.stop_gateway, methods=['POST'])

    def get_status(self):
        """Obtiene el estado de todos los PLCs"""
        try:
            status = self.adapter.get_status()
            return jsonify(status)
        except Exception as e:
            self.app.logger.error(f"Error obteniendo status: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    def get_machine_status(self, machine_id: str):
        """Obtiene el estado de un PLC específico"""
        try:
            status = self.adapter.get_status(machine_id)
            return jsonify(status)
        except Exception as e:
            self.app.logger.error(
                f"Error obteniendo status de máquina {machine_id}: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    def get_machines(self):
        """Obtiene la lista de máquinas disponibles"""
        try:
            machines = self.adapter.get_machines()
            return jsonify(machines)
        except Exception as e:
            self.app.logger.error(f"Error obteniendo lista de máquinas: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    def send_command(self):
        """Envía un comando a un PLC"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No se proporcionaron datos", "success": False}), 400

            command = data.get('command')
            argument = data.get('argument')
            machine_id = data.get('machine_id')

            if command is None:
                return jsonify({"error": "Falta el parámetro 'command'", "success": False}), 400

            result = self.adapter.send_command(command, argument, machine_id)
            return jsonify(result)
        except Exception as e:
            self.app.logger.error(f"Error enviando comando: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    def move_to_position(self, position: int):
        """Mueve un carrusel a una posición específica"""
        try:
            data = request.get_json()
            machine_id = data.get('machine_id') if data else None

            result = self.adapter.move_to_position(position, machine_id)
            return jsonify(result)
        except Exception as e:
            self.app.logger.error(f"Error moviendo a posición {position}: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    def start_gateway(self):
        """Inicia el gateway"""
        try:
            if self.gateway.running:
                return jsonify({"message": "Gateway ya está iniciado", "success": True})

            if self.gateway.start():
                return jsonify({"message": "Gateway iniciado exitosamente", "success": True})
            else:
                return jsonify({"error": "Error iniciando Gateway", "success": False}), 500
        except Exception as e:
            self.app.logger.error(f"Error iniciando gateway: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    def stop_gateway(self):
        """Detiene el gateway"""
        try:
            if not self.gateway.running:
                return jsonify({"message": "Gateway ya está detenido", "success": True})

            self.gateway.stop()
            return jsonify({"message": "Gateway detenido exitosamente", "success": True})
        except Exception as e:
            self.app.logger.error(f"Error deteniendo gateway: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    def run(self, host: Optional[str] = None, port: Optional[int] = None, debug: bool = False) -> None:
        """Inicia el servidor Flask"""
        # Obtener configuración de red del gateway
        if host is None:
            host_config = self.gateway.config_manager.get(
                "network.bind_address", "0.0.0.0")
            host = host_config if isinstance(host_config, str) else "0.0.0.0"
        if port is None:
            port_config = self.gateway.config_manager.get(
                "network.bind_port", 8080)
            port = port_config if isinstance(port_config, int) else 8080

        self.app.logger.info(f"Iniciando API REST en {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


def create_app(config_file: str = "gateway_config.json") -> Flask:
    """Crea y configura la aplicación Flask"""
    api = GatewayAPI(config_file)
    return api.app


def main():
    """Función principal para ejecutar la API"""
    import argparse

    parser = argparse.ArgumentParser(description="API REST para Gateway Local")
    parser.add_argument("--host", default=None,
                        help="Dirección IP para escuchar")
    parser.add_argument("--port", type=int, default=None,
                        help="Puerto para escuchar")
    parser.add_argument("--config", default="gateway_config.json",
                        help="Archivo de configuración")
    parser.add_argument("--debug", action="store_true", help="Modo debug")

    args = parser.parse_args()

    api = GatewayAPI(args.config)
    api.run(args.host, args.port, args.debug)


if __name__ == "__main__":
    main()
