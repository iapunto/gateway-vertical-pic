#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada principal para el Gateway Local
"""

from core.gateway_core import GatewayCore
import sys
import os
import signal
import time
import argparse
from typing import Optional

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def signal_handler(sig, frame):
    """Manejador de señales para cierre limpio"""
    print("\nRecibida señal de interrupción. Cerrando Gateway...")
    if 'gateway' in globals():
        gateway.stop()
    sys.exit(0)


def run_standalone():
    """Ejecuta el gateway en modo standalone"""
    global gateway

    # Registrar manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Iniciando Gateway Local en modo standalone...")

    # Crear e iniciar el gateway
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


def run_with_api(host: Optional[str] = None, port: Optional[int] = None, debug: bool = False):
    """Ejecuta el gateway con API REST"""
    try:
        # Importar la API (solo si se necesita)
        from api.gateway_api import GatewayAPI

        print("Iniciando Gateway Local con API REST...")

        # Crear la API
        api = GatewayAPI()

        # Registrar manejador de señales
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Iniciar la API
        api.run(host, port, debug)

    except ImportError as e:
        print(f"Error importando API: {e}")
        print("Asegúrese de tener Flask instalado: pip install flask")
        sys.exit(1)
    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)


def main():
    """Función principal del Gateway Local"""
    parser = argparse.ArgumentParser(
        description="Gateway Local para comunicación con PLCs")
    parser.add_argument("--api", action="store_true",
                        help="Ejecutar con API REST")
    parser.add_argument("--host", default=None,
                        help="Dirección IP para la API")
    parser.add_argument("--port", type=int, default=None,
                        help="Puerto para la API")
    parser.add_argument("--debug", action="store_true",
                        help="Modo debug para la API")

    args = parser.parse_args()

    if args.api:
        run_with_api(args.host if args.host else None,
                     args.port if args.port else None, args.debug)
    else:
        run_standalone()


if __name__ == "__main__":
    main()
