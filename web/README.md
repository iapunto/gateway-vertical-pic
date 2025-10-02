# Interfaz Web del Gateway Local

Esta carpeta contiene la interfaz de usuario web para el Gateway Local que conecta los PLCs del Carousel Vertical PIC con los sistemas WMS/ERP.

## Estructura de Archivos

- `index.html` - Página principal de la interfaz web
- `styles.css` - Hojas de estilo CSS
- `script.js` - Lógica JavaScript para la interfaz
- `components/` - Componentes reutilizables (archivos .vue antiguos, ya no utilizados)

## Características

### Dashboard

- Visualización en tiempo real del estado del sistema
- Contadores de PLCs conectados, comandos ejecutados y eventos registrados
- Gráficos de estado de PLCs y tiempo de respuesta
- Últimos eventos del sistema

### Gestión de PLCs

- Listado completo de PLCs registrados
- Creación, edición y eliminación de PLCs
- Visualización del estado en línea/fuera de línea
- Información detallada de cada PLC

### Comandos

- Envío de comandos a los PLCs (START, STOP, MOVE, STATUS, RESET)
- Historial de comandos ejecutados
- Visualización del estado de éxito/error de cada comando
- Respuestas de los PLCs

### Eventos

- Registro de eventos del sistema
- Clasificación por tipo (CONNECTION, COMMAND, SCAN, ERROR, WARNING)
- Visualización de la fuente y descripción de cada evento
- Nivel de severidad indicado por colores

### Configuración

- Configuración de parámetros del gateway
- Dirección IP y puerto de escucha
- Puerto para comunicación con PLCs
- Intervalo de escaneo de red
- Nivel de logging
- Endpoint del sistema WMS

## Tecnologías Utilizadas

- HTML5
- CSS3 con diseño responsivo
- JavaScript (ES6+) sin frameworks adicionales
- Chart.js para visualización de gráficos
- Font Awesome para iconos
- Google Fonts para tipografía

## Integración con API REST

La interfaz se comunica con el backend a través de una API RESTful:

- `GET /api/v1/plcs` - Obtener lista de PLCs
- `GET /api/v1/plcs/{id}` - Obtener información de un PLC específico
- `POST /api/v1/plcs` - Crear un nuevo PLC
- `PUT /api/v1/plcs/{id}` - Actualizar un PLC existente
- `DELETE /api/v1/plcs/{id}` - Eliminar un PLC
- `GET /api/v1/commands` - Obtener historial de comandos
- `GET /api/v1/events` - Obtener eventos del sistema
- `GET /api/v1/metrics` - Obtener métricas de rendimiento
- `GET /api/v1/stats` - Obtener estadísticas del sistema

## Diseño Responsivo

La interfaz está diseñada para funcionar correctamente en diferentes dispositivos:

- Escritorio: Diseño de cuadrícula completa
- Tabletas: Ajuste de columnas en cuadrícula
- Móviles: Diseño de una sola columna con menú hamburguesa

## Notificaciones

El sistema muestra notificaciones en tiempo real para:

- Confirmación de acciones realizadas
- Errores en operaciones
- Alertas de eventos importantes
- Actualizaciones automáticas de datos

## Seguridad

- Todas las comunicaciones se realizan a través de HTTP (en entorno local)
- Validación de datos en el cliente y servidor
- Manejo de errores apropiado

## Personalización

Para personalizar la interfaz:

1. Modificar `styles.css` para cambiar el diseño visual
2. Editar `script.js` para modificar la lógica de negocio
3. Actualizar `index.html` para cambiar la estructura de la interfaz

## Uso

1. Iniciar el servidor del gateway
2. Abrir un navegador web
3. Navegar a `http://localhost:8080` (o el puerto configurado)
4. Utilizar el menú lateral para navegar entre las diferentes secciones

## Mantenimiento

- Los archivos se han modularizado para facilitar el mantenimiento
- Código comentado para facilitar la comprensión
- Estructura organizada por funcionalidades
- Sin dependencias externas complejas
