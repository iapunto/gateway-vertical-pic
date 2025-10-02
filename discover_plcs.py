#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de demostración para descubrir PLCs Vertical PIC en la red
"""

from src.plc.plc_discovery import PLCDiscovery
import sys
import os
import argparse
import json
import logging

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar el descubridor de PLCs


def setup_logging(verbose: bool = False):
    """Configura el logging para el script"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Función principal del script de descubrimiento"""
    parser = argparse.ArgumentParser(
        description="Descubrir PLCs Vertical PIC en la red",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Escanear toda la red local
  python discover_plcs.py
  
  # Escanear una subred específica
  python discover_plcs.py --subnet 192.168.1.0/24
  
  # Escanear un rango de IPs
  python discover_plcs.py --start-ip 192.168.1.10 --end-ip 192.168.1.50
  
  # Escanear con más hilos para mayor velocidad
  python discover_plcs.py --workers 100 --verbose
        """
    )

    parser.add_argument(
        '--subnet',
        help='Subred a escanear en formato CIDR (ej: 192.168.1.0/24)'
    )

    parser.add_argument(
        '--start-ip',
        help='Dirección IP inicial para escaneo de rango'
    )

    parser.add_argument(
        '--end-ip',
        help='Dirección IP final para escaneo de rango'
    )

    parser.add_argument(
        '--port',
        type=int,
        default=3200,
        help='Puerto donde escuchan los PLCs (por defecto: 3200)'
    )

    parser.add_argument(
        '--workers',
        type=int,
        default=50,
        help='Número de hilos para escaneo paralelo (por defecto: 50)'
    )

    parser.add_argument(
        '--output',
        help='Archivo de salida para guardar resultados (formato JSON)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mostrar información detallada de depuración'
    )

    args = parser.parse_args()

    # Configurar logging
    setup_logging(args.verbose)

    print("🔍 Descubridor de PLCs Vertical PIC")
    print("=" * 40)

    # Crear descubridor
    discovery = PLCDiscovery(port=args.port, timeout=2)

    # Realizar escaneo según los parámetros
    try:
        if args.subnet:
            print(f"Escaneando subred: {args.subnet}")
            results = discovery.quick_scan_subnet(args.subnet, args.workers)
        elif args.start_ip and args.end_ip:
            print(f"Escaneando rango: {args.start_ip} - {args.end_ip}")
            results = discovery.scan_ip_range(
                args.start_ip, args.end_ip, args.workers)
        else:
            print("Escaneando red local...")
            results = discovery.scan_local_network(args.workers)

        # Mostrar resultados
        print(f"\n✅ Escaneo completado. {len(results)} PLCs encontrados:")
        print("-" * 50)

        if results:
            for i, plc in enumerate(results, 1):
                print(f"{i:2d}. {plc['ip']}:{plc['port']}")
                print(f"     Tipo: {plc['type']}")
                print(f"     Estado: {plc['status']}")
                print(f"     Posición: {plc['position']}")
                print()
        else:
            print("No se encontraron PLCs en la red.")

        # Guardar resultados si se especificó archivo de salida
        if args.output:
            if discovery.save_discovery_results(results, args.output):
                print(f"💾 Resultados guardados en: {args.output}")
            else:
                print(f"❌ Error guardando resultados en: {args.output}")

    except KeyboardInterrupt:
        print("\n\n⚠️  Escaneo cancelado por el usuario")
        return 1
    except Exception as e:
        print(f"\n\n❌ Error durante el escaneo: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
