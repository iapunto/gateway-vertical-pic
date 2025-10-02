#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar las configuraciones en la base de datos
"""

import sqlite3
import os


def check_config():
    """Verifica las configuraciones en la base de datos"""
    db_path = "gateway.db"

    if not os.path.exists(db_path):
        print(f"Base de datos {db_path} no encontrada")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT key, value FROM configurations')
        rows = cursor.fetchall()

        print("Configuraciones en la base de datos:")
        for row in rows:
            print(f"{row[0]}: {row[1]}")

        conn.close()

    except Exception as e:
        print(f"Error verificando configuraciones: {e}")


if __name__ == "__main__":
    check_config()
