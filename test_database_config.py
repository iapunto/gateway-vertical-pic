#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar que la función get_all_configurations del DatabaseManager
esté funcionando correctamente
"""

from src.database.database_manager import DatabaseManager
import sys
import os

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_database_config():
    """Verifica que la función get_all_configurations funcione correctamente"""
    print("Iniciando prueba de configuración de base de datos...")

    try:
        # Crear instancia del DatabaseManager
        db_manager = DatabaseManager()
        print("✓ DatabaseManager creado exitosamente")

        # Obtener todas las configuraciones
        configs = db_manager.get_all_configurations()
        print(f"✓ Configuraciones obtenidas: {configs}")

        # Verificar que se obtengan las configuraciones esperadas
        expected_keys = ["bind_address", "bind_port", "plc_port",
                         "scan_interval", "log_level", "wms_endpoint"]
        for key in expected_keys:
            if key in configs:
                print(f"✓ Configuración {key}: {configs[key]}")
            else:
                print(f"⚠ Configuración {key} no encontrada")

        print("✓ Prueba de configuración de base de datos completada exitosamente")
        return True

    except Exception as e:
        print(f"✗ Error en la prueba de configuración de base de datos: {e}")
        return False


if __name__ == "__main__":
    test_database_config()
