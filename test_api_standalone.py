#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la API de forma aislada
"""

from src.api.routes.database_routes import register_database_routes
from src.database import get_database_manager
from flask import Flask, jsonify
import sys
import os

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def create_test_app():
    """Crea una aplicación de prueba"""
    app = Flask(__name__)

    # Obtener el DatabaseManager
    database_manager = get_database_manager()

    # Registrar las rutas
    register_database_routes(app, database_manager)

    @app.route('/')
    def index():
        return "API de prueba funcionando"

    return app


if __name__ == "__main__":
    app = create_test_app()
    app.run(host='0.0.0.0', port=8082, debug=True)
