#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el DatabaseManager
"""

from src.database import get_database_manager
import sys
import os

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_database_manager():
    """Prueba el DatabaseManager"""
    try:
        # Obtener la instancia del DatabaseManager
        db_manager = get_database_manager()

        # Probar obtener todas las configuraciones
        configs = db_manager.get_all_configurations()
        print("Configuraciones obtenidas:")
        for key, value in configs.items():
            print(f"  {key}: {value}")

        # Probar obtener una configuración específica
        bind_address = db_manager.get_configuration("bind_address")
        print(f"\nConfiguración bind_address: {bind_address}")

    except Exception as e:
        print(f"Error probando DatabaseManager: {e}")


if __name__ == "__main__":
    test_database_manager()
