# 🏗️ Arquitectura de Multi-Tenant y Gateway Local

## 📋 Resumen Ejecutivo

Este documento describe la arquitectura técnica del sistema WMS Multi-Tenant en la nube y el rol específico del Gateway Local como intermediario de comunicación pura con los PLCs de los racks verticales. El Gateway Local no maneja lógica de negocio, inventario ni productos, únicamente se encarga de la comunicación con los PLCs a través de IP y puerto 3200.

## 🎯 Objetivos de la Arquitectura

- Implementar una solución WMS en arquitectura Multi-Tenant en la nube
- Proporcionar conectividad local con racks verticales a través del Gateway Local
- Mantener separación clara de responsabilidades entre componentes
- Garantizar escalabilidad y alta disponibilidad del sistema

## 🏗️ Arquitectura General

### Componentes Principales

1. **WMS en la Nube (Multi-Tenant)**

   - Sistema central de gestión de almacén
   - Mantiene toda la lógica de negocio (inventario, recepción, picking, envíos)
   - Gestiona usuarios, configuraciones y datos por tenant
   - Coordina actividades con múltiples Gateways Locales

2. **Gateway Local**

   - Componente ligero instalado en las instalaciones del cliente
   - ÚNICA RESPONSABILIDAD: Comunicación con PLCs de racks
   - NO maneja inventario, productos ni lógica de negocio
   - Conecta a través de IP y puerto 3200 con PLCs
   - Comunica con WMS en la nube a través de APIs seguras

3. **PLCs de Racks Verticales**
   - Controladores físicos de los racks verticales
   - Reportan datos de sensores (peso, movimiento, posición, alarmas)
   - Reciben comandos de movimiento del Gateway Local
   - Operan de forma independiente pero coordinada

## 🔧 Detalles del Gateway Local

### Responsabilidades EXCLUSIVAS

- **Comunicación con PLCs**

  - Conexión a través de IP y puerto 3200
  - Envío de comandos de movimiento a racks
  - Recepción de datos de sensores de PLCs:
    - Peso
    - Movimiento
    - Barrera de proximidad
    - Variador de velocidad
    - Posición actual
    - Estado de parada de emergencia
    - Modo remoto/manual
    - Alarmas activas

- **Reenvío de Información**
  - Transmitir comandos del WMS a los PLCs
  - Enviar datos de sensores del PLC al WMS
  - Manejar reconexiones automáticas

### Responsabilidades que NO TIENE

- ❌ NO maneja lógica de inventario
- ❌ NO almacena datos de productos
- ❌ NO toma decisiones de negocio
- ❌ NO procesa pedidos
- ❌ NO gestiona usuarios
- ❌ NO mantiene configuraciones de almacén
- ❌ NO ejecuta mantenimiento
- ❌ NO genera informes

## 🔄 Flujos de Comunicación

### Flujo de Comandos (WMS → Rack)

1. WMS determina necesidad de movimiento físico
2. WMS envía comando específico al Gateway Local
3. Gateway Local traduce y envía comando al PLC correspondiente
4. PLC ejecuta movimiento y reporta estado
5. Gateway Local recoge datos de sensores y envía al WMS
6. WMS actualiza inventario y estado según retroalimentación

### Flujo de Datos (Rack → WMS)

1. PLC detecta cambio en sensores o estado
2. PLC envía datos al Gateway Local
3. Gateway Local recopila y envía datos al WMS
4. WMS procesa datos para:
   - Actualizar estado de equipos
   - Generar alertas
   - Actualizar inventario
   - Optimizar operaciones

## ⚙️ Características Técnicas

### Gateway Local

- **Protocolo de Comunicación**: TCP/IP
- **Puerto de Conexión con PLCs**: 3200
- **Conexión con WMS**: HTTPS/WebSocket seguro
- **Lenguaje de Implementación**: Node.js/Python embebido
- **Requisitos de Hardware**: Mínimos (Raspberry Pi compatible)
- **Almacenamiento**: Mínimo necesario para operación
- **Seguridad**: Certificados TLS, autenticación mutua

