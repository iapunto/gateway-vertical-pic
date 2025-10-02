#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Colector de métricas para el Gateway Local
"""

import time
import threading
from typing import Dict, Any, List, Optional
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import json


class MetricsCollector:
    """Colector de métricas para el Gateway Local"""

    def __init__(self):
        # Métricas de sistema
        self.gateway_status = Gauge(
            'gateway_status', 'Estado del Gateway (1=running, 0=stopped)')
        self.plc_connections = Gauge(
            'plc_connections', 'Número de conexiones PLC activas')
        self.plc_connection_errors = Counter(
            'plc_connection_errors', 'Número de errores de conexión a PLCs')
        self.commands_sent = Counter(
            'commands_sent', 'Número de comandos enviados', ['plc_id', 'command'])
        self.command_duration = Histogram(
            'command_duration', 'Duración de comandos enviados', ['plc_id'])

        # Métricas de negocio
        self.position_changes = Counter(
            'position_changes', 'Número de cambios de posición', ['plc_id'])
        self.current_positions = Gauge(
            'current_positions', 'Posición actual de cada PLC', ['plc_id'])

        # Estado interno
        self.running = False
        self.metrics_thread = None

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
        return generate_latest().decode('utf-8')

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


# Instancia global del colector de métricas
metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Obtiene la instancia global del colector de métricas"""
    return metrics_collector
