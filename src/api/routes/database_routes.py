#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rutas para la gestión de datos en la base de datos
"""

from flask import jsonify, request
from database import get_database_manager


def register_database_routes(app, database_manager):
    """Registra las rutas para la gestión de datos en la base de datos"""

    @app.route('/api/v1/plcs', methods=['GET'])
    def get_all_plcs():
        """Obtiene todos los PLCs registrados"""
        try:
            plcs = database_manager.get_all_plcs()
            return jsonify(plcs)
        except Exception as e:
            app.logger.error(f"Error obteniendo PLCs: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/plcs/<plc_id>', methods=['GET'])
    def get_plc(plc_id: str):
        """Obtiene un PLC específico"""
        try:
            plc = database_manager.get_plc(plc_id)
            if plc:
                return jsonify(plc)
            else:
                return jsonify({"error": "PLC no encontrado", "success": False}), 404
        except Exception as e:
            app.logger.error(f"Error obteniendo PLC {plc_id}: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/plcs/<plc_id>', methods=['DELETE'])
    def remove_plc(plc_id: str):
        """Elimina un PLC de la base de datos"""
        try:
            if database_manager.remove_plc(plc_id):
                return jsonify({"message": "PLC eliminado exitosamente", "success": True})
            else:
                return jsonify({"error": "Error eliminando PLC", "success": False}), 500
        except Exception as e:
            app.logger.error(f"Error eliminando PLC {plc_id}: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/commands', methods=['GET'])
    def get_commands():
        """Obtiene los comandos registrados"""
        try:
            plc_id = request.args.get('plc_id')
            limit = request.args.get('limit', default=100, type=int)
            commands = database_manager.get_commands(plc_id, limit)
            return jsonify(commands)
        except Exception as e:
            app.logger.error(f"Error obteniendo comandos: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/events', methods=['GET'])
    def get_events():
        """Obtiene los eventos registrados"""
        try:
            event_type = request.args.get('type')
            limit = request.args.get('limit', default=100, type=int)
            events = database_manager.get_events(event_type, limit)
            return jsonify(events)
        except Exception as e:
            app.logger.error(f"Error obteniendo eventos: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/metrics', methods=['GET'])
    def get_metrics():
        """Obtiene los registros de métricas"""
        try:
            metric_type = request.args.get('type')
            plc_id = request.args.get('plc_id')
            hours = request.args.get('hours', default=24, type=int)
            metrics = database_manager.get_metrics(
                metric_type, plc_id, hours)
            return jsonify(metrics)
        except Exception as e:
            app.logger.error(f"Error obteniendo métricas: {e}")
            return jsonify({"error": str(e), "success": False}), 500

    @app.route('/api/v1/stats', methods=['GET'])
    def get_database_stats():
        """Obtiene estadísticas de la base de datos"""
        try:
            stats = database_manager.get_database_stats()
            return jsonify(stats)
        except Exception as e:
            app.logger.error(f"Error obteniendo estadísticas: {e}")
            return jsonify({"error": str(e), "success": False}), 500
