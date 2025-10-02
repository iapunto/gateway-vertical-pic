# 🔌 Gateway Local PRD - Módulo de Comunicación con PLCs

## 📋 Resumen Ejecutivo

Este documento detalla los requisitos específicos para el Módulo de Comunicación con PLCs del Gateway Local. Este módulo es responsable de establecer y mantener conexiones con los PLCs de los racks verticales, enviar comandos de movimiento, recibir datos de sensores, y manejar el descubrimiento automático de nuevos PLCs en la red.

El módulo se implementará en Python, utilizando librerías especializadas para comunicación con diferentes tipos de PLCs.

## 🎯 Objetivos del Módulo

- Establecer y mantener conexiones confiables con PLCs de racks verticales
- Enviar comandos de movimiento y control a PLCs específicos
- Recibir y procesar datos de sensores de PLCs en tiempo real
- Descubrir automáticamente nuevos PLCs en la red local
- Manejar múltiples protocolos de comunicación con diferentes tipos de PLCs

## 👥 Usuarios y Sistemas Involucrados

- **PLCs de Racks**: Controladores físicos de los racks verticales
- **Gateway Local**: Sistema que actúa como intermediario de comunicación
- **WMS en la Nube**: Sistema central que coordina operaciones
- **Administrador del Sistema**: Personal de TI que configura y monitorea
- **Sistema de Monitoreo**: Herramientas que supervisan el estado de PLCs

## 📋 Requisitos Funcionales

### RF-001: Conexión con PLCs

- El sistema debe conectarse a PLCs a través de IP y puerto 3200
- Debe manejar múltiples conexiones simultáneas con diferentes PLCs
- Debe implementar timeouts configurables para conexiones
- Debe manejar reconexiones automáticas en caso de pérdida de conexión

### RF-002: Envío de Comandos a PLCs

- El sistema debe enviar comandos de movimiento a racks verticales
- Debe soportar diferentes tipos de comandos (posición, velocidad, parada)
- Debe incluir identificadores de contexto en cada comando
- Debe manejar confirmaciones de ejecución de comandos

### RF-003: Recepción de Datos de Sensores

- El sistema debe recibir datos de sensores de PLCs en tiempo real:
  - Peso
  - Movimiento
  - Barrera de proximidad
  - Variador de velocidad
  - Posición actual
  - Estado de parada de emergencia
  - Modo remoto/manual
  - Alarmas activas
- Debe procesar y estructurar datos para envío al WMS
- Debe manejar diferentes formatos de datos según tipo de PLC

### RF-004: Descubrimiento de PLCs

- El sistema debe descubrir automáticamente PLCs en la red local
- Debe identificar tipo de PLC y protocolo de comunicación
- Debe registrar PLCs descubiertos con información de identificación
- Debe mantener inventario actualizado de PLCs conectados

### RF-005: Soporte de Múltiples Protocolos

- El sistema debe soportar protocolo Modbus TCP
- Debe soportar protocolo Ethernet/IP
- Debe soportar protocolo Profinet
- Debe permitir adición de nuevos protocolos mediante plugins

### RF-006: Manejo de Errores de Comunicación

- El sistema debe detectar errores de comunicación con PLCs
- Debe implementar reintentos con backoff exponencial
- Debe generar alertas para errores persistentes
- Debe mantener operación con otros PLCs si uno falla

## ⚙️ Requisitos No Funcionales

### RNF-001: Rendimiento

- La latencia de comunicación con PLCs debe ser < 5 segundos
- El sistema debe manejar al menos 50 conexiones simultáneas
- El tiempo de respuesta a comandos debe ser < 2 segundos
- El throughput de datos debe ser > 100 mensajes por segundo

### RNF-002: Disponibilidad

- El sistema debe tener una disponibilidad del 99.9%
- Debe recuperarse de fallos de comunicación en < 30 segundos
- Debe operar en modo degradado si algunos PLCs no responden
- Debe notificar al WMS sobre estado de conectividad de PLCs

### RNF-003: Seguridad

