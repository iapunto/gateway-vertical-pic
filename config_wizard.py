#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asistente de configuración para el Gateway Local
"""

import json
import os
import sys
from typing import Dict, Any


def load_config(config_file: str = "gateway_config.json") -> Dict[str, Any]:
    """Carga la configuración desde un archivo"""
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            # Cargar configuración de ejemplo si no existe
            with open("gateway_config_example.json", 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error cargando configuración: {e}")
        return {}


def save_config(config: Dict[str, Any], config_file: str = "gateway_config.json") -> bool:
    """Guarda la configuración en un archivo"""
    try:
        # Crear directorio de logs si no existe
        log_file = config.get("logging", {}).get("file", "")
        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error guardando configuración: {e}")
        return False


def get_input(prompt: str, default: str = "") -> str:
    """Obtiene entrada del usuario con un valor por defecto"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()


def configure_gateway(config: Dict[str, Any]) -> Dict[str, Any]:
    """Configura los parámetros del gateway"""
    print("\n=== Configuración del Gateway ===")

    gateway = config.get("gateway", {})
    gateway["id"] = get_input("ID del Gateway", gateway.get("id", "GW-001"))
    gateway["name"] = get_input("Nombre del Gateway", gateway.get(
        "name", "Gateway Local Principal"))
    gateway["version"] = get_input(
        "Versión del Gateway", gateway.get("version", "2.7.0"))
    config["gateway"] = gateway

    return config


def configure_wms(config: Dict[str, Any]) -> Dict[str, Any]:
    """Configura los parámetros de conexión con el WMS"""
    print("\n=== Configuración de conexión con WMS ===")

    wms = config.get("wms", {})
    wms["endpoint"] = get_input("Endpoint del WMS", wms.get(
        "endpoint", "https://wms.example.com/api/v1/gateways"))
    wms["auth_token"] = get_input(
        "Token de autenticación del WMS", wms.get("auth_token", ""))
    wms["reconnect_interval"] = int(get_input(
        "Intervalo de reconexión (segundos)", str(wms.get("reconnect_interval", 30))))
    wms["heartbeat_interval"] = int(get_input(
        "Intervalo de heartbeat (segundos)", str(wms.get("heartbeat_interval", 60))))
    config["wms"] = wms

    return config


def configure_network(config: Dict[str, Any]) -> Dict[str, Any]:
    """Configura los parámetros de red"""
    print("\n=== Configuración de red ===")

    network = config.get("network", {})
    network["bind_address"] = get_input(
        "Dirección IP para escuchar", network.get("bind_address", "0.0.0.0"))
    network["bind_port"] = int(
        get_input("Puerto para la API", str(network.get("bind_port", 8080))))
    network["plc_port"] = int(
        get_input("Puerto para conexiones PLC", str(network.get("plc_port", 3200))))
    config["network"] = network

    return config


def configure_logging(config: Dict[str, Any]) -> Dict[str, Any]:
    """Configura los parámetros de logging"""
    print("\n=== Configuración de logging ===")

    logging = config.get("logging", {})
    logging["level"] = get_input(
        "Nivel de log (DEBUG, INFO, WARNING, ERROR)", logging.get("level", "INFO"))
    logging["file"] = get_input(
        "Archivo de log", logging.get("file", "logs/gateway.log"))
    logging["max_size"] = int(get_input(
        "Tamaño máximo del archivo (bytes)", str(logging.get("max_size", 10485760))))
    logging["backup_count"] = int(get_input(
        "Número de archivos de respaldo", str(logging.get("backup_count", 5))))
    config["logging"] = logging

    return config


def configure_plcs(config: Dict[str, Any]) -> Dict[str, Any]:
    """Configura los PLCs"""
    print("\n=== Configuración de PLCs ===")

    plcs = config.get("plcs", [])

    while True:
        print(f"\nPLCs configurados actualmente: {len(plcs)}")
        if plcs:
            for i, plc in enumerate(plcs):
                print(
                    f"  {i+1}. {plc.get('id', 'Sin ID')} - {plc.get('ip', 'Sin IP')}:{plc.get('port', 3200)}")

        action = get_input(
            "\n¿Qué desea hacer? (añadir/eliminar/listo)", "listo").lower()

        if action == "listo":
            break
        elif action == "añadir":
            plc = {}
            plc["id"] = get_input("ID del PLC", f"PLC-{len(plcs)+1:03d}")
            plc["type"] = get_input("Tipo de PLC", "delta")
            plc["name"] = get_input(
                "Nombre del PLC", f"Carrusel {len(plcs)+1}")
            plc["ip"] = get_input("Dirección IP del PLC", "192.168.1.50")
            plc["port"] = int(get_input("Puerto del PLC", "3200"))
            plc["description"] = get_input(
                "Descripción del PLC", f"PLC Delta AS Series {len(plcs)+1}")
            plcs.append(plc)
        elif action == "eliminar" and plcs:
            if len(plcs) > 0:
                index = int(
                    get_input(f"Índice del PLC a eliminar (1-{len(plcs)})", "1")) - 1
                if 0 <= index < len(plcs):
                    removed = plcs.pop(index)
                    print(f"PLC {removed.get('id', 'Sin ID')} eliminado")
                else:
                    print("Índice inválido")
            else:
                print("No hay PLCs para eliminar")

    config["plcs"] = plcs
    return config


def main():
    """Función principal del asistente de configuración"""
    print("🧙‍♂️ Asistente de configuración del Gateway Local")
    print("=" * 50)

    # Cargar configuración existente o crear una nueva
    config = load_config()

    if config:
        print("Se ha encontrado una configuración existente.")
        if get_input("¿Desea usarla como base? (s/n)", "s").lower() != "s":
            config = {}
    else:
        print("Creando nueva configuración...")

    # Configurar cada sección
    config = configure_gateway(config)
    config = configure_wms(config)
    config = configure_network(config)
    config = configure_logging(config)
    config = configure_plcs(config)

    # Guardar configuración
    if save_config(config):
        print("\n✅ Configuración guardada exitosamente en 'gateway_config.json'")
        print("\n📝 Siguiente paso: Ejecute el gateway con:")
        if os.name == "nt":  # Windows
            print("   start_gateway.bat")
        else:  # Linux/Mac
            print("   ./start_gateway.sh")
    else:
        print("\n❌ Error guardando la configuración")
        return False

    return True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        sys.exit(1)
