// Simulación completa del comportamiento del navegador

// Simular el entorno del navegador
const browserEnvironment = {
  // Simular el DOM
  document: {
    readyState: 'loading',
    addEventListener: function(event, callback) {
      console.log(`addEventListener: ${event}`);
      if (event === 'DOMContentLoaded' && this.readyState === 'complete') {
        callback();
      }
    },
    getElementById: function(id) {
      console.log(`getElementById: ${id}`);
      // Simular los elementos del formulario de configuración
      const configElements = {
        'bind-address': { value: '' },
        'bind-port': { value: '' },
        'plc-port': { value: '' },
        'scan-interval': { value: '' },
        'log-level': { value: '' },
        'wms-endpoint': { value: '' },
        'config-view': { 
          classList: { 
            add: function(className) { console.log(`addClass: ${className}`); },
            remove: function(className) { console.log(`removeClass: ${className}`); }
          }
        }
      };
      
      return configElements[id] || null;
    },
    querySelectorAll: function(selector) {
      console.log(`querySelectorAll: ${selector}`);
      return [];
    }
  },
  
  // Simular fetch
  fetch: async function(url) {
    console.log(`fetch: ${url}`);
    if (url === '/api/v1/config') {
      return {
        ok: true,
        json: async () => ({
          "bind_address": "192.168.1.100",
          "bind_port": "9090",
          "log_level": "DEBUG",
          "plc_port": "3300",
          "scan_interval": "60",
          "wms_endpoint": "https://test.wms.example.com/api/v1/gateways"
        })
      };
    }
    return { ok: true, json: async () => ({}) };
  },
  
  // Simular console
  console: {
    log: function(...args) {
      console.log('[BROWSER]', ...args);
    },
    error: function(...args) {
      console.error('[BROWSER]', ...args);
    }
  }
};

// Establecer el entorno global
global.document = browserEnvironment.document;
global.fetch = browserEnvironment.fetch;
global.console = browserEnvironment.console;

// Variables globales del script
let plcStatusChart = null;
let responseTimeChart = null;
let currentEditingPLC = null;
const API_BASE_URL = "/api/v1";

// Funciones auxiliares
function showNotification(message, type = "info") {
  console.log(`[NOTIFICATION] ${type}: ${message}`);
}

// Función loadConfigData
async function loadConfigData() {
  console.log('[FUNCTION] Iniciando loadConfigData');
  try {
    // Obtener configuraciones desde la API
    console.log('[FUNCTION] Obteniendo configuraciones desde la API');
    const response = await fetch(`${API_BASE_URL}/config`);
    console.log('[FUNCTION] Respuesta recibida', response.ok);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const configs = await response.json();
    console.log('[FUNCTION] Configuraciones obtenidas', configs);

    // Establecer valores en el formulario si existen en la base de datos
    if (configs) {
      console.log('[FUNCTION] Configuraciones encontradas, estableciendo valores');
      
      const elements = {
        "bind-address": configs["bind_address"] || "0.0.0.0",
        "bind-port": configs["bind_port"] || "8080",
        "plc-port": configs["plc_port"] || "3200",
        "scan-interval": configs["scan_interval"] || "30",
        "log-level": configs["log_level"] || "INFO",
        "wms-endpoint": configs["wms_endpoint"] || "https://wms.example.com/api/v1/gateways"
      };
      
      for (const [id, value] of Object.entries(elements)) {
        const element = document.getElementById(id);
        if (element) {
          element.value = value;
          console.log(`[FUNCTION] Valor establecido para ${id}: ${value}`);
        } else {
          console.log(`[FUNCTION] Elemento no encontrado: ${id}`);
        }
      }
    } else {
      console.log('[FUNCTION] No se encontraron configuraciones');
    }
  } catch (error) {
    console.error("[FUNCTION] Error cargando configuración:", error);
    showNotification("Error cargando configuración", "error");
  }
}

// Función loadView
function loadView(viewName) {
  console.log('[FUNCTION] Cargando vista:', viewName);
  
  // Mostrar la vista solicitada
  const targetView = document.getElementById(viewName + "-view");
  if (targetView) {
    console.log('[FUNCTION] Vista encontrada, removiendo clase hidden');
    targetView.classList.remove("hidden");
    
    // Cargar datos específicos de la vista
    switch (viewName) {
      case "config":
        console.log('[FUNCTION] Llamando a loadConfigData');
        loadConfigData();
        break;
    }
  } else {
    console.log('[FUNCTION] Vista no encontrada:', viewName);
  }
}

// Simular el evento DOMContentLoaded
console.log('[SIMULATION] Simulando DOMContentLoaded');
browserEnvironment.document.readyState = 'complete';

// Simular la navegación a la vista de configuración
console.log('[SIMULATION] Simulando navegación a la vista de configuración');
loadView('config');