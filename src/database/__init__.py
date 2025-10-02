# -*- coding: utf-8 -*-
"""
Paquete de base de datos para el Gateway Local
"""

# Importaciones públicas
from .database_manager import DatabaseManager, get_database_manager

__all__ = [
    "DatabaseManager",
    "get_database_manager"
]
