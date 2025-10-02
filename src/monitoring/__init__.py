#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paquete de monitoreo para el Gateway Local
"""

# Versión del paquete
__version__ = "1.0.0"

# Importaciones públicas
from .metrics_collector import MetricsCollector, get_metrics_collector

__all__ = ["MetricsCollector", "get_metrics_collector"]
