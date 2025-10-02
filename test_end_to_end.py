#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba de extremo a extremo para verificar que el frontend
esté cargando correctamente los datos de configuración desde la base de datos
"""

import requests
import time


def test_end_to_end():
    """Prueba de extremo a extremo"""
    print("Iniciando prueba de extremo a extremo...")

    # Verificar que el servidor Flask esté corriendo
    try:
        response = requests.get('http://localhost:5001/api/v1/config')
        if response.status_code == 200:
            print("✓ Servidor Flask accesible")
            config_data = response.json()
            print(f"✓ Configuración obtenida de la API: {config_data}")
        else:
            print(f"✗ Error al obtener configuración: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error conectando al servidor Flask: {e}")
        return False

    # Verificar que se pueda acceder a la interfaz web
    try:
        response = requests.get('http://localhost:5001/')
        if response.status_code == 200:
            print("✓ Interfaz web accesible")
        else:
            print(
                f"✗ Error al acceder a la interfaz web: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error accediendo a la interfaz web: {e}")
        return False

    # Verificar que se puedan acceder a los archivos estáticos
    try:
        response = requests.get('http://localhost:5001/script.js')
        if response.status_code == 200 and len(response.text) > 0:
            print("✓ Archivo script.js accesible")
        else:
            print(f"✗ Error al acceder a script.js: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error accediendo a script.js: {e}")
        return False

    try:
        response = requests.get('http://localhost:5001/styles.css')
        if response.status_code == 200 and len(response.text) > 0:
            print("✓ Archivo styles.css accesible")
        else:
            print(f"✗ Error al acceder a styles.css: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error accediendo a styles.css: {e}")
        return False

    print("✓ Todas las pruebas pasaron exitosamente")
    return True


if __name__ == "__main__":
    test_end_to_end()
