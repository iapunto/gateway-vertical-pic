#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de gestión de eventos para el Gateway Local
"""

import threading
import time
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    """Representa un evento del sistema"""
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime
    source: str


class EventManager:
    """Gestor de eventos del sistema"""

    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        self._lock = threading.RLock()
        self._event_queue: List[Event] = []
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Inicia el gestor de eventos"""
        with self._lock:
            if not self._running:
                self._running = True
                self._worker_thread = threading.Thread(
                    target=self._event_worker, daemon=True)
                self._worker_thread.start()

    def stop(self) -> None:
        """Detiene el gestor de eventos"""
        with self._lock:
            self._running = False
            if self._worker_thread and self._worker_thread.is_alive():
                self._worker_thread.join(timeout=5)

    def subscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """Suscribe un callback a un tipo de evento"""
        with self._lock:
            if event_type not in self._listeners:
                self._listeners[event_type] = []
            self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """Elimina la suscripción de un callback a un tipo de evento"""
        with self._lock:
            if event_type in self._listeners:
                try:
                    self._listeners[event_type].remove(callback)
                except ValueError:
                    pass

    def emit(self, event_type: str, data: Dict[str, Any], source: str = "system") -> None:
        """Emite un evento"""
        event = Event(
            event_type=event_type,
            data=data,
            timestamp=datetime.now(),
            source=source
        )

        with self._lock:
            self._event_queue.append(event)

    def _event_worker(self) -> None:
        """Worker para procesar eventos en cola"""
        while self._running:
            try:
                event = None
                with self._lock:
                    if self._event_queue:
                        event = self._event_queue.pop(0)

                if event:
                    self._process_event(event)

                time.sleep(0.01)  # Pequeña pausa para no consumir CPU
            except Exception as e:
                print(f"Error en worker de eventos: {e}")
                time.sleep(1)

    def _process_event(self, event: Event) -> None:
        """Procesa un evento"""
        # Notificar a los listeners específicos del tipo de evento
        with self._lock:
            listeners = self._listeners.get(event.event_type, []).copy()

        # Notificar a los listeners generales
        with self._lock:
            general_listeners = self._listeners.get("*", []).copy()

        # Combinar listeners
        all_listeners = listeners + general_listeners

        # Notificar a todos los listeners
        for listener in all_listeners:
            try:
                listener(event)
            except Exception as e:
                print(
                    f"Error notificando listener para evento {event.event_type}: {e}")


# Instancia global del gestor de eventos
_event_manager = EventManager()


def get_event_manager() -> EventManager:
    """Obtiene la instancia global del gestor de eventos"""
    return _event_manager


def emit_event(event_type: str, data: Dict[str, Any], source: str = "system") -> None:
    """Emite un evento globalmente"""
    _event_manager.emit(event_type, data, source)


def subscribe_event(event_type: str, callback: Callable[[Event], None]) -> None:
    """Suscribe un callback a un tipo de evento globalmente"""
    _event_manager.subscribe(event_type, callback)


def unsubscribe_event(event_type: str, callback: Callable[[Event], None]) -> None:
    """Elimina la suscripción de un callback a un tipo de evento globalmente"""
    _event_manager.unsubscribe(event_type, callback)
