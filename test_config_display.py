#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar que los datos de configuración se muestren correctamente
en la interfaz web
"""

import requests
import json


def test_config_display():
    """Verifica que los datos de configuración se muestren correctamente"""
    print("Iniciando prueba de visualización de configuración...")

    # Insertar configuración de prueba
    test_configs = [
        {"key": "bind_address", "value": "192.168.1.100",
            "description": "Dirección IP de prueba"},
        {"key": "bind_port", "value": "9090", "description": "Puerto de prueba"},
        {"key": "plc_port", "value": "3300", "description": "Puerto PLC de prueba"},
        {"key": "scan_interval", "value": "60",
            "description": "Intervalo de escaneo de prueba"},
        {"key": "log_level", "value": "DEBUG",
            "description": "Nivel de log de prueba"},
        {"key": "wms_endpoint", "value": "https://test.wms.example.com/api/v1/gateways",
            "description": "Endpoint WMS de prueba"}
    ]

    print("Insertando configuración de prueba...")
    for config in test_configs:
        try:
            response = requests.post(
                'http://localhost:5001/api/v1/config',
                json=config
            )
            if response.status_code == 200:
                print(f"✓ Configuración {config['key']} insertada")
            else:
                print(
                    f"✗ Error insertando {config['key']}: {response.status_code}")
        except Exception as e:
            print(f"✗ Error insertando {config['key']}: {e}")

    # Verificar que la API devuelva la configuración de prueba
    print("\nVerificando configuración en la API...")
    try:
        response = requests.get('http://localhost:5001/api/v1/config')
        if response.status_code == 200:
            api_configs = response.json()
            print("✓ Configuración obtenida de la API")

            # Verificar que los valores sean los de prueba
            expected_values = {
                "bind_address": "192.168.1.100",
                "bind_port": "9090",
                "plc_port": "3300",
                "scan_interval": "60",
                "log_level": "DEBUG",
                "wms_endpoint": "https://test.wms.example.com/api/v1/gateways"
            }

            all_correct = True
            for key, expected_value in expected_values.items():
                if api_configs.get(key) == expected_value:
                    print(f"✓ {key}: {api_configs[key]}")
                else:
                    print(
                        f"✗ {key}: esperado {expected_value}, obtenido {api_configs.get(key)}")
                    all_correct = False

            if all_correct:
                print("✓ Todos los valores de configuración son correctos en la API")
            else:
                print("✗ Algunos valores de configuración no coinciden en la API")
                return False
        else:
            print(f"✗ Error obteniendo configuración: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error verificando configuración en la API: {e}")
        return False

    print("✓ Prueba de visualización de configuración completada exitosamente")
    return True


if __name__ == "__main__":
    test_config_display()
