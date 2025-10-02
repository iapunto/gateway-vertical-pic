#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Colector de métricas para el Gateway Local
"""

import time
import threading
from typing import Dict, Any, List, Optional
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry, REGISTRY
import json


class MetricsCollector:
    """Colector de métricas para el Gateway Local"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MetricsCollector, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Crear un registro personalizado para evitar conflictos
        self.registry = CollectorRegistry()

        # Métricas de sistema
        self.gateway_status = Gauge(
            'gateway_status', 'Estado del Gateway (1=running, 0=stopped)', registry=self.registry)
        self.plc_connections = Gauge(
            'plc_connections', 'Número de conexiones PLC activas', registry=self.registry)
        self.plc_connection_errors = Counter(
            'plc_connection_errors', 'Número de errores de conexión a PLCs', registry=self.registry)
        self.commands_sent = Counter(
            'commands_sent', 'Número de comandos enviados', ['plc_id', 'command'], registry=self.registry)
        self.command_duration = Histogram(
            'command_duration', 'Duración de comandos enviados', ['plc_id'], registry=self.registry)

        # Métricas de negocio
        self.position_changes = Counter(
            'position_changes', 'Número de cambios de posición', ['plc_id'], registry=self.registry)
        self.current_positions = Gauge(
            'current_positions', 'Posición actual de cada PLC', ['plc_id'], registry=self.registry)

        # Estado interno
        self.running = False
        self.metrics_thread = None
        self._initialized = True

    def start(self) -> None:
        """Inicia el colector de métricas"""
        self.running = True
        self.gateway_status.set(1)

        # Iniciar hilo de actualización de métricas
        self.metrics_thread = threading.Thread(
            target=self._metrics_worker, daemon=True)
        self.metrics_thread.start()

    def stop(self) -> None:
        """Detiene el colector de métricas"""
        self.running = False
        self.gateway_status.set(0)

        if self.metrics_thread and self.metrics_thread.is_alive():
            self.metrics_thread.join(timeout=5)

    def _metrics_worker(self) -> None:
        """Worker para actualización periódica de métricas"""
        while self.running:
            try:
                # Aquí se podrían actualizar métricas del sistema
                time.sleep(10)
            except Exception as e:
                print(f"Error en worker de métricas: {e}")
                time.sleep(5)

    def record_plc_connection(self, plc_id: str, connected: bool) -> None:
        """Registra el estado de conexión de un PLC"""
        if connected:
            self.plc_connections.inc()
        else:
            self.plc_connections.dec()

    def record_connection_error(self, plc_id: str) -> None:
        """Registra un error de conexión"""
        self.plc_connection_errors.inc()

    def record_command(self, plc_id: str, command: int, duration: float) -> None:
        """Registra un comando enviado"""
        self.commands_sent.labels(plc_id=plc_id, command=str(command)).inc()
        self.command_duration.labels(plc_id=plc_id).observe(duration)

    def record_position_change(self, plc_id: str, new_position: int) -> None:
        """Registra un cambio de posición"""
        self.position_changes.labels(plc_id=plc_id).inc()
        self.current_positions.labels(plc_id=plc_id).set(new_position)

    def get_metrics_text(self) -> str:
        """Obtiene las métricas en formato texto para Prometheus"""
        return generate_latest(self.registry).decode('utf-8')

    def get_metrics_json(self) -> Dict[str, Any]:
        """Obtiene las métricas en formato JSON"""
        # Esta es una implementación simplificada
        # En producción, se usaría una biblioteca de serialización de métricas
        return {
            "gateway_status": 1 if self.running else 0,
            "plc_connections": self.plc_connections._value.get(),
            "plc_connection_errors": self.plc_connection_errors._value.get(),
            "commands_sent": sum([child._value.get() for child in self.commands_sent._metrics.values()]),
            "position_changes": sum([child._value.get() for child in self.position_changes._metrics.values()])
        }


def get_metrics_collector() -> MetricsCollector:
    """Obtiene la instancia global del colector de métricas"""
    return MetricsCollector()
