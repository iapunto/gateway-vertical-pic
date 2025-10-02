#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API REST para el Gateway Local
"""

from .gateway_api import GatewayAPI, create_app, main
from .routes import register_status_routes, register_health_routes, register_database_routes, register_ui_routes
from .middleware import AuthMiddleware, RateLimitMiddleware, SecurityMiddleware

__all__ = [
    'GatewayAPI',
    'create_app',
    'main',
    'register_status_routes',
    'register_health_routes',
    'register_database_routes',
    'register_ui_routes',
    'AuthMiddleware',
    'RateLimitMiddleware',
    'SecurityMiddleware'
]
