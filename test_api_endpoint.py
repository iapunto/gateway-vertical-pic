#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar que el endpoint de configuración de la API funcione correctamente
"""

from src.database.database_manager import DatabaseManager
import sys
import os

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_api_endpoint():
    """Verifica que el endpoint de configuración de la API funcione correctamente"""
    print("Iniciando prueba del endpoint de configuración de la API...")

    try:
        # Crear instancia del DatabaseManager
        db_manager = DatabaseManager()
        print("✓ DatabaseManager creado exitosamente")

        # Probar la función get_all_configurations directamente
        configs = db_manager.get_all_configurations()
        print(f"✓ Configuraciones obtenidas directamente: {configs}")

        # Verificar que las configuraciones sean las esperadas
        expected_configs = {
            "bind_address": "192.168.1.100",
            "bind_port": "9090",
            "plc_port": "3300",
            "scan_interval": "60",
            "log_level": "DEBUG",
            "wms_endpoint": "https://test.wms.example.com/api/v1/gateways"
        }

        all_correct = True
        for key, expected_value in expected_configs.items():
            if configs.get(key) == expected_value:
                print(f"✓ {key}: {configs[key]}")
            else:
                print(
                    f"✗ {key}: esperado {expected_value}, obtenido {configs.get(key)}")
                all_correct = False

        if all_correct:
            print("✓ Todas las configuraciones son correctas")
        else:
            print("✗ Algunas configuraciones no coinciden")
            return False

        print("✓ Prueba del endpoint de configuración completada exitosamente")
        return True

    except Exception as e:
        print(f"✗ Error en la prueba del endpoint de configuración: {e}")
        return False


if __name__ == "__main__":
    test_api_endpoint()
