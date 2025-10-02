#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el comportamiento completo del frontend
"""

import requests
import time
import json

def test_full_frontend():
    """Prueba el comportamiento completo del frontend"""
    print("Iniciando prueba completa del frontend...")
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get('http://localhost:5001/')
        if response.status_code == 200:
            print("✓ Servidor accesible")
        else:
            print(f"✗ Error accediendo al servidor: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error conectando al servidor: {e}")
        return False
    
    # Verificar que la API devuelva configuraciones
    try:
        response = requests.get('http://localhost:5001/api/v1/config')
        if response.status_code == 200:
            configs = response.json()
            print(f"✓ API devuelve configuraciones: {configs}")
        else:
            print(f"✗ Error en API de configuración: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error accediendo a la API: {e}")
        return False
    
    # Verificar que los archivos estáticos estén disponibles
    static_files = ['script.js', 'styles.css', 'debug_frontend.js']
    for file in static_files:
        try:
            response = requests.get(f'http://localhost:5001/{file}')
            if response.status_code == 200 and len(response.text) > 0:
                print(f"✓ Archivo {file} accesible")
            else:
                print(f"✗ Error accediendo a {file}: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error accediendo a {file}: {e}")
            return False
    
    # Verificar que el HTML contenga los elementos necesarios
    try:
        response = requests.get('http://localhost:5001/')
        html_content = response.text
        
        required_elements = [
            'id="config-view"',
            'id="bind-address"',
            'id="bind-port"',
            'id="plc-port"',
            'id="scan-interval"',
            'id="log-level"',
            'id="wms-endpoint"'
        ]
        
        all_found = True
        for element in required_elements:
            if element in html_content:
                print(f"✓ Elemento {element} encontrado en el HTML")
            else:
                print(f"✗ Elemento {element} NO encontrado en el HTML")
                all_found = False
        
        if all_found:
            print("✓ Todos los elementos requeridos encontrados en el HTML")
        else:
            print("✗ Algunos elementos requeridos NO encontrados en el HTML")
            return False
            
    except Exception as e:
        print(f"✗ Error verificando elementos del HTML: {e}")
        return False
    
    print("✓ Prueba completa del frontend pasada exitosamente")
    return True

if __name__ == "__main__":
    test_full_frontend()