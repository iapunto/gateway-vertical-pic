#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de rutas para la API REST del Gateway Local
"""

from .status_routes import register_status_routes
from .health_routes import register_health_routes
from .database_routes import register_database_routes
from .ui_routes import register_ui_routes

__all__ = ['register_status_routes', 'register_health_routes',
           'register_database_routes', 'register_ui_routes']
