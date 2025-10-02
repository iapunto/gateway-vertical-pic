// Script para simular la carga de configuración en el frontend

// Simular el entorno del navegador
const mockDocument = {
  readyState: 'complete',
  addEventListener: function(event, callback) {
    console.log(`addEventListener: ${event}`);
    if (event === 'DOMContentLoaded') {
      setTimeout(callback, 100); // Simular que el DOM ya está cargado
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
};

// Simular fetch
async function mockFetch(url) {
  console.log(`fetch: ${url}`);
  if (url === '/api/v1/config') {
    return {
      ok: true,
      status: 200,
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
  return { ok: true, status: 200, json: async () => ({}) };
}

// Variables globales
let plcStatusChart = null;
let responseTimeChart = null;
let currentEditingPLC = null;
const API_BASE_URL = "/api/v1";

// Funciones auxiliares
function showNotification(message, type = "info") {
  console.log(`[NOTIFICATION] ${type}: ${message}`);
}

// Función loadConfigData con depuración (versión del frontend modificado)
async function loadConfigData() {
  console.log("Iniciando loadConfigData");
  try {
    // Obtener configuraciones desde la API
    console.log("Obteniendo configuraciones desde la API");
    const response = await mockFetch(`${API_BASE_URL}/config`);
    console.log("Respuesta de la API recibida", response.status);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const configs = await response.json();
    console.log("Configuraciones obtenidas", configs);

    // Establecer valores en el formulario si existen en la base de datos
    if (configs) {
      console.log("Configuraciones encontradas, estableciendo valores");
      
      // Verificar que los elementos existan antes de establecer valores
      const bindAddressElement = mockDocument.getElementById("bind-address");
      const bindPortElement = mockDocument.getElementById("bind-port");
      const plcPortElement = mockDocument.getElementById("plc-port");
      const scanIntervalElement = mockDocument.getElementById("scan-interval");
      const logLevelElement = mockDocument.getElementById("log-level");
      const wmsEndpointElement = mockDocument.getElementById("wms-endpoint");
      
      console.log("Elementos del DOM:", {
        bindAddress: !!bindAddressElement,
        bindPort: !!bindPortElement,
        plcPort: !!plcPortElement,
        scanInterval: !!scanIntervalElement,
        logLevel: !!logLevelElement,
        wmsEndpoint: !!wmsEndpointElement
      });
      
      if (bindAddressElement) {
        bindAddressElement.value = configs["bind_address"] || "0.0.0.0";
        console.log("Valor establecido para bind-address:", bindAddressElement.value);
      }
      
      if (bindPortElement) {
        bindPortElement.value = configs["bind_port"] || "8080";
        console.log("Valor establecido para bind-port:", bindPortElement.value);
      }
      
      if (plcPortElement) {
        plcPortElement.value = configs["plc_port"] || "3200";
        console.log("Valor establecido para plc-port:", plcPortElement.value);
      }
      
      if (scanIntervalElement) {
        scanIntervalElement.value = configs["scan_interval"] || "30";
        console.log("Valor establecido para scan-interval:", scanIntervalElement.value);
      }
      
      if (logLevelElement) {
        logLevelElement.value = configs["log_level"] || "INFO";
        console.log("Valor establecido para log-level:", logLevelElement.value);
      }
      
      if (wmsEndpointElement) {
        wmsEndpointElement.value = configs["wms_endpoint"] || "https://wms.example.com/api/v1/gateways";
        console.log("Valor establecido para wms-endpoint:", wmsEndpointElement.value);
      }
    } else {
      console.log("No se encontraron configuraciones");
    }
  } catch (error) {
    console.error("Error cargando configuración:", error);
    showNotification("Error cargando configuración", "error");
  }
}

// Función loadView con depuración
function loadView(viewName) {
  console.log("Cargando vista:", viewName);
  
  // Mostrar la vista solicitada
  const targetView = mockDocument.getElementById(viewName + "-view");
  if (targetView) {
    console.log("Vista encontrada, removiendo clase hidden");
    targetView.classList.remove("hidden");
    
    // Cargar datos específicos de la vista
    switch (viewName) {
      case "config":
        console.log("Llamando a loadConfigData");
        loadConfigData();
        break;
    }
  } else {
    console.log("Vista no encontrada:", viewName);
  }
}

// Simular el evento DOMContentLoaded
console.log("Simulando DOMContentLoaded");
mockDocument.addEventListener('DOMContentLoaded', function() {
  console.log("DOMContentLoaded disparado");
  
  // Simular la navegación a la vista de configuración
  console.log("Simulando navegación a la vista de configuración");
  loadView('config');
});