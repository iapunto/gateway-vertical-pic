#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar el estado actual de la base de datos y la API
"""

import requests
import json


def verify_data():
    """Verifica el estado actual de la base de datos y la API"""
    print("Verificando estado actual de la base de datos y la API...")

    # Verificar configuración
    try:
        response = requests.get('http://localhost:5001/api/v1/config')
        if response.status_code == 200:
            config = response.json()
            print("✓ Configuración en la API:")
            for key, value in config.items():
                print(f"  {key}: {value}")
        else:
            print(f"✗ Error obteniendo configuración: {response.status_code}")
    except Exception as e:
        print(f"✗ Error conectando a la API de configuración: {e}")

    print()

    # Verificar PLCs
    try:
        response = requests.get('http://localhost:5001/api/v1/plcs')
        if response.status_code == 200:
            plcs = response.json()
            print("✓ PLCs en la API:")
            if plcs:
                for plc in plcs:
                    print(f"  ID: {plc.get('plc_id', plc.get('id'))}")
                    print(f"  Nombre: {plc.get('name', 'N/A')}")
                    print(f"  IP: {plc.get('ip_address', 'N/A')}")
                    print(f"  Puerto: {plc.get('port', 'N/A')}")
                    print(f"  Tipo: {plc.get('type', 'N/A')}")
                    print()
            else:
                print("  No hay PLCs registrados")
        else:
            print(f"✗ Error obteniendo PLCs: {response.status_code}")
    except Exception as e:
        print(f"✗ Error conectando a la API de PLCs: {e}")


if __name__ == "__main__":
    verify_data()
