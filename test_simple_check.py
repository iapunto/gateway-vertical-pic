#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para verificar los componentes clave
"""

import requests

def test_simple_check():
    """Verificación simple de los componentes clave"""
    print("Verificando componentes clave...")
    
    # Verificar API de configuración
    try:
        response = requests.get('http://localhost:5001/api/v1/config')
        if response.status_code == 200:
            configs = response.json()
            print(f"API Config: {configs}")
        else:
            print(f"Error API: {response.status_code}")
    except Exception as e:
        print(f"Error API: {e}")
    
    # Verificar elementos HTML
    try:
        response = requests.get('http://localhost:5001/')
        html = response.text
        
        elements = ['config-view', 'bind-address', 'bind-port']
        for element in elements:
            if element in html:
                print(f"HTML {element}: ✓")
            else:
                print(f"HTML {element}: ✗")
    except Exception as e:
        print(f"Error HTML: {e}")

if __name__ == "__main__":
    test_simple_check()