#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rutas para la interfaz web del gateway
"""

import os
from flask import send_from_directory


def register_ui_routes(app):
    """Registra las rutas para la interfaz web"""

    @app.route('/', methods=['GET'])
    def index():
        """Sirve la página principal de la interfaz web"""
        web_dir = os.path.join(os.path.dirname(
            __file__), '..', '..', '..', 'web')
        return send_from_directory(web_dir, 'index.html')

    @app.route('/<path:path>', methods=['GET'])
    def serve_static(path):
        """Sirve archivos estáticos de la interfaz web"""
        web_dir = os.path.join(os.path.dirname(
            __file__), '..', '..', '..', 'web')
        return send_from_directory(web_dir, path)
