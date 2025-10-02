# Gateway Local

## Descripción

Implementación modular del Gateway Local para comunicación con PLCs de racks verticales, evolución del Carousel API existente.

## Arquitectura Modular

La nueva arquitectura sigue principios de diseño limpio y separación de responsabilidades:

```text
gateway/
├── src/                    # Código fuente del Gateway
│   ├── core/              # Core del sistema y orquestación
│   ├── plc/               # Implementaciones específicas de PLCs
│   ├── interfaces/        # Interfaces comunes
│   ├── config/            # Gestión de configuración
│   ├── wms/               # Comunicación con WMS cloud
│   ├── utils/             # Utilidades y herramientas
│   ├── adapters/          # Adaptadores para compatibilidad
│   └── main.py            # Punto de entrada
├── tests/                 # Pruebas unitarias e integración
├── docs/                  # Documentación técnica
├── requirements.txt       # Dependencias de Python
├── gateway_config.json    # Configuración principal
└── README.md              # Este archivo
```

## Componentes Principales

### Core (`src/core/`)

- **gateway_core.py**: Orquestador principal del sistema
- Gestiona el ciclo de vida del gateway
- Coordina la comunicación entre componentes

### PLC (`src/plc/`)

- **delta_plc.py**: Implementación específica para PLC Delta AS Series
- **plc_factory.py**: Fábrica para crear instancias de PLCs
- Diseñado para fácil extensión a otras marcas de PLC

### Interfaces (`src/interfaces/`)

- **plc_interface.py**: Interface común para todos los PLCs
- Permite polimorfismo y fácil sustitución de implementaciones

### Configuración (`src/config/`)

- **config_manager.py**: Gestor centralizado de configuración
- Soporta configuración por archivos JSON

### WMS (`src/wms/`)

- **wms_client.py**: Cliente para comunicación con WMS cloud
- Implementa registro, heartbeat y sincronización

### Utilidades (`src/utils/`)

- **logger.py**: Sistema de logging centralizado

### Adaptadores (`src/adapters/`)

- **api_adapter.py**: Mantiene compatibilidad con API existente

## Extensibilidad

Para añadir soporte para un nuevo tipo de PLC:

1. Crear una nueva implementación en `src/plc/`
2. Implementar la interface `PLCInterface`
3. Registrar el nuevo tipo en `PLCFactory`
4. Añadir configuración en `gateway_config.json`

## Desarrollo

Siga el flujo de trabajo GIT definido en [docs/GIT_WORKFLOW_GATEWAY.md](file:///C:/laragon/www/carousel_api/docs/GIT_WORKFLOW_GATEWAY.md)

## Compatibilidad

Este componente mantiene compatibilidad con la versión actual del Carousel API v2.6.1
