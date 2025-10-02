#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada principal para el Gateway Local
"""

# Corregir la importación
from core.gateway_core import GatewayCore
import sys
import os
import signal
import time

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def signal_handler(sig, frame):
    """Manejador de señales para cierre limpio"""
    print("\nRecibida señal de interrupción. Cerrando Gateway...")
    if 'gateway' in globals():
        gateway.stop()
    sys.exit(0)


def main():
    """Función principal del Gateway Local"""
    # Registrar manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Iniciando Gateway Local...")

    # Crear e iniciar el gateway
    global gateway
    gateway = GatewayCore()

    try:
        if gateway.start():
            print("Gateway Local iniciado exitosamente")
            print("Presione Ctrl+C para detener")

            # Mantener el proceso vivo
            while True:
                time.sleep(1)
        else:
            print("Error iniciando Gateway Local")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nInterrupción por teclado recibida")
    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)
    finally:
        if 'gateway' in globals():
            gateway.stop()
        print("Gateway Local detenido")


if __name__ == "__main__":
    main()
