#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de base de datos SQLite para el Gateway Local
"""

import sqlite3
import logging
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import threading

# Instancia global del gestor de base de datos
_database_manager_instance = None

def get_database_manager(db_path: str = "gateway.db") -> 'DatabaseManager':
    """Obtiene la instancia singleton del gestor de base de datos
    
    Args:
        db_path: Ruta al archivo de base de datos SQLite
        
    Returns:
        Instancia del DatabaseManager
    """
    global _database_manager_instance
    if _database_manager_instance is None:
        _database_manager_instance = DatabaseManager(db_path)
    return _database_manager_instance


class DatabaseManager:
    """Gestor de base de datos SQLite para el Gateway Local"""

    def __init__(self, db_path: str = "gateway.db"):
        """Inicializa el gestor de base de datos

        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._lock = threading.Lock()
        self._initialize_database()

    def _initialize_database(self):
        """Inicializa la base de datos y crea las tablas necesarias"""
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                # Crear tabla de PLCs
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS plcs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        plc_id TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        ip_address TEXT NOT NULL,
                        port INTEGER NOT NULL,
                        type TEXT NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Crear tabla de comandos
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS commands (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        plc_id TEXT NOT NULL,
                        command INTEGER NOT NULL,
                        argument INTEGER,
                        result TEXT,
                        success BOOLEAN,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (plc_id) REFERENCES plcs (plc_id)
                    )
                ''')

                # Crear tabla de eventos
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_type TEXT NOT NULL,
                        source TEXT NOT NULL,
                        data TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Crear tabla de configuraciones
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS configurations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        key TEXT UNIQUE NOT NULL,
                        value TEXT NOT NULL,
                        description TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Crear tabla de métricas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        metric_type TEXT NOT NULL,
                        plc_id TEXT,
                        value REAL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Crear índices para mejorar el rendimiento
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_commands_plc_id ON commands (plc_id)
                ''')

                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_commands_timestamp ON commands (timestamp)
                ''')

                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_events_type ON events (event_type)
                ''')

                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events (timestamp)
                ''')

                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_metrics_type ON metrics (metric_type)
                ''')

                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_metrics_plc_id ON metrics (plc_id)
                ''')

                conn.commit()
                conn.close()

                self.logger.info("Base de datos inicializada correctamente")

        except Exception as e:
            self.logger.error(f"Error inicializando base de datos: {e}")
            raise

    def add_plc(self, plc_id: str, name: str, ip_address: str, port: int,
                plc_type: str, description: Optional[str] = None) -> bool:
        """Agrega un nuevo PLC a la base de datos

        Args:
            plc_id: Identificador único del PLC
            name: Nombre descriptivo del PLC
            ip_address: Dirección IP del PLC
            port: Puerto del PLC
            plc_type: Tipo de PLC
            description: Descripción del PLC

        Returns:
            True si se agregó correctamente, False en caso contrario
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT OR REPLACE INTO plcs 
                    (plc_id, name, ip_address, port, type, description, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (plc_id, name, ip_address, port, plc_type, description))

                conn.commit()
                conn.close()

                self.logger.info(
                    f"PLC {plc_id} agregado/actualizado en la base de datos")
                return True

        except Exception as e:
            self.logger.error(f"Error agregando PLC {plc_id}: {e}")
            return False

    def update_plc(self, plc_id: str, name: str, ip_address: str, port: int,
                   plc_type: str, description: Optional[str] = None) -> bool:
        """Actualiza un PLC existente en la base de datos

        Args:
            plc_id: Identificador único del PLC
            name: Nombre descriptivo del PLC
            ip_address: Dirección IP del PLC
            port: Puerto del PLC
            plc_type: Tipo de PLC
            description: Descripción del PLC

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                cursor.execute('''
                    UPDATE plcs 
                    SET name = ?, ip_address = ?, port = ?, type = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE plc_id = ?
                ''', (name, ip_address, port, plc_type, description, plc_id))

                # Verificar si se actualizó algún registro
                rows_affected = cursor.rowcount
                conn.commit()
                conn.close()

                if rows_affected > 0:
                    self.logger.info(f"PLC {plc_id} actualizado en la base de datos")
                    return True
                else:
                    self.logger.warning(f"No se encontró el PLC {plc_id} para actualizar")
                    return False

        except Exception as e:
            self.logger.error(f"Error actualizando PLC {plc_id}: {e}")
            return False

    def get_plc(self, plc_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene la información de un PLC específico

        Args:
            plc_id: Identificador único del PLC

        Returns:
            Diccionario con la información del PLC o None si no se encuentra
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT * FROM plcs WHERE plc_id = ?
                ''', (plc_id,))

                row = cursor.fetchone()
                conn.close()

                if row:
                    return dict(row)
                else:
                    return None

        except Exception as e:
            self.logger.error(f"Error obteniendo PLC {plc_id}: {e}")
            return None

    def get_all_plcs(self) -> List[Dict[str, Any]]:
        """Obtiene todos los PLCs registrados

        Returns:
            Lista de diccionarios con la información de todos los PLCs
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT * FROM plcs ORDER BY name
                ''')

                rows = cursor.fetchall()
                conn.close()

                return [dict(row) for row in rows]

        except Exception as e:
            self.logger.error(f"Error obteniendo todos los PLCs: {e}")
            return []

    def remove_plc(self, plc_id: str) -> bool:
        """Elimina un PLC de la base de datos

        Args:
            plc_id: Identificador único del PLC

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                # Eliminar comandos asociados al PLC
                cursor.execute('''
                    DELETE FROM commands WHERE plc_id = ?
                ''', (plc_id,))

                # Eliminar métricas asociadas al PLC
                cursor.execute('''
                    DELETE FROM metrics WHERE plc_id = ?
                ''', (plc_id,))

                # Eliminar el PLC
                cursor.execute('''
                    DELETE FROM plcs WHERE plc_id = ?
                ''', (plc_id,))

                conn.commit()
                conn.close()

                self.logger.info(f"PLC {plc_id} eliminado de la base de datos")
                return True

        except Exception as e:
            self.logger.error(f"Error eliminando PLC {plc_id}: {e}")
            return False

    def add_command(self, plc_id: str, command: int, argument: Optional[int] = None,
                    result: Optional[Dict[str, Any]] = None, success: bool = True) -> bool:
        """Agrega un registro de comando ejecutado

        Args:
            plc_id: Identificador del PLC
            command: Código del comando
            argument: Argumento del comando (opcional)
            result: Resultado del comando (opcional)
            success: Indica si el comando fue exitoso

        Returns:
            True si se registró correctamente, False en caso contrario
        """
        try:
            result_json = json.dumps(result) if result else None

            with self._lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO commands 
                    (plc_id, command, argument, result, success, timestamp)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (plc_id, command, argument, result_json, success))

                conn.commit()
                conn.close()

                self.logger.debug(
                    f"Comando {command} registrado para PLC {plc_id}")
                return True

        except Exception as e:
            self.logger.error(
                f"Error registrando comando para PLC {plc_id}: {e}")
            return False

    def get_commands(self, plc_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtiene los comandos registrados

        Args:
            plc_id: Filtrar por PLC específico (opcional)
            limit: Número máximo de registros a devolver

        Returns:
            Lista de diccionarios con los comandos registrados
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                if plc_id:
                    cursor.execute('''
                        SELECT * FROM commands 
                        WHERE plc_id = ? 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    ''', (plc_id, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM commands 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    ''', (limit,))

                rows = cursor.fetchall()
                conn.close()

                # Convertir JSON de resultados
                commands = []
                for row in rows:
                    command_dict = dict(row)
                    if command_dict['result']:
                        try:
                            command_dict['result'] = json.loads(
                                command_dict['result'])
                        except json.JSONDecodeError:
                            pass  # Mantener el valor original si no se puede parsear
                    commands.append(command_dict)

                return commands

        except Exception as e:
            self.logger.error(f"Error obteniendo comandos: {e}")
            return []

    def add_event(self, event_type: str, source: str, data: Optional[Dict[str, Any]] = None) -> bool:
        """Agrega un registro de evento

        Args:
            event_type: Tipo de evento
            source: Fuente del evento
            data: Datos adicionales del evento (opcional)

        Returns:
            True si se registró correctamente, False en caso contrario
        """
        try:
            data_json = json.dumps(data) if data else None

            with self._lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO events 
                    (event_type, source, data, timestamp)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ''', (event_type, source, data_json))

                conn.commit()
                conn.close()

                self.logger.debug(
                    f"Evento {event_type} registrado desde {source}")
                return True

        except Exception as e:
            self.logger.error(f"Error registrando evento {event_type}: {e}")
            return False

    def get_events(self, event_type: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtiene los eventos registrados

        Args:
            event_type: Filtrar por tipo de evento (opcional)
            limit: Número máximo de registros a devolver

        Returns:
            Lista de diccionarios con los eventos registrados
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                if event_type:
                    cursor.execute('''
                        SELECT * FROM events 
                        WHERE event_type = ? 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    ''', (event_type, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM events 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    ''', (limit,))

                rows = cursor.fetchall()
                conn.close()

                # Convertir JSON de datos
                events = []
                for row in rows:
                    event_dict = dict(row)
                    if event_dict['data']:
                        try:
                            event_dict['data'] = json.loads(event_dict['data'])
                        except json.JSONDecodeError:
                            pass  # Mantener el valor original si no se puede parsear
                    events.append(event_dict)

                return events

        except Exception as e:
            self.logger.error(f"Error obteniendo eventos: {e}")
            return []

    def add_metric(self, metric_type: str, plc_id: Optional[str] = None,
                   value: float = 0.0) -> bool:
        """Agrega un registro de métrica

        Args:
            metric_type: Tipo de métrica
            plc_id: Identificador del PLC (opcional)
            value: Valor de la métrica

        Returns:
            True si se registró correctamente, False en caso contrario
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO metrics 
                    (metric_type, plc_id, value, timestamp)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ''', (metric_type, plc_id, value))

                conn.commit()
                conn.close()

                self.logger.debug(
                    f"Métrica {metric_type} registrada para PLC {plc_id}: {value}")
                return True

        except Exception as e:
            self.logger.error(f"Error registrando métrica {metric_type}: {e}")
            return False

    def get_metrics(self, metric_type: Optional[str] = None,
                    plc_id: Optional[str] = None, hours: int = 24) -> List[Dict[str, Any]]:
        """Obtiene los registros de métricas

        Args:
            metric_type: Filtrar por tipo de métrica (opcional)
            plc_id: Filtrar por PLC específico (opcional)
            hours: Horas hacia atrás para filtrar (por defecto 24)

        Returns:
            Lista de diccionarios con los registros de métricas
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # Construir consulta con filtros
                query = "SELECT * FROM metrics WHERE timestamp >= datetime('now', '-{} hours')".format(
                    hours)
                params = []

                if metric_type:
                    query += " AND metric_type = ?"
                    params.append(metric_type)

                if plc_id:
                    query += " AND plc_id = ?"
                    params.append(plc_id)

                query += " ORDER BY timestamp DESC"

                cursor.execute(query, params)

                rows = cursor.fetchall()
                conn.close()

                return [dict(row) for row in rows]

        except Exception as e:
            self.logger.error(f"Error obteniendo métricas: {e}")
            return []

    def get_database_stats(self) -> Dict[str, int]:
        """Obtiene estadísticas de la base de datos

        Returns:
            Diccionario con las estadísticas de la base de datos
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                # Contar registros en cada tabla
                cursor.execute("SELECT COUNT(*) FROM plcs")
                plcs_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM commands")
                commands_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM events")
                events_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM configurations")
                configurations_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM metrics")
                metrics_count = cursor.fetchone()[0]

                conn.close()

                return {
                    "plcs_count": plcs_count,
                    "commands_count": commands_count,
                    "events_count": events_count,
                    "configurations_count": configurations_count,
                    "metrics_count": metrics_count
                }

        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas: {e}")
            return {
                "plcs_count": 0,
                "commands_count": 0,
                "events_count": 0,
                "configurations_count": 0,
                "metrics_count": 0
            }

    def set_configuration(self, key: str, value: str, description: Optional[str] = None) -> bool:
        """Establece un valor de configuración

        Args:
            key: Clave de la configuración
            value: Valor de la configuración
            description: Descripción de la configuración (opcional)

        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT OR REPLACE INTO configurations 
                    (key, value, description, updated_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ''', (key, value, description))

                conn.commit()
                conn.close()

                self.logger.info(f"Configuración {key} guardada en la base de datos")
                return True

        except Exception as e:
            self.logger.error(f"Error guardando configuración {key}: {e}")
            return False

    def get_configuration(self, key: str) -> Optional[str]:
        """Obtiene un valor de configuración

        Args:
            key: Clave de la configuración

        Returns:
            Valor de la configuración o None si no se encuentra
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT value FROM configurations WHERE key = ?
                ''', (key,))

                row = cursor.fetchone()
                conn.close()

                if row:
                    return row['value']
                else:
                    return None

        except Exception as e:
            self.logger.error(f"Error obteniendo configuración {key}: {e}")
            return None

    def get_all_configurations(self) -> Dict[str, str]:
        """Obtiene todas las configuraciones

        Returns:
            Diccionario con todas las configuraciones
        """
        try:
            with self._lock:
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT key, value FROM configurations ORDER BY key
                ''')

                rows = cursor.fetchall()
                conn.close()

                return {row['key']: row['value'] for row in rows}

        except Exception as e:
            self.logger.error(f"Error obteniendo todas las configuraciones: {e}")
            return {}