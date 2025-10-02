#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de demostración del Gateway Local
"""

import sys
import os
import time
import requests
import json
from typing import Dict, Any

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def demo_events():
    """Demostración del sistema de eventos"""
    print("=== Demostración del Sistema de Eventos ===")

    try:
        # Importar usando rutas relativas
        events_module = __import__('events.event_manager', fromlist=[
                                   'subscribe_event', 'emit_event'])
        subscribe_event = getattr(events_module, 'subscribe_event')
        emit_event = getattr(events_module, 'emit_event')

        # Callback para eventos de PLC
        def plc_event_handler(event):
            print(f"EVENTO PLC: {event.event_type} - {event.data}")

        # Callback para eventos generales
        def general_event_handler(event):
            print(f"EVENTO GENERAL: {event.event_type} - {event.data}")

        # Suscribir a eventos específicos
        subscribe_event("plc.*", plc_event_handler)
        subscribe_event("*", general_event_handler)

        # Emitir algunos eventos de prueba
        emit_event("plc.initialized", {
                   "plc_id": "DEMO-PLC-001", "type": "delta"})
        emit_event("plc.connected", {
                   "plc_id": "DEMO-PLC-001", "ip": "192.168.1.100"})
        emit_event("gateway.started", {"plc_count": 1})

        print("Eventos demostrados\n")
    except ImportError as e:
        print(f"Error importando módulos de eventos: {e}\n")


def demo_health_check():
    """Demostración del sistema de salud"""
    print("=== Demostración del Sistema de Salud ===")

    try:
        # Importar usando rutas relativas
        core_module = __import__('core.gateway_core', fromlist=['GatewayCore'])
        GatewayCore = getattr(core_module, 'GatewayCore')

        health_module = __import__(
            'health.health_checker', fromlist=['HealthChecker'])
        HealthChecker = getattr(health_module, 'HealthChecker')

        # Crear un gateway de demostración
        gateway = GatewayCore()

        # Crear health checker
        health_checker = HealthChecker(gateway)

        # Obtener estado de salud
        health_status = health_checker.get_health_status()
        print(f"Estado de salud: {health_status['status']}")
        print(f"Timestamp: {health_status['timestamp']}")

        # Mostrar detalles de cada check
        for check in health_status['checks']:
            print(f"  {check['name']}: {check['status']} - {check['message']}")

        print("Sistema de salud demostrado\n")
    except ImportError as e:
        print(f"Error importando módulos de salud: {e}\n")


def demo_metrics():
    """Demostración del sistema de métricas"""
    print("=== Demostración del Sistema de Métricas ===")

    try:
        # Importar usando rutas relativas
        monitoring_module = __import__('monitoring.metrics_collector', fromlist=[
                                       'get_metrics_collector'])
        get_metrics_collector = getattr(
            monitoring_module, 'get_metrics_collector')

        # Obtener colector de métricas
        metrics_collector = get_metrics_collector()

        # Registrar algunas métricas de demostración
        metrics_collector.record_plc_connection("DEMO-PLC-001", True)
        metrics_collector.record_command("DEMO-PLC-001", 1, 0.123)
        metrics_collector.record_position_change("DEMO-PLC-001", 5)

        # Obtener métricas en formato JSON
        metrics_json = metrics_collector.get_metrics_json()
        print("Métricas en formato JSON:")
        print(json.dumps(metrics_json, indent=2))

        print("Sistema de métricas demostrado\n")
    except ImportError as e:
        print(f"Error importando módulos de métricas: {e}\n")


def demo_api_calls():
    """Demostración de llamadas a la API"""
    print("=== Demostración de Llamadas a la API ===")

    # Nota: Esta demostración requiere que la API esté corriendo
    base_url = "http://localhost:8080"

    try:
        # Verificar salud del sistema
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"  Estado: {health_data['status']}")

        # Obtener métricas
        response = requests.get(f"{base_url}/metrics", timeout=5)
        print(f"Métricas: {response.status_code}")
        if response.status_code == 200:
            print(f"  Contenido: {len(response.text)} bytes")

    except requests.exceptions.RequestException as e:
        print(f"  No se pudo conectar a la API: {e}")
        print("  Asegúrate de que la API esté corriendo con: python src/main.py --api")

    print("Llamadas a la API demostradas\n")


def demo_gateway_functionality():
    """Demostración de funcionalidad del gateway"""
    print("=== Demostración de Funcionalidad del Gateway ===")

    try:
        # Importar usando rutas relativas
        core_module = __import__('core.gateway_core', fromlist=['GatewayCore'])
        GatewayCore = getattr(core_module, 'GatewayCore')

        # Crear gateway
        gateway = GatewayCore()

        # Mostrar información de configuración
        gateway_id = gateway.config_manager.get("gateway.id", "unknown")
        gateway_name = gateway.config_manager.get("gateway.name", "unknown")
        print(f"Gateway ID: {gateway_id}")
        print(f"Gateway Name: {gateway_name}")

        # Mostrar PLCs configurados
        plcs = gateway.config_manager.get_plc_list()
        print(f"PLCs configurados: {len(plcs)}")
        for plc in plcs:
            print(
                f"  - {plc.get('id', 'unknown')}: {plc.get('ip', 'unknown')}:{plc.get('port', 3200)}")

        print("Funcionalidad del gateway demostrada\n")
    except ImportError as e:
        print(f"Error importando módulos del gateway: {e}\n")


def main():
    """Función principal de demostración"""
    print("🚀 Demostración del Gateway Local")
    print("=" * 50)

    # Ejecutar todas las demostraciones
    demo_events()
    demo_health_check()
    demo_metrics()
    demo_gateway_functionality()
    demo_api_calls()

    print("🎉 ¡Demostración completada!")
    print("\nPara probar la API REST:")
    print("  1. Ejecuta: python src/main.py --api")
    print("  2. En otra terminal, ejecuta: python demo.py")


if __name__ == "__main__":
    main()
