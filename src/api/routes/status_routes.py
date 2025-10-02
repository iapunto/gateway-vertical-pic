#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rutas para el estado y control del gateway y PLCs
"""

from flask import jsonify, request
from adapters.api_adapter import APIAdapter


def register_status_routes(app, adapter: APIAdapter):
    """Registra las rutas de estado y control"""

    @app.route('/api/v1/status', methods=['GET'])
    def get_status():
        """Obtiene el estado de todos los PLCs"""
        try:
            status = adapter.get_status()
            return jsonify(status)
        except Exception as e:
            app.logger.error(f"Error obteniendo status: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/status/<machine_id>', methods=['GET'])
    def get_machine_status(machine_id: str):
        """Obtiene el estado de un PLC específico"""
        try:
            status = adapter.get_status(machine_id)
            return jsonify(status)
        except Exception as e:
            app.logger.error(
                f"Error obteniendo status de máquina {machine_id}: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/machines', methods=['GET'])
    def get_machines():
        """Obtiene la lista de máquinas disponibles"""
        try:
            machines = adapter.get_machines()
            return jsonify(machines)
        except Exception as e:
            app.logger.error(f"Error obteniendo lista de máquinas: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/command', methods=['POST'])
    def send_command():
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

            result = adapter.send_command(command, argument, machine_id)
            return jsonify(result)
        except Exception as e:
            app.logger.error(f"Error enviando comando: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/move/<int:position>', methods=['POST'])
    def move_to_position(position: int):
        """Mueve un carrusel a una posición específica"""
        try:
            data = request.get_json()
            machine_id = data.get('machine_id') if data else None

            result = adapter.move_to_position(position, machine_id)
            return jsonify(result)
        except Exception as e:
            app.logger.error(f"Error moviendo a posición {position}: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/start', methods=['POST'])
    def start_gateway():
        """Inicia el gateway"""
        try:
            if adapter.gateway_core.running:
                return jsonify({"message": "Gateway ya está iniciado", "success": True})

            if adapter.gateway_core.start():
                return jsonify({"message": "Gateway iniciado exitosamente", "success": True})
            else:
                return jsonify({"error": "Error iniciando Gateway", "success": False}), 500
        except Exception as e:
            app.logger.error(f"Error iniciando gateway: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/stop', methods=['POST'])
    def stop_gateway():
        """Detiene el gateway"""
        try:
            if not adapter.gateway_core.running:
                return jsonify({"message": "Gateway ya está detenido", "success": True})

            adapter.gateway_core.stop()
            return jsonify({"message": "Gateway detenido exitosamente", "success": True})
        except Exception as e:
            app.logger.error(f"Error deteniendo gateway: {e}")
            return jsonify({"error": str(e), "success": False}), 500
