# Interfaz Web Modular con Vue.js para Gateway Local

Esta carpeta contiene la interfaz web moderna y modular para el Gateway Local, construida con Vue.js para una experiencia de usuario más dinámica y mantenible.

## Estructura de Archivos

```
web/
├── components/                 # Componentes Vue reutilizables
│   ├── dashboard.vue          # Componente del dashboard principal
│   ├── plc-manager.vue        # Gestión completa de PLCs (CRUD)
│   ├── command-manager.vue    # Gestión de comandos
│   ├── event-manager.vue      # Visualización de eventos
│   └── config-manager.vue     # Gestión de configuración
├── app.js                     # Punto de entrada de la aplicación Vue
├── index.html                 # Página principal (versión original)
├── index-vue.html             # Página principal (versión con Vue.js)
├── styles.css                 # Hojas de estilo CSS
├── script.js                  # Funcionalidad JavaScript (versión original)
└── README.md                  # Documentación de la interfaz web
```

## Características de la Nueva Interfaz

### 1. Modularización Completa

- Cada sección de la interfaz es un componente Vue independiente
- Facilita el mantenimiento y la expansión futura
- Permite la reutilización de componentes

### 2. Funcionalidades CRUD Completas

- **PLC Manager**: Crear, leer, actualizar y eliminar PLCs
- **Command Manager**: Enviar y visualizar comandos
- **Event Manager**: Visualizar eventos del sistema
- **Config Manager**: Configurar parámetros del gateway

### 3. Notificaciones en Tiempo Real

- Sistema de notificaciones para feedback inmediato
- Diferentes tipos de notificaciones (éxito, error, advertencia, info)
- Auto-eliminación de notificaciones

### 4. Navegación Intuitiva

- Menú lateral con todas las secciones
- Vista principal que cambia dinámicamente
- Indicadores visuales del estado actual

## Componentes Detallados

### Dashboard (`components/dashboard.vue`)

- Estadísticas en tiempo real del sistema
- Estado de salud del gateway
- Últimos eventos registrados
- Gráficos interactivos con Chart.js
- Indicadores de rendimiento

### PLC Manager (`components/plc-manager.vue`)

- Tabla con todos los PLCs registrados
- Modal para crear nuevos PLCs
- Modal para editar PLCs existentes
- Confirmación de eliminación
- Validación de formularios
- Simulación de operaciones CRUD

### Command Manager (`components/command-manager.vue`)

- Envío de comandos a PLCs específicos
- Historial de comandos enviados
- Soporte para diferentes tipos de comandos
- Argumentos dinámicos según el tipo de comando
- Feedback visual del estado de ejecución

### Event Manager (`components/event-manager.vue`)

- Visualización de eventos del sistema
- Filtrado por nivel de severidad
- Detalles completos de cada evento
- Timestamps precisos

### Config Manager (`components/config-manager.vue`)

- Configuración completa del gateway
- Secciones organizadas por categorías
- Validación de parámetros
- Persistencia de configuración

## Tecnologías Utilizadas

- **Vue.js 3**: Framework progresivo para interfaces de usuario
- **Chart.js**: Biblioteca de gráficos interactivos
- **Font Awesome**: Iconos vectoriales
- **Google Fonts**: Tipografía Roboto
- **CSS3**: Estilos modernos y responsivos

## Cómo Usar

1. **Para usar la versión original**:

   ```
   Acceder a http://localhost:8080/
   ```

2. **Para usar la versión con Vue.js**:

   ```
   Acceder a http://localhost:8080/index-vue.html
   ```

3. **Desarrollo**:
   - Modificar componentes en la carpeta `components/`
   - Actualizar estilos en `styles.css`
   - Añadir nueva funcionalidad en `app.js`

## Ventajas de la Arquitectura Modular

1. **Mantenibilidad**: Cada componente es independiente y fácil de modificar
2. **Escalabilidad**: Fácil de extender con nuevos componentes
3. **Reusabilidad**: Componentes pueden ser reutilizados en otras partes
4. **Colaboración**: Múltiples desarrolladores pueden trabajar en diferentes componentes
5. **Testing**: Cada componente puede ser probado independientemente

## Próximos Pasos

1. Conectar los componentes con la API REST real del gateway
2. Implementar autenticación y autorización
3. Añadir más componentes para funcionalidades avanzadas
4. Optimizar el rendimiento de la aplicación
5. Implementar pruebas unitarias para los componentes

## Notas de Implementación

- La versión actual utiliza datos simulados para demostración
- En producción, los componentes se conectarían a la API REST real
- Los estilos están optimizados para dispositivos móviles y escritorio
- La aplicación es completamente responsiva
