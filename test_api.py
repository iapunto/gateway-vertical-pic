#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la API del Gateway Local
"""

import requests
import json

# URL base de la API
BASE_URL = "http://localhost:8081/api/v1"


def test_api():
    """Prueba las funcionalidades principales de la API"""
    print("Probando API del Gateway Local...")

    # Probar endpoint de estadísticas
    try:
        response = requests.get(f"{BASE_URL}/stats")
        print(f"Endpoint /stats: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"  Estadísticas: {json.dumps(stats, indent=2)}")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  Error al conectar con /stats: {e}")

    # Probar endpoint de PLCs
    try:
        response = requests.get(f"{BASE_URL}/plcs")
        print(f"Endpoint /plcs: {response.status_code}")
        if response.status_code == 200:
            plcs = response.json()
            print(f"  PLCs encontrados: {len(plcs) if plcs else 0}")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  Error al conectar con /plcs: {e}")

    # Probar endpoint de comandos
    try:
        response = requests.get(f"{BASE_URL}/commands?limit=5")
        print(f"Endpoint /commands: {response.status_code}")
        if response.status_code == 200:
            commands = response.json()
            print(
                f"  Comandos encontrados: {len(commands) if commands else 0}")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  Error al conectar con /commands: {e}")

    # Probar endpoint de eventos
    try:
        response = requests.get(f"{BASE_URL}/events?limit=5")
        print(f"Endpoint /events: {response.status_code}")
        if response.status_code == 200:
            events = response.json()
            print(f"  Eventos encontrados: {len(events) if events else 0}")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  Error al conectar con /events: {e}")


if __name__ == "__main__":
    test_api()
