# 📡 Gateway Local PRD - Documento de Requisitos Generales

## 📋 Resumen Ejecutivo

Este documento define los requisitos generales del Gateway Local, que actúa como intermediario de comunicación pura entre el WMS en la nube y los PLCs de los racks verticales. El Gateway Local no maneja lógica de negocio, inventario ni productos, únicamente se encarga de la comunicación con los PLCs a través de IP y puerto 3200.

El Gateway Local se implementará completamente en Python, manteniendo Tkinter para la interfaz gráfica de usuario como se maneja actualmente.

## 🎯 Objetivos del Gateway Local

- Proporcionar conectividad segura y confiable entre WMS Cloud y PLCs locales
- Actuar como intermediario de comunicación pura sin lógica de negocio
- Mantener operación autónoma con capacidad de funcionamiento offline limitado
- Facilitar el descubrimiento automático de PLCs en la red local
- Garantizar alta disponibilidad y resiliencia en comunicaciones

## 👥 Usuarios y Sistemas Interactuando

- **WMS en la Nube**: Sistema central que envía comandos y recibe datos
- **PLCs de Racks**: Controladores físicos de los racks verticales
- **Administrador del Sistema**: Personal de TI que configura y mantiene el Gateway
- **Sistema de Monitoreo**: Herramientas que supervisan el estado del Gateway

## 📋 Requisitos Funcionales Generales

### RF-001: Comunicación con WMS Cloud

- El Gateway debe establecer conexión segura con el WMS en la nube
- Debe autenticarse utilizando certificados TLS mutuos
- Debe mantener sesión activa con heartbeats periódicos
- Debe manejar reconexiones automáticas en caso de pérdida de conexión

### RF-002: Comunicación con PLCs

- El Gateway debe conectarse a PLCs a través de IP y puerto 3200
- Debe soportar múltiples protocolos de comunicación (Modbus TCP, Ethernet/IP, Profinet)
- Debe manejar reconexiones automáticas con PLCs
- Debe enviar comandos de movimiento a racks verticales

### RF-003: Transmisión de Datos

- El Gateway debe reenviar comandos del WMS a los PLCs correspondientes
- Debe transmitir datos de sensores de PLCs al WMS
- Debe mantener orden en la transmisión de mensajes
- Debe manejar buffering de datos en caso de desconexión temporal

### RF-004: Descubrimiento de PLCs

- El Gateway debe descubrir automáticamente PLCs en la red local
- Debe identificar tipo de PLC y protocolo de comunicación
- Debe registrar PLCs descubiertos en el sistema
- Debe mantener inventario actualizado de PLCs conectados

## ⚙️ Requisitos No Funcionales

### RNF-001: Disponibilidad

- El Gateway debe tener una disponibilidad del 99.9%
- Debe reiniciarse automáticamente en caso de fallos críticos
- Debe operar en modo degradado si algunos PLCs no están disponibles

### RNF-002: Rendimiento

- La latencia de comunicación Gateway-PLC debe ser < 5 segundos
- El Gateway debe manejar al menos 50 conexiones simultáneas con PLCs
- La latencia de reenvío de datos debe ser < 1 segundo

### RNF-003: Seguridad

- Toda la comunicación debe estar encriptada con TLS 1.3
- El Gateway debe autenticarse con certificados digitales
- Debe validar la integridad de todos los mensajes
- Debe mantener logs de auditoría de todas las operaciones

### RNF-004: Escalabilidad

- El Gateway debe soportar adición de nuevos PLCs sin reinicio
- Debe manejar diferentes tipos de PLCs simultáneamente
- Debe permitir actualización de configuración en caliente

## 🔄 Arquitectura del Sistema

### Componentes Principales

1. **Core Communication Layer**

   - Maneja conexiones con WMS Cloud
   - Implementa protocolos de seguridad
   - Gestiona autenticación y autorización

2. **PLC Communication Layer**

   - Establece conexiones con PLCs
   - Traduce protocolos de comunicación
   - Maneja reconexiones automáticas

3. **Message Router**

   - Enruta mensajes entre WMS y PLCs
   - Implementa buffering para manejo de desconexiones
   - Gestiona prioridades de mensajes

4. **PLC Discovery Service**

   - Descubre automáticamente PLCs en la red
   - Identifica tipos de PLC y protocolos
   - Mantiene registro de PLCs disponibles

5. **Configuration Manager**

   - Gestiona configuración local
   - Sincroniza con configuración del WMS
   - Almacena parámetros de operación

6. **Health Monitor**
   - Monitorea estado de conexiones
   - Reporta métricas de rendimiento
   - Genera alertas de problemas

## 📊 KPIs y Métricas del Sistema

- Tiempo de respuesta promedio de comandos (< 5 segundos)
- Tasa de éxito de comunicaciones (> 99.5%)
- Tiempo de reconexión automática (< 30 segundos)
- Número de PLCs gestionados simultáneamente
- Uptime del Gateway (> 99.9%)
- Latencia de reenvío de datos (< 1 segundo)

## 🔧 Consideraciones Técnicas

### Tecnología de Implementación

- **Lenguaje Principal**: Python 3.9+
- **Framework Web**: Flask/FastAPI para servicios REST
- **Interfaz Gráfica**: Tkinter (manteniendo implementación actual)
- **Librerías de Comunicación**: pymodbus, pycomm3, y otras específicas de protocolo
- **Gestión de Concurrencia**: asyncio para operaciones asíncronas
- **Sistema de Logging**: logging estándar de Python

### Hardware Requerido

- CPU: Mínimo dual core 1.5GHz
- RAM: Mínimo 512MB
- Almacenamiento: Mínimo 2GB
- Puertos de red: Ethernet 100Mbps
- Sistema operativo: Linux embebido o Windows compatible

### Entorno de Ejecución

- **Versión de Python**: 3.9 o superior
- **Gestor de Paquetes**: pip para dependencias
- **Entorno Virtual**: Recomendado para isolación de dependencias
- **Compatibilidad**: Multiplataforma (Windows, Linux)

### Seguridad

- Autenticación mutua TLS con WMS
- Certificados digitales para identificación
- Encriptación AES-256 para datos sensibles
- Firewall integrado para protección de puertos
