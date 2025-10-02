#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core del Gateway Local - Orquestador principal
"""

import logging
import threading
import time
from typing import Dict, Any, List, Optional

# Corregir las importaciones
from config.config_manager import ConfigManager
from utils.logger import setup_logger
from plc.plc_factory import PLCFactory
from interfaces.plc_interface import PLCInterface

# Importar el colector de métricas
from monitoring import get_metrics_collector

# Importar el gestor de eventos
from events import get_event_manager, emit_event


class GatewayCore:
    """Clase principal del Gateway Local"""

    def __init__(self, config_file: str = "gateway_config.json"):
        """Inicializa el Gateway Local"""
        self.config_manager = ConfigManager(config_file)
        self.logger = setup_logger(self.config_manager.get("logging", {}))
        self.plcs: Dict[str, PLCInterface] = {}
        self.running = False
        self.threads: List[threading.Thread] = []

        # Inicializar colector de métricas
        self.metrics_collector = get_metrics_collector()

        # Inicializar gestor de eventos
        self.event_manager = get_event_manager()

        # Configuración
        heartbeat_interval = self.config_manager.get(
            "wms.heartbeat_interval", 60)
        # Manejar diferentes tipos de retorno de configuración
        if isinstance(heartbeat_interval, (int, float, str)):
            self.heartbeat_interval = int(heartbeat_interval)
        else:
            self.heartbeat_interval = 60

        self.logger.info("Gateway Local inicializado")

    def initialize_plcs(self) -> bool:
        """Inicializa todos los PLCs configurados"""
        try:
            plc_configs = self.config_manager.get_plc_list()
            self.logger.info(f"Inicializando {len(plc_configs)} PLCs")

            for plc_config in plc_configs:
                plc_id = plc_config.get("id")
                plc_type = plc_config.get("type", "delta")
                ip = plc_config.get("ip")
                port = plc_config.get("port", 3200)

                if not all([plc_id, ip]):
                    self.logger.warning(
                        f"Configuración incompleta para PLC: {plc_config}")
                    continue

                try:
                    plc = PLCFactory.create_plc(plc_type, ip, port)
                    self.plcs[plc_id] = plc
                    self.logger.info(
                        f"PLC {plc_id} ({plc_type}) inicializado: {ip}:{port}")

                    # Emitir evento de inicialización de PLC
                    emit_event("plc.initialized", {
                        "plc_id": plc_id,
                        "type": plc_type,
                        "ip": ip,
                        "port": port
                    }, "gateway_core")
                except Exception as e:
                    self.logger.error(f"Error inicializando PLC {plc_id}: {e}")
                    emit_event("plc.initialization_error", {
                        "plc_id": plc_id,
                        "error": str(e)
                    }, "gateway_core")
                    return False

            return True
        except Exception as e:
            self.logger.error(f"Error inicializando PLCs: {e}")
            emit_event("gateway.initialization_error", {
                "error": str(e)
            }, "gateway_core")
            return False

    def connect_plcs(self) -> bool:
        """Conecta todos los PLCs inicializados"""
        success_count = 0
        for plc_id, plc in self.plcs.items():
            try:
                if plc.connect():
                    self.logger.info(f"PLC {plc_id} conectado exitosamente")
                    self.metrics_collector.record_plc_connection(plc_id, True)
                    success_count += 1

                    # Obtener IP del PLC si está disponible
                    plc_ip = getattr(plc, 'ip', 'unknown')
                    # Emitir evento de conexión exitosa
                    emit_event("plc.connected", {
                        "plc_id": plc_id,
                        "ip": plc_ip
                    }, "gateway_core")
                else:
                    self.logger.error(f"Error conectando PLC {plc_id}")
                    self.metrics_collector.record_connection_error(plc_id)

                    # Emitir evento de error de conexión
                    emit_event("plc.connection_error", {
                        "plc_id": plc_id,
                        "error": "Connection failed"
                    }, "gateway_core")
            except Exception as e:
                self.logger.error(f"Excepción conectando PLC {plc_id}: {e}")
                self.metrics_collector.record_connection_error(plc_id)

                # Emitir evento de excepción de conexión
                emit_event("plc.connection_exception", {
                    "plc_id": plc_id,
                    "error": str(e)
                }, "gateway_core")

        return success_count == len(self.plcs)

    def start(self) -> bool:
        """Inicia el Gateway Local"""
        self.logger.info("Iniciando Gateway Local...")

        # Iniciar gestor de eventos
        self.event_manager.start()

        # Iniciar colector de métricas
        self.metrics_collector.start()

        # Inicializar PLCs
        if not self.initialize_plcs():
            self.logger.error("Error inicializando PLCs")
            return False

        # Conectar PLCs
        if not self.connect_plcs():
            self.logger.error("Error conectando PLCs")
            return False

        self.running = True

        # Iniciar hilos de trabajo
        self._start_heartbeat_thread()
        self._start_monitoring_thread()

        # Emitir evento de inicio del gateway
        emit_event("gateway.started", {
            "plc_count": len(self.plcs)
        }, "gateway_core")

        self.logger.info("Gateway Local iniciado exitosamente")
        return True

    def stop(self) -> None:
        """Detiene el Gateway Local"""
        self.logger.info("Deteniendo Gateway Local...")
        self.running = False

        # Emitir evento de detención del gateway
        emit_event("gateway.stopping", {}, "gateway_core")

        # Detener colector de métricas
        self.metrics_collector.stop()

        # Detener gestor de eventos
        self.event_manager.stop()

        # Desconectar todos los PLCs
        for plc_id, plc in self.plcs.items():
            try:
                plc.disconnect()
                self.logger.info(f"PLC {plc_id} desconectado")
                self.metrics_collector.record_plc_connection(plc_id, False)

                # Emitir evento de desconexión
                emit_event("plc.disconnected", {
                    "plc_id": plc_id
                }, "gateway_core")
            except Exception as e:
                self.logger.error(f"Error desconectando PLC {plc_id}: {e}")

        # Esperar a que terminen los hilos
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=5)

        self.logger.info("Gateway Local detenido")

    def _start_heartbeat_thread(self) -> None:
        """Inicia el hilo de heartbeat"""
        heartbeat_thread = threading.Thread(
            target=self._heartbeat_worker, daemon=True)
        heartbeat_thread.start()
        self.threads.append(heartbeat_thread)
        self.logger.info("Hilo de heartbeat iniciado")

    def _start_monitoring_thread(self) -> None:
        """Inicia el hilo de monitoreo"""
        monitoring_thread = threading.Thread(
            target=self._monitoring_worker, daemon=True)
        monitoring_thread.start()
        self.threads.append(monitoring_thread)
        self.logger.info("Hilo de monitoreo iniciado")

    def _heartbeat_worker(self) -> None:
        """Worker para enviar heartbeat"""
        while self.running:
            try:
                # TODO: Implementar envío real de heartbeat al WMS
                self.logger.debug("Enviando heartbeat...")
                time.sleep(float(self.heartbeat_interval))
            except Exception as e:
                self.logger.error(f"Error en worker de heartbeat: {e}")
                time.sleep(5.0)

    def _monitoring_worker(self) -> None:
        """Worker para monitoreo de PLCs"""
        while self.running:
            try:
                # TODO: Implementar monitoreo real de PLCs
                self.logger.debug("Monitoreando PLCs...")
                time.sleep(10.0)
            except Exception as e:
                self.logger.error(f"Error en worker de monitoreo: {e}")
                time.sleep(5.0)

    def get_plc_status(self, plc_id: str) -> Dict[str, Any]:
        """Obtiene el estado de un PLC específico"""
        if plc_id not in self.plcs:
            error_msg = f"PLC {plc_id} no encontrado"
            emit_event("plc.not_found", {
                "plc_id": plc_id,
                "error": error_msg
            }, "gateway_core")
            return {"error": error_msg, "success": False}

        try:
            plc = self.plcs[plc_id]
            status = plc.get_status()

            # Emitir evento de consulta de estado
            emit_event("plc.status_queried", {
                "plc_id": plc_id,
                "connected": plc.is_connected(),
                "status": status
            }, "gateway_core")

            return {
                "plc_id": plc_id,
                "connected": plc.is_connected(),
                "status": status,
                "success": True
            }
        except Exception as e:
            self.logger.error(f"Error obteniendo estado de PLC {plc_id}: {e}")
            emit_event("plc.status_error", {
                "plc_id": plc_id,
                "error": str(e)
            }, "gateway_core")
            return {"error": str(e), "success": False}

    def send_plc_command(self, plc_id: str, command: int, argument: Optional[int] = None) -> Dict[str, Any]:
        """Envía un comando a un PLC específico"""
        if plc_id not in self.plcs:
            error_msg = f"PLC {plc_id} no encontrado"
            emit_event("plc.not_found", {
                "plc_id": plc_id,
                "error": error_msg
            }, "gateway_core")
            return {"error": error_msg, "success": False}

        start_time = time.time()
        try:
            plc = self.plcs[plc_id]
            if not plc.is_connected():
                if not plc.connect():
                    error_msg = "No se pudo conectar al PLC"
                    emit_event("plc.connection_failed", {
                        "plc_id": plc_id,
                        "error": error_msg
                    }, "gateway_core")
                    return {"error": error_msg, "success": False}

            result = plc.send_command(command, argument)

            # Registrar métricas
            duration = time.time() - start_time
            self.metrics_collector.record_command(plc_id, command, duration)

            # Si es un comando de movimiento, registrar el cambio de posición
            if command == 1 and argument is not None:  # MUEVETE
                self.metrics_collector.record_position_change(plc_id, argument)

            # Emitir evento de comando enviado
            emit_event("plc.command_sent", {
                "plc_id": plc_id,
                "command": command,
                "argument": argument,
                "result": result,
                "duration": duration
            }, "gateway_core")

            return {
                "plc_id": plc_id,
                "command": command,
                "argument": argument,
                "result": result,
                "success": result.get("success", False)
            }
        except Exception as e:
            self.logger.error(f"Error enviando comando a PLC {plc_id}: {e}")
            emit_event("plc.command_error", {
                "plc_id": plc_id,
                "command": command,
                "argument": argument,
                "error": str(e)
            }, "gateway_core")
            return {"error": str(e), "success": False}
