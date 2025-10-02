# 🏗️ Arquitectura Modular del Gateway Local

## 🎯 Objetivo

Documentar la nueva arquitectura modular del Gateway Local, diseñada para ser extensible, mantenible y compatible con múltiples marcas de PLC.

## 📐 Principios de Diseño

### 1. Separación de Responsabilidades

Cada módulo tiene una única responsabilidad bien definida:

- **Core**: Orquestación del sistema
- **PLC**: Implementaciones específicas por marca
- **Interfaces**: Contratos comunes
- **Config**: Gestión de configuración
- **WMS**: Comunicación con el sistema cloud
- **Utils**: Utilidades comunes
- **Adapters**: Compatibilidad con sistemas existentes

### 2. Inversión de Dependencias

Los módulos dependen de abstracciones, no de implementaciones concretas.

### 3. Extensibilidad

Fácil adición de nuevos tipos de PLC sin modificar código existente.

### 4. Compatibilidad

Mantener interfaces compatibles con el sistema existente.

## 🏗️ Estructura de Directorios

```
gateway/
├── src/                    # Código fuente
│   ├── core/              # Núcleo del sistema
│   ├── plc/               # Implementaciones PLC
│   ├── interfaces/        # Interfaces comunes
│   ├── config/            # Gestión de configuración
│   ├── wms/               # Comunicación WMS
│   ├── utils/             # Utilidades
│   ├── adapters/          # Adaptadores de compatibilidad
│   └── main.py            # Punto de entrada
├── tests/                 # Pruebas
├── docs/                  # Documentación
├── requirements.txt       # Dependencias
├── gateway_config.json    # Configuración
└── README.md              # Documentación principal
```

## 🧩 Componentes Detallados

### Core (`src/core/`)

**gateway_core.py**: Orquestador principal

- Gestiona el ciclo de vida del gateway
- Coordina la inicialización de PLCs
- Maneja hilos de trabajo (heartbeat, monitoreo)
- Proporciona API central para operaciones

### Interfaces (`src/interfaces/`)

**plc_interface.py**: Contrato común para todos los PLCs

- Define métodos obligatorios: `connect`, `disconnect`, `send_command`, etc.
- Permite polimorfismo y sustitución fácil de implementaciones

### PLC (`src/plc/`)

Implementaciones específicas por marca:

**delta_plc.py**: PLC Delta AS Series

- Implementación completa de la interface
- Manejo de conexión TCP/IP
- Envío/recepción de comandos
- Reintentos con backoff exponencial

**plc_factory.py**: Fábrica de PLCs

- Crea instancias según tipo especificado
- Registro dinámico de nuevos tipos
- Mapeo case-insensitive de tipos

### Configuración (`src/config/`)

**config_manager.py**: Gestor de configuración

- Carga/guarda configuración JSON
- Valores por defecto
- Acceso jerárquico con notación de puntos

### WMS (`src/wms/`)

**wms_client.py**: Cliente WMS

- Registro de gateway
- Envío de heartbeat
- Sincronización de datos
- Manejo de comandos

### Utilidades (`src/utils/`)

**logger.py**: Sistema de logging

- Configuración flexible
- Rotación de archivos
- Formato estandarizado

### Adaptadores (`src/adapters/`)

**api_adapter.py**: Compatibilidad con API existente

- Mantiene interfaces compatibles
- Traduce llamadas al nuevo sistema
- Facilita la transición gradual

## 🔌 Extensibilidad para Nuevas Marcas de PLC

### Pasos para Añadir un Nuevo PLC:

1. **Crear Implementación**:

   ```python
   # src/plc/siemens_plc.py
   from gateway.src.interfaces.plc_interface import PLCInterface

   class SiemensPLC(PLCInterface):
       def __init__(self, ip: str, port: int):
           # Implementación específica
           pass

       def connect(self) -> bool:
           # Implementación específica
           pass

       # ... implementar todos los métodos abstractos
   ```

2. **Registrar en Fábrica**:

   ```python
   # En el punto de inicialización
   from gateway.src.plc.plc_factory import PLCFactory
   from gateway.src.plc.siemens_plc import SiemensPLC

   PLCFactory.register_plc_type("siemens", SiemensPLC)
   ```

3. **Añadir Configuración**:
   ```json
   {
     "plcs": [
       {
         "id": "PLC-003",
         "type": "siemens",
         "ip": "192.168.1.102",
         "port": 3200
       }
     ]
   }
   ```

## 🔄 Patrones de Diseño Utilizados

### 1. Factory Pattern

**PLCFactory** crea instancias de PLCs según el tipo especificado.

### 2. Adapter Pattern

**APIAdapter** mantiene compatibilidad con la API existente.

### 3. Interface Segregation

Interfaces específicas para cada responsabilidad.

### 4. Dependency Injection

Inyección de dependencias para facilitar testing.

### 5. Singleton Pattern (implícito)

Configuración y logging como singletons implícitos.

## 🧪 Estrategia de Testing

### Pruebas Unitarias

- Cada módulo se prueba independientemente
- Mocks para dependencias externas
- Cobertura de casos normales y excepcionales

### Pruebas de Integración

- Comunicación entre módulos
- Flujos completos de operación
- Compatibilidad con API existente

### Pruebas de Extensibilidad

- Registro de nuevos tipos de PLC
- Funcionamiento con diferentes implementaciones

## 🛡️ Consideraciones de Seguridad

### Configuración Segura

- Tokens y credenciales en variables de entorno
- Validación de entradas
- Logging seguro (sin datos sensibles)

### Comunicación Segura

- TLS para comunicación WMS
- Validación de certificados
- Encriptación de datos sensibles

## 📈 Ventajas de la Arquitectura Modular

### 1. Mantenibilidad

- Cambios localizados en módulos específicos
- Menor riesgo de efectos secundarios
- Código más legible y organizado

### 2. Extensibilidad

- Fácil adición de nuevas marcas de PLC
- Nuevas funcionalidades sin afectar existentes
- Reutilización de componentes

### 3. Testeabilidad

- Módulos independientes fácilmente testeables
- Mocks para simular dependencias
- Cobertura más precisa

### 4. Escalabilidad

- Componentes reemplazables
- Balanceo de carga posible
- Distribución geográfica

### 5. Compatibilidad

- Adaptadores para sistemas existentes
- Migración gradual
- Sin interrupciones de servicio

## 🚀 Próximos Pasos

1. **Implementar PLCs adicionales** (Siemens, Allen Bradley, etc.)
2. **Desarrollar API REST** para el nuevo gateway
3. **Crear dashboard de monitoreo**
4. **Implementar sistema de actualizaciones automáticas**
5. **Desarrollar pruebas de carga y estrés**
6. **Documentar API pública**

## 📝 Conclusión

La nueva arquitectura modular del Gateway Local proporciona una base sólida para la evolución del sistema, manteniendo la compatibilidad con clientes existentes mientras permite la extensión a nuevas tecnologías y marcas de PLC. La separación clara de responsabilidades y el uso de patrones de diseño probados garantizan un sistema mantenible, escalable y robusto.
