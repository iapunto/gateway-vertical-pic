#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paquete de comunicación entre microservicios para el Gateway Local
"""

# Versión del paquete
__version__ = "1.0.0"

# Importaciones públicas
from .service_client import (
    ServiceClient, 
    ServiceRegistry, 
    ServiceInfo, 
    ServiceStatus,
    get_service_registry,
    register_service,
    get_service_client
)

__all__ = [
    "ServiceClient",
    "ServiceRegistry", 
    "ServiceInfo", 
    "ServiceStatus",
    "get_service_registry",
    "register_service",
    "get_service_client"
]