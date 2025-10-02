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
from utils.logger import setup_logger, log_event
from plc.plc_factory import PLCFactory
from interfaces.plc_interface import PLCInterface

# Importar el colector de métricas
from monitoring import get_metrics_collector

# Importar el gestor de eventos
from events import get_event_manager, emit_event

# Importar el cliente WMS
from wms.wms_client import WMSClient

# Importar el túnel reverso
from wms.reverse_tunnel import ReverseTunnel

# Importar el gestor de base de datos
from database import get_database_manager


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

        # Inicializar base de datos
        self.database_manager = get_database_manager()

        # Inicializar cliente WMS
        wms_config = self.config_manager.get("wms", {})
        self.wms_client: Optional[WMSClient] = None
        if wms_config and isinstance(wms_config, dict):
            endpoint = wms_config.get("endpoint")
            auth_token = wms_config.get("auth_token")
            if endpoint and auth_token and isinstance(endpoint, str) and isinstance(auth_token, str):
                self.wms_client = WMSClient(endpoint, auth_token)

        # Inicializar túnel reverso
        self.reverse_tunnel: Optional[ReverseTunnel] = None
        if wms_config and isinstance(wms_config, dict):
            endpoint = wms_config.get("endpoint")
            auth_token = wms_config.get("auth_token")
            gateway_id = self.config_manager.get("gateway.id", "unknown")
            if endpoint and auth_token and isinstance(gateway_id, str):
                self.reverse_tunnel = ReverseTunnel(
                    endpoint, auth_token, gateway_id)
                self.reverse_tunnel.set_command_callback(
                    self._handle_wms_command)

        # Configuración
        heartbeat_interval = self.config_manager.get(
            "wms.heartbeat_interval", 60)
        # Manejar diferentes tipos de retorno de configuración
        if isinstance(heartbeat_interval, (int, float, str)):
            self.heartbeat_interval = int(heartbeat_interval)
        else:
            self.heartbeat_interval = 60

        self.logger.info("Gateway Local inicializado")
        log_event(self.logger, "gateway.initialized",
                  "Gateway Local inicializado")

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
                name = plc_config.get("name", f"PLC {plc_id}")
                description = plc_config.get("description", "")

                if not all([plc_id, ip]):
                    self.logger.warning(
                        f"Configuración incompleta para PLC: {plc_config}")
                    continue

                try:
                    plc = PLCFactory.create_plc(plc_type, ip, port)
                    self.plcs[plc_id] = plc

                    # Guardar PLC en la base de datos
                    self.database_manager.add_plc(
                        plc_id=plc_id,
                        name=name,
                        ip_address=ip,
                        port=port,
                        plc_type=plc_type,
                        description=description
                    )

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

                    # Registrar evento en la base de datos
                    self.database_manager.add_event(
                        event_type="plc.connected",
                        source="gateway_core",
                        data={"plc_id": plc_id, "ip": plc_ip}
                    )
                else:
                    self.logger.error(f"Error conectando PLC {plc_id}")
                    self.metrics_collector.record_connection_error(plc_id)

                    # Emitir evento de error de conexión
                    emit_event("plc.connection_error", {
                        "plc_id": plc_id,
                        "error": "Connection failed"
                    }, "gateway_core")

                    # Registrar evento en la base de datos
                    self.database_manager.add_event(
                        event_type="plc.connection_error",
                        source="gateway_core",
                        data={"plc_id": plc_id, "error": "Connection failed"}
                    )
            except Exception as e:
                self.logger.error(f"Excepción conectando PLC {plc_id}: {e}")
                self.metrics_collector.record_connection_error(plc_id)

                # Emitir evento de excepción de conexión
                emit_event("plc.connection_exception", {
                    "plc_id": plc_id,
                    "error": str(e)
                }, "gateway_core")

                # Registrar evento en la base de datos
                self.database_manager.add_event(
                    event_type="plc.connection_exception",
                    source="gateway_core",
                    data={"plc_id": plc_id, "error": str(e)}
                )
        return success_count == len(self.plcs)

    def disconnect_plcs(self) -> None:
        """Desconecta todos los PLCs"""
        for plc_id, plc in self.plcs.items():
            try:
                plc.disconnect()
                self.logger.info(f"PLC {plc_id} desconectado")

                # Emitir evento de desconexión
                emit_event("plc.disconnected", {
                    "plc_id": plc_id
                }, "gateway_core")

                # Registrar evento en la base de datos
                self.database_manager.add_event(
                    event_type="plc.disconnected",
                    source="gateway_core",
                    data={"plc_id": plc_id}
                )
            except Exception as e:
                self.logger.error(f"Error desconectando PLC {plc_id}: {e}")

                # Emitir evento de error de desconexión
                emit_event("plc.disconnection_error", {
                    "plc_id": plc_id,
                    "error": str(e)
                }, "gateway_core")

                # Registrar evento en la base de datos
                self.database_manager.add_event(
                    event_type="plc.disconnection_error",
                    source="gateway_core",
                    data={"plc_id": plc_id, "error": str(e)}
                )

    def start(self) -> bool:
        """Inicia el Gateway Local"""
        if self.running:
            self.logger.warning("Gateway ya está iniciado")
            return True

        try:
            self.logger.info("Iniciando Gateway Local...")

            # Inicializar PLCs
            if not self.initialize_plcs():
                self.logger.error("Error inicializando PLCs")
                return False

            # Conectar PLCs
            if not self.connect_plcs():
                self.logger.error("Error conectando PLCs")
                return False

            # Iniciar túnel reverso si está configurado
            if self.reverse_tunnel:
                self.reverse_tunnel.start()

            # Iniciar hilos de monitoreo
            self._start_monitoring_threads()

            self.running = True
            self.logger.info("Gateway Local iniciado exitosamente")

            # Emitir evento de inicio
            emit_event("gateway.started", {}, "gateway_core")

            # Registrar evento en la base de datos
            self.database_manager.add_event(
                event_type="gateway.started",
                source="gateway_core",
                data={}
            )

            return True
        except Exception as e:
            self.logger.error(f"Error iniciando Gateway: {e}")

            # Emitir evento de error de inicio
            emit_event("gateway.start_error", {
                "error": str(e)
            }, "gateway_core")

            # Registrar evento en la base de datos
            self.database_manager.add_event(
                event_type="gateway.start_error",
                source="gateway_core",
                data={"error": str(e)}
            )

            return False

    def stop(self) -> None:
        """Detiene el Gateway Local"""
        if not self.running:
            self.logger.warning("Gateway ya está detenido")
            return

        self.logger.info("Deteniendo Gateway Local...")
        self.running = False

        # Detener hilos
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=5)

        # Detener túnel reverso
        if self.reverse_tunnel:
            self.reverse_tunnel.stop()

        # Desconectar PLCs
        self.disconnect_plcs()

        self.logger.info("Gateway Local detenido")

        # Emitir evento de detención
        emit_event("gateway.stopped", {}, "gateway_core")

        # Registrar evento en la base de datos
        self.database_manager.add_event(
            event_type="gateway.stopped",
            source="gateway_core",
            data={}
        )

    def _start_monitoring_threads(self) -> None:
        """Inicia los hilos de monitoreo"""
        # Hilo de heartbeat
        heartbeat_thread = threading.Thread(
            target=self._heartbeat_worker, daemon=True)
        heartbeat_thread.start()
        self.threads.append(heartbeat_thread)

        # Hilo de monitoreo de PLCs
        plc_monitor_thread = threading.Thread(
            target=self._plc_monitor_worker, daemon=True)
        plc_monitor_thread.start()
        self.threads.append(plc_monitor_thread)

    def _heartbeat_worker(self) -> None:
        """Worker para enviar heartbeats al WMS"""
        while self.running:
            try:
                if self.wms_client:
                    status = self.get_status()
                    self.wms_client.send_heartbeat(status)

                    # Registrar métrica
                    self.metrics_collector.record_connection_error(
                        "heartbeat")  # Usar método existente

                    # Registrar evento en la base de datos
                    self.database_manager.add_event(
                        event_type="gateway.heartbeat",
                        source="gateway_core",
                        data={"status": status}
                    )
            except Exception as e:
                self.logger.error(f"Error enviando heartbeat: {e}")

                # Emitir evento de error de heartbeat
                emit_event("gateway.heartbeat_error", {
                    "error": str(e)
                }, "gateway_core")

                # Registrar evento en la base de datos
                self.database_manager.add_event(
                    event_type="gateway.heartbeat_error",
                    source="gateway_core",
                    data={"error": str(e)}
                )

            time.sleep(self.heartbeat_interval)

    def _plc_monitor_worker(self) -> None:
        """Worker para monitorear el estado de los PLCs"""
        while self.running:
            try:
                for plc_id, plc in self.plcs.items():
                    if plc.is_connected():
                        # Obtener estado del PLC
                        status = plc.get_status()

                        # Registrar métrica
                        if "response_time" in status:
                            self.metrics_collector.record_command(
                                # Usar método existente
                                plc_id, 0, status["response_time"])

                        # Registrar comando en la base de datos
                        self.database_manager.add_command(
                            plc_id=plc_id,
                            command=0,  # STATUS command
                            result=status
                        )

                        # Emitir evento de estado de PLC
                        emit_event("plc.status_update", {
                            "plc_id": plc_id,
                            "status": status
                        }, "gateway_core")

                        # Registrar evento en la base de datos
                        self.database_manager.add_event(
                            event_type="plc.status_update",
                            source="gateway_core",
                            data={"plc_id": plc_id, "status": status}
                        )
            except Exception as e:
                self.logger.error(f"Error monitoreando PLCs: {e}")

                # Emitir evento de error de monitoreo
                emit_event("gateway.plc_monitor_error", {
                    "error": str(e)
                }, "gateway_core")

                # Registrar evento en la base de datos
                self.database_manager.add_event(
                    event_type="gateway.plc_monitor_error",
                    source="gateway_core",
                    data={"error": str(e)}
                )

            time.sleep(10)  # Monitorear cada 10 segundos

    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado completo del gateway"""
        plc_statuses = {}
        for plc_id, plc in self.plcs.items():
            try:
                if plc.is_connected():
                    status = plc.get_status()
                    plc_statuses[plc_id] = {
                        "connected": True,
                        "status": status
                    }
                else:
                    plc_statuses[plc_id] = {
                        "connected": False,
                        "error": "Not connected"
                    }
            except Exception as e:
                plc_statuses[plc_id] = {
                    "connected": False,
                    "error": str(e)
                }

        return {
            "gateway": {
                "id": self.config_manager.get("gateway.id", "unknown"),
                "name": self.config_manager.get("gateway.name", "Gateway Local"),
                "version": self.config_manager.get("gateway.version", "1.0.0"),
                "running": self.running
            },
            "plcs": plc_statuses,
            "timestamp": time.time()
        }

    def send_command(self, command: str, argument: Optional[Any] = None,
                     plc_id: Optional[str] = None) -> Dict[str, Any]:
        """Envía un comando a uno o todos los PLCs"""
        results = {}

        # Determinar PLCs objetivo
        target_plcs = []
        if plc_id:
            if plc_id in self.plcs:
                target_plcs = [(plc_id, self.plcs[plc_id])]
            else:
                return {"success": False, "error": f"PLC {plc_id} no encontrado"}
        else:
            target_plcs = list(self.plcs.items())

        # Enviar comando a cada PLC
        for target_id, plc in target_plcs:
            try:
                if not plc.is_connected():
                    results[target_id] = {
                        "success": False,
                        "error": "PLC no conectado"
                    }
                    continue

                # Mapear comando a código numérico
                command_map = {
                    "STATUS": 0,
                    "MOVE": 1,
                    "START": 2,
                    "STOP": 3,
                    "RESET": 4
                }

                if command not in command_map:
                    results[target_id] = {
                        "success": False,
                        "error": f"Comando {command} no soportado"
                    }
                    continue

                command_code = command_map[command]

                # Enviar comando
                if argument is not None:
                    result = plc.send_command(command_code, argument)
                else:
                    result = plc.send_command(command_code)

                results[target_id] = result

                # Registrar comando en la base de datos
                self.database_manager.add_command(
                    plc_id=target_id,
                    command=command_code,
                    argument=argument if isinstance(argument, int) else None,
                    result=result,
                    success=result.get("success", False)
                )

                # Registrar métrica
                if "response_time" in result:
                    self.metrics_collector.record_command(
                        target_id, command_code, result["response_time"])

                # Emitir evento de comando
                emit_event("plc.command_sent", {
                    "plc_id": target_id,
                    "command": command,
                    "argument": argument,
                    "result": result
                }, "gateway_core")

                # Registrar evento en la base de datos
                self.database_manager.add_event(
                    event_type="plc.command_sent",
                    source="gateway_core",
                    data={
                        "plc_id": target_id,
                        "command": command,
                        "argument": argument,
                        "result": result
                    }
                )
            except Exception as e:
                error_msg = f"Error enviando comando {command} a PLC {target_id}: {e}"
                self.logger.error(error_msg)
                results[target_id] = {"success": False, "error": str(e)}

                # Emitir evento de error de comando
                emit_event("plc.command_error", {
                    "plc_id": target_id,
                    "command": command,
                    "error": str(e)
                }, "gateway_core")

                # Registrar evento en la base de datos
                self.database_manager.add_event(
                    event_type="plc.command_error",
                    source="gateway_core",
                    data={
                        "plc_id": target_id,
                        "command": command,
                        "error": str(e)
                    }
                )

        return {
            "success": True,
            "results": results
        }

    def move_to_position(self, position: int, plc_id: Optional[str] = None) -> Dict[str, Any]:
        """Mueve uno o todos los PLCs a una posición específica"""
        return self.send_command("MOVE", position, plc_id)

    def _handle_wms_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja comandos recibidos desde el WMS a través del túnel reverso"""
        try:
            command = command_data.get("command")
            argument = command_data.get("argument")
            plc_id = command_data.get("plc_id")

            self.logger.info(
                f"Comando recibido desde WMS: {command} ({argument}) para PLC {plc_id}")

            # Registrar evento en la base de datos
            self.database_manager.add_event(
                event_type="wms.command_received",
                source="gateway_core",
                data=command_data
            )

            # Ejecutar comando
            result = self.send_command(command or "", argument, plc_id)

            # Emitir evento de comando WMS procesado
            emit_event("wms.command_processed", {
                "command": command,
                "argument": argument,
                "plc_id": plc_id,
                "result": result
            }, "gateway_core")

            # Registrar evento en la base de datos
            self.database_manager.add_event(
                event_type="wms.command_processed",
                source="gateway_core",
                data={
                    "command": command,
                    "argument": argument,
                    "plc_id": plc_id,
                    "result": result
                }
            )

            return result
        except Exception as e:
            error_msg = f"Error procesando comando WMS: {e}"
            self.logger.error(error_msg)

            # Emitir evento de error de comando WMS
            emit_event("wms.command_error", {
                "error": str(e),
                "command_data": command_data
            }, "gateway_core")

            # Registrar evento en la base de datos
            self.database_manager.add_event(
                event_type="wms.command_error",
                source="gateway_core",
                data={
                    "error": str(e),
                    "command_data": command_data
                }
            )

            return {"success": False, "error": str(e)}
