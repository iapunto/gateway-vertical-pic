#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para insertar configuraciones de prueba en la base de datos
"""

import sqlite3
import os


def insert_test_config():
    """Inserta configuraciones de prueba en la base de datos"""
    db_path = "gateway.db"

    if not os.path.exists(db_path):
        print(f"Base de datos {db_path} no encontrada")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Insertar configuraciones de prueba
        configs = [
            ("bind_address", "0.0.0.0", "Dirección IP de escucha"),
            ("bind_port", "8080", "Puerto de escucha"),
            ("plc_port", "3200", "Puerto PLC"),
            ("scan_interval", "30", "Intervalo de escaneo"),
            ("log_level", "INFO", "Nivel de log"),
            ("wms_endpoint", "https://wms.example.com/api/v1/gateways", "Endpoint WMS")
        ]

        for key, value, description in configs:
            cursor.execute('''
                INSERT OR REPLACE INTO configurations 
                (key, value, description, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (key, value, description))

        conn.commit()
        conn.close()

        print("Configuraciones de prueba insertadas correctamente")

    except Exception as e:
        print(f"Error insertando configuraciones: {e}")


if __name__ == "__main__":
    insert_test_config()
