#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de uso del descubrimiento de PLCs
"""

from src.plc.plc_discovery import PLCDiscovery, discover_plcs_on_network
import sys
import os

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def main():
    """Ejemplo de uso del descubrimiento de PLCs"""

    print("Ejemplo de descubrimiento de PLCs Vertical PIC")
    print("=" * 50)

    # Crear instancia del descubridor
    discovery = PLCDiscovery(port=3200, timeout=2)

    # Ejemplo 1: Escanear una subred específica
    print("1. Escaneando subred 192.168.1.0/24...")
    plcs = discovery.quick_scan_subnet("192.168.1.0/24", max_workers=20)

    print(f"   PLCs encontrados: {len(plcs)}")
    for plc in plcs:
        print(f"   - {plc['ip']}:{plc['port']} - {plc['type']}")

    # Ejemplo 2: Escanear un rango de IPs
    print("\n2. Escaneando rango 192.168.0.100 - 192.168.0.110...")
    plcs = discovery.scan_ip_range(
        "192.168.0.100", "192.168.0.110", max_workers=10)

    print(f"   PLCs encontrados: {len(plcs)}")
    for plc in plcs:
        print(f"   - {plc['ip']}:{plc['port']} - {plc['type']}")

    # Ejemplo 3: Escanear toda la red local (puede tomar más tiempo)
    print("\n3. Escaneando toda la red local...")
    plcs = discovery.scan_local_network(max_workers=30)

    print(f"   PLCs encontrados: {len(plcs)}")
    for plc in plcs:
        print(f"   - {plc['ip']}:{plc['port']} - {plc['type']}")

    # Ejemplo 4: Guardar resultados en archivo
    print("\n4. Guardando resultados en archivo...")
    discovery.save_discovery_results(plcs, "plcs_descubiertos.json")
    print("   Resultados guardados en plcs_descubiertos.json")

    # Ejemplo 5: Usar la función de conveniencia
    print("\n5. Usando función de conveniencia...")
    plcs = discover_plcs_on_network(subnet="192.168.1.0/24")
    print(f"   PLCs encontrados: {len(plcs)}")


if __name__ == "__main__":
    main()
