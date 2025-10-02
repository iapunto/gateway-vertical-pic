#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paquete de gestión de eventos para el Gateway Local
"""

# Versión del paquete
__version__ = "1.0.0"

# Importaciones públicas
from .event_manager import EventManager, Event, get_event_manager, emit_event, subscribe_event, unsubscribe_event

__all__ = ["EventManager", "Event", "get_event_manager",
           "emit_event", "subscribe_event", "unsubscribe_event"]