### WMS en la Nube

- **Arquitectura**: Microservicios
- **Base de Datos**: PostgreSQL cluster
- **Caché**: Redis
- **Mensajería**: Apache Kafka
- **Balanceo de Carga**: NGINX
- **Contenedores**: Docker/Kubernetes
- **Monitoreo**: Prometheus/Grafana

## 🛡️ Seguridad

### Autenticación

- Gateways Locales se registran con certificados únicos
- Autenticación mutua TLS entre Gateway y WMS
- Tokens JWT para comunicación con APIs

### Autorización

- Cada Gateway solo puede acceder a datos de su tenant
- Control de acceso basado en roles (RBAC)
- Auditoría de todas las operaciones

### Encriptación

- Datos en tránsito: TLS 1.3
- Datos en reposo: AES-256
- Claves de encriptación gestionadas por el tenant

## 📊 Monitoreo y Observabilidad

### Métricas del Gateway Local

- Tiempo de respuesta de PLCs
- Tasa de éxito de comandos
- Uso de recursos (CPU, memoria)
- Estado de conectividad

### Métricas del WMS

- Rendimiento por tenant
- Latencia de operaciones
- Disponibilidad del sistema
- Eficiencia operativa

## 🧪 Pruebas y Despliegue

### Pruebas del Gateway Local

- Simulación de PLCs para pruebas
- Pruebas de desconexión/reconexión
- Pruebas de seguridad y autenticación
- Pruebas de rendimiento bajo carga

### Despliegue

- Contenedores Docker para desarrollo
- Instaladores ligeros para producción
- Actualizaciones OTA (Over-The-Air)
- Rollback automático en caso de fallos

## 📈 Escalabilidad

### Horizontal

- Múltiples Gateways por tenant
- Balanceo de carga entre instancias WMS
- particionamiento de datos por tenant

### Vertical

- Aumento de recursos en servidores WMS
- Optimización de consultas de base de datos
- Caching estratégico de datos frecuentes

## 🆘 Tolerancia a Fallos

### Gateway Local

- Reconexión automática con WMS
- Operación en modo offline limitado
- Almacenamiento temporal de datos
- Notificaciones de estado al WMS

### WMS en la Nube

- Replicación de datos entre regiones
- Failover automático de servicios
- Recuperación de datos ante desastres
- Balanceo de carga entre instancias

## 📋 Consideraciones de Implementación

### Desarrollo del Gateway Local

- Framework ligero (sin dependencias pesadas)
- Mecanismos de logging eficientes
- Gestión de configuración centralizada
- Actualización remota segura

### Integración con PLCs

- Librerías de comunicación estándar
- Manejo de diferentes protocolos PLC
- Conversión de datos entre formatos
- Validación de integridad de datos

## 🚀 Roadmap de Implementación

### Fase 1: Gateway Local Básico

- Comunicación con PLCs
- Conexión segura con WMS
- Envío/recepción de datos básicos

### Fase 2: Funcionalidades Avanzadas

- Manejo de múltiples PLCs
- Caché local para operación offline
- Métricas y monitoreo

### Fase 3: Optimización

- Actualizaciones automáticas
- Mejora de rendimiento
- Integración con más tipos de PLCs

## 📊 KPIs y Métricas

### Rendimiento

- Latencia promedio de comandos (< 5 segundos)
- Tasa de éxito de comunicaciones (> 99.5%)
- Tiempo de reconexión automática (< 30 segundos)

### Disponibilidad

- Uptime del Gateway Local (> 99.9%)
- Uptime del WMS (> 99.95%)
- Tiempo medio de recuperación (< 5 minutos)

### Seguridad

- Número de intentos de acceso no autorizados
- Tiempo de respuesta a vulnerabilidades
- Cumplimiento de estándares de seguridad
