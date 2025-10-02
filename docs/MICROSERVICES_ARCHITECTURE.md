# Arquitectura de Microservicios

## Visión General

El sistema ha sido evolucionado hacia una arquitectura de microservicios siguiendo principios de Domain-Driven Design (DDD) para mejorar la modularidad, escalabilidad y mantenibilidad del sistema.

## Microservicios Disponibles

### 1. Adaptador PLC (`plc-adapter`)

- **Responsabilidad**: Comunicación con PLCs Delta AS Series
- **Puerto**: 8082
- **Endpoints**:
  - `GET /health` - Verificación de salud
  - `GET /metrics` - Métricas del sistema
  - `GET /plcs` - Listar PLCs configurados
  - `GET /plcs/{plc_id}/status` - Estado de un PLC específico
  - `POST /plcs/{plc_id}/command` - Enviar comando a un PLC

### 2. Servicio de Monitoreo (`monitoring`)

- **Responsabilidad**: Recopilación y exposición de métricas del sistema
- **Puerto**: 8083
- **Endpoints**:
  - `GET /health` - Verificación de salud
  - `GET /metrics` - Métricas del sistema
  - `GET /metrics/prometheus` - Métricas en formato Prometheus

### 3. Servicio de Salud (`health`)

- **Responsabilidad**: Verificación del estado de todos los microservicios
- **Puerto**: 8084
- **Endpoints**:
  - `GET /health` - Verificación de salud del servicio
  - `GET /health/system` - Verificación de salud del sistema completo
  - `GET /health/services` - Estado de todos los microservicios

### 4. Gestor de Eventos (`event_manager`)

- **Responsabilidad**: Gestión centralizada de eventos del sistema
- **Puerto**: 8085
- **Endpoints**:
  - `GET /health` - Verificación de salud
  - `GET /events` - Listar eventos recientes
  - `POST /events` - Emitir un evento

## Comunicación entre Microservicios

Los microservicios se comunican a través de:

1. **API REST**: Cada microservicio expone una API REST para interacción externa
2. **Cola de Mensajes**: Redis se utiliza como broker de mensajes para comunicación asíncrona
3. **Eventos**: Sistema de eventos interno para notificaciones entre componentes

## Configuración

La configuración de microservicios se encuentra en `src/config/microservices_config.json` y puede ser personalizada según las necesidades del entorno.

## Despliegue

### Opción 1: Ejecución Individual

Cada microservicio puede ejecutarse individualmente usando sus scripts de inicio:

```bash
# En Linux/Mac
./microservices/plc-adapter/start_adapter.sh

# En Windows
microservices\plc-adapter\start_adapter.bat
```

### Opción 2: Docker Compose

```bash
docker-compose up -d
```

### Opción 3: Todos los Servicios

```bash
# En Linux/Mac
./start_all_services.sh

# En Windows
start_all_services.bat
```

## Beneficios de la Arquitectura

1. **Escalabilidad**: Cada microservicio puede escalarse independientemente
2. **Mantenibilidad**: Cambios en un microservicio no afectan a otros
3. **Resiliencia**: Fallas en un microservicio no detienen todo el sistema
4. **Despliegue Flexible**: Cada microservicio puede desplegarse por separado
5. **Tecnología Heterogénea**: Cada microservicio puede utilizar tecnologías específicas según sus necesidades