- Las comunicaciones con PLCs deben ser validadas
- El sistema debe mantener logs de todas las operaciones con PLCs
- Debe validar integridad de datos recibidos de PLCs
- Debe proteger contra accesos no autorizados a funciones de control

### RNF-004: Escalabilidad

- El sistema debe soportar adición de nuevos PLCs sin reinicio
- Debe permitir configuración de parámetros por tipo de PLC
- Debe manejar diferentes velocidades de comunicación
- Debe permitir actualización de protocolos sin interrupción

## 🔄 Flujos de Trabajo Principales

### Flujo 1: Conexión Inicial con PLC

1. Gateway detecta PLC en la red (por descubrimiento o configuración)
2. Se establece conexión TCP con PLC en puerto 3200
3. Se realiza handshake de protocolo específico
4. Se configuran parámetros de comunicación
5. Se registra PLC en inventario del Gateway
6. Se notifica conexión al WMS

### Flujo 2: Envío de Comando a PLC

1. Gateway recibe comando del WMS para PLC específico
2. Se valida identificador de PLC y existencia de conexión
3. Comando se formatea según protocolo del PLC
4. Se envía comando a través de conexión establecida
5. Se espera confirmación de recepción del PLC
6. Se confirma ejecución del comando al WMS

### Flujo 3: Recepción de Datos de Sensores

1. PLC envía datos de sensores al Gateway
2. Gateway recibe y parsea datos según protocolo
3. Se estructuran datos en formato estándar
4. Se incluyen identificadores de contexto
5. Datos se encolan para envío al WMS
6. Se confirma recepción al PLC

### Flujo 4: Descubrimiento Automático de PLCs

1. Gateway inicia proceso de escaneo de red
2. Se envían paquetes de descubrimiento broadcast
3. PLCs responden con información de identificación
4. Gateway identifica tipo de PLC y protocolo
5. Se intenta conexión con PLCs descubiertos
6. PLCs válidos se registran en inventario

## 📊 KPIs y Métricas

- **Latencia de Comunicación PLC**: < 5 segundos promedio
- **Tasa de Éxito de Conexiones**: > 99.5%
- **Tiempo de Reconexión**: < 30 segundos
- **Número de PLCs Gestionados**: > 50 simultáneamente
- **Throughput de Mensajes**: > 100 mensajes/segundo
- **Tiempo de Respuesta a Comandos**: < 2 segundos

## 🔧 Consideraciones Técnicas

### Tecnología de Implementación

- **Lenguaje**: Python 3.9+
- **Librerías Principales**:
  - `pymodbus` para comunicación Modbus TCP
  - `pycomm3` para comunicación Ethernet/IP
  - `python-snap7` para comunicación Profinet/Siemens
  - `socket` para comunicaciones TCP/IP básicas
- **Concurrencia**: `asyncio` para manejo de múltiples conexiones
- **Gestión de Conexiones**: Pool de conexiones reutilizables

### Protocolos Soportados

- **Modbus TCP**: Para PLCs compatibles con protocolo Modbus
- **Ethernet/IP**: Para PLCs Allen-Bradley y compatibles
- **Profinet**: Para PLCs Siemens y compatibles
- **Protocolos Personalizados**: Para PLCs con protocolos específicos

### Manejo de Conexiones

- **Pool de Conexiones**: Reutilización de conexiones establecidas
- **Timeouts Configurables**: Parámetros ajustables por tipo de PLC
- **Reconexión Automática**: Proceso automático con backoff exponencial
- **Monitoreo de Estado**: Verificación continua de conectividad

### Formatos de Datos

- **Estructura Unificada**: Formato estándar para todos los datos de sensores
- **Mapeo de Protocolos**: Conversión entre formatos específicos y estándar
- **Validación de Datos**: Verificación de integridad y rango de valores
- **Compresión**: Opcional para optimización de ancho de banda

### Descubrimiento de PLCs

- **Métodos de Escaneo**: Broadcast, multicast, lista de IPs configuradas
- **Identificación de Protocolo**: Detección automática o configuración manual
- **Registro Automático**: Incorporación al inventario sin intervención manual
- **Actualización de Inventario**: Mantenimiento en tiempo real del estado
