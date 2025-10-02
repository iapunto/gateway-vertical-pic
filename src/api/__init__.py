#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paquete API para el Gateway Local
"""

# Versión del paquete
__version__ = "1.0.0"

# Importaciones públicas
from .gateway_api import GatewayAPI, create_app

__all__ = ["GatewayAPI", "create_app"]