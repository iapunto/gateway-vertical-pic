#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API REST para el Gateway Local
"""

from src.monitoring import get_metrics_collector
from src.health.health_checker import HealthChecker
from src.adapters.api_adapter import APIAdapter
from src.core.gateway_core import GatewayCore
from src.database import get_database_manager
import sys
import os
import logging
from typing import Optional
from flask import Flask
from flask.logging import default_handler

# Importar las nuevas rutas modulares
from src.api.routes.status_routes import register_status_routes
from src.api.routes.health_routes import register_health_routes
from src.api.routes.database_routes import register_database_routes
from src.api.routes.ui_routes import register_ui_routes

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class GatewayAPI:
    """API REST para el Gateway Local"""

    def __init__(self, config_file: str = "gateway_config.json"):
        self.app = Flask(__name__)
        self.gateway = GatewayCore(config_file)
        self.adapter = APIAdapter(self.gateway)
        self.health_checker = HealthChecker(self.gateway)
        self.metrics_collector = get_metrics_collector()
        self.database_manager = get_database_manager()
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
        # Registrar las rutas modulares
        register_status_routes(self.app, self.adapter)
        register_health_routes(
            self.app, self.health_checker, self.metrics_collector)
        register_database_routes(self.app, self.database_manager)
        register_ui_routes(self.app)

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
