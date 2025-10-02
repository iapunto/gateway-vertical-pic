#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rutas para la salud y métricas del sistema
"""

from flask import jsonify
from src.health.health_checker import HealthChecker
from src.monitoring import get_metrics_collector


def register_health_routes(app, health_checker: HealthChecker, metrics_collector):
    """Registra las rutas de salud y métricas"""

    @app.route('/health', methods=['GET'])
    def health_check():
        """Endpoint de verificación de salud"""
        try:
            health_status = health_checker.get_health_status()
            status_code = 200
            if health_status['status'] == 'unhealthy':
                status_code = 503
            elif health_status['status'] == 'degraded':
                status_code = 200  # Aún funcional pero con problemas

            return jsonify(health_status), status_code
        except Exception as e:
            app.logger.error(f"Error en health check: {e}")
            return jsonify({
                "status": "error",
                "message": str(e),
                "timestamp": health_checker.get_health_status()['timestamp']
            }), 500

    @app.route('/metrics', methods=['GET'])
    def metrics():
        """Endpoint de métricas para Prometheus"""
        try:
            metrics_text = metrics_collector.get_metrics_text()
            return metrics_text, 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}
        except Exception as e:
            app.logger.error(f"Error obteniendo métricas: {e}")
            return "Error obteniendo métricas", 500, {'Content-Type': 'text/plain'}
