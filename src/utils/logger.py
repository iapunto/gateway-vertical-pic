#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de logging para el Gateway Local
"""

import logging
import logging.handlers
import os
from typing import Optional, Dict, Any


class GatewayLogger:
    """Clase para manejar el logging del Gateway Local"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Inicializa el sistema de logging"""
        self.config = config or {}
        self.logger = logging.getLogger("gateway")
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configura el sistema de logging"""
        # Obtener configuración
        log_level_str = self.config.get("level", "INFO")
        log_file = self.config.get("file", "gateway.log")
        max_size = self.config.get("max_size", 10485760)  # 10MB
        backup_count = self.config.get("backup_count", 5)

        # Convertir nivel de log
        log_level = getattr(logging, str(log_level_str).upper(), logging.INFO)

        # Configurar logger
        self.logger.setLevel(log_level)

        # Evitar handlers duplicados
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Formato de log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Handler de archivo rotativo
        if log_file:
            # Crear directorio si no existe
            log_dir = os.path.dirname(str(log_file))
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            file_handler = logging.handlers.RotatingFileHandler(
                str(log_file),
                maxBytes=int(str(max_size)),
                backupCount=int(str(backup_count)),
                encoding='utf-8'
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Handler de consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Obtiene un logger para un módulo específico"""
        if name:
            return self.logger.getChild(name)
        return self.logger

    def set_level(self, level: str) -> None:
        """Establece el nivel de logging"""
        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        for handler in self.logger.handlers:
            handler.setLevel(log_level)


def setup_logger(config: Optional[Dict[str, Any]] = None) -> logging.Logger:
    """Función de conveniencia para configurar el logger"""
    gateway_logger = GatewayLogger(config)
    return gateway_logger.get_logger()


def log_event(logger: logging.Logger, event_type: str, message: str, **kwargs) -> None:
    """Función para registrar eventos estructurados en los logs"""
    # Crear mensaje de log con información adicional
    if kwargs:
        extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        log_message = f"{message} [{extra_info}]"
    else:
        log_message = message

    # Registrar el evento en el log
    logger.info(f"EVENT:{event_type} - {log_message}")
