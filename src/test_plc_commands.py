#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para enviar comandos al PLC a través del Gateway
"""

import sys
import os
import json
import time
from typing import Optional

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.gateway_core import GatewayCore
from adapters.api_adapter import APIAdapter


def test_plc_commands():
    """Test para enviar comandos al PLC"""
    print("🧪 Iniciando test de comandos PLC...")
    
    try:
        # Crear e iniciar el gateway
        print(" Iniciando Gateway...")
        gateway = GatewayCore()
        
        if not gateway.start():
            print("❌ Error iniciando Gateway")
            return False
            
        print("✅ Gateway iniciado correctamente")
        
        # Crear adaptador API
        adapter = APIAdapter(gateway)
        
        # Obtener lista de máquinas
        print(" Obteniendo lista de máquinas...")
        machines = adapter.get_machines()
        print(f"  Máquinas disponibles: {machines}")
        
        if not machines.get("success", False) or not machines.get("data", []):
            print("❌ No hay máquinas disponibles")
            gateway.stop()
            return False
            
        # Obtener el ID del primer PLC
        plc_id = machines["data"][0]["id"]
        print(f"  Usando PLC: {plc_id}")
        
        # Obtener estado inicial
        print(" Obteniendo estado inicial...")
        status = adapter.get_status(plc_id)
        print(f"  Estado inicial: {status}")
        
        if not status.get("success", False):
            print("❌ Error obteniendo estado inicial")
            gateway.stop()
            return False
            
        # Enviar comando para mover a posición 1
        print(" Enviando comando para mover a posición 1...")
        result = adapter.move_to_position(1, plc_id)
        print(f"  Resultado: {result}")
        
        if not result.get("success", False):
            print("❌ Error moviendo a posición 1")
            gateway.stop()
            return False
            
        print("✅ Comando enviado correctamente")
        
        # Esperar un momento
        time.sleep(2)
        
        # Obtener estado actual
        print(" Obteniendo estado actual...")
        status = adapter.get_status(plc_id)
        print(f"  Estado actual: {status}")
        
        # Enviar comando para mover a posición 5
        print(" Enviando comando para mover a posición 5...")
        result = adapter.move_to_position(5, plc_id)
        print(f"  Resultado: {result}")
        
        if not result.get("success", False):
            print("❌ Error moviendo a posición 5")
            gateway.stop()
            return False
            
        print("✅ Comando enviado correctamente")
        
        # Esperar un momento
        time.sleep(2)
        
        # Obtener estado final
        print(" Obteniendo estado final...")
        status = adapter.get_status(plc_id)
        print(f"  Estado final: {status}")
        
        # Detener el gateway
        print(" Deteniendo Gateway...")
        gateway.stop()
        print("✅ Gateway detenido correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        return False


def send_custom_command(plc_id: Optional[str] = None, command: int = 0, argument: Optional[int] = None):
    """Envía un comando personalizado al PLC"""
    print(f"🧪 Enviando comando personalizado: comando={command}, argumento={argument}")
    
    try:
        # Crear e iniciar el gateway
        print(" Iniciando Gateway...")
        gateway = GatewayCore()
        
        if not gateway.start():
            print("❌ Error iniciando Gateway")
            return False
            
        print("✅ Gateway iniciado correctamente")
        
        # Crear adaptador API
        adapter = APIAdapter(gateway)
        
        # Si no se especifica PLC, usar el primero disponible
        if plc_id is None:
            machines = adapter.get_machines()
            if machines.get("success", False) and machines.get("data", []):
                plc_id = machines["data"][0]["id"]
                print(f"  Usando PLC: {plc_id}")
            else:
                print("❌ No hay máquinas disponibles")
                gateway.stop()
                return False
        
        # Enviar comando
        print(f" Enviando comando {command} con argumento {argument} al PLC {plc_id}...")
        result = adapter.send_command(command, argument, plc_id)
        print(f"  Resultado: {result}")
        
        if result.get("success", False):
            print("✅ Comando enviado correctamente")
        else:
            print("❌ Error enviando comando")
            
        # Detener el gateway
        print(" Deteniendo Gateway...")
        gateway.stop()
        print("✅ Gateway detenido correctamente")
        
        return result.get("success", False)
        
    except Exception as e:
        print(f"❌ Error enviando comando: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal"""
    print("🚀 Script de prueba de comandos PLC")
    print("=" * 40)
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == "move":
            if len(sys.argv) >= 3:
                position = int(sys.argv[2])
                plc_id = sys.argv[3] if len(sys.argv) > 3 else None
                send_custom_command(plc_id, 1, position)
            else:
                print("Uso: python test_plc_commands.py move <posición> [plc_id]")
        elif sys.argv[1] == "status":
            plc_id = sys.argv[2] if len(sys.argv) > 2 else None
            send_custom_command(plc_id, 0)
        elif sys.argv[1] == "custom":
            if len(sys.argv) >= 4:
                command = int(sys.argv[2])
                argument = int(sys.argv[3]) if sys.argv[3].lower() != "none" else None
                plc_id = sys.argv[4] if len(sys.argv) > 4 else None
                send_custom_command(plc_id, command, argument)
            else:
                print("Uso: python test_plc_commands.py custom <comando> <argumento|none> [plc_id]")
        else:
            print("Comandos disponibles:")
            print("  python test_plc_commands.py          # Test completo")
            print("  python test_plc_commands.py move <posición> [plc_id]")
            print("  python test_plc_commands.py status [plc_id]")
            print("  python test_plc_commands.py custom <comando> <argumento|none> [plc_id]")
            return 1
    else:
        # Ejecutar test completo
        if test_plc_commands():
            print("\n🎉 Todos los tests PASARON exitosamente!")
        else:
            print("\n❌ Algunos tests FALLARON")
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())