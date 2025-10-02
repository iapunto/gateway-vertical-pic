// Script para probar la navegación y carga de vistas

// Simular el DOM y eventos
const mockViews = {
  "dashboard-view": { classList: { add: () => {}, remove: () => {} } },
  "plcs-view": { classList: { add: () => {}, remove: () => {} } },
  "commands-view": { classList: { add: () => {}, remove: () => {} } },
  "events-view": { classList: { add: () => {}, remove: () => {} } },
  "config-view": { classList: { add: () => {}, remove: () => {} } },
};

const mockElements = {
  "bind-address": { value: "" },
  "bind-port": { value: "" },
  "plc-port": { value: "" },
  "scan-interval": { value: "" },
  "log-level": { value: "" },
  "wms-endpoint": { value: "" },
};

global.document = {
  getElementById: (id) => {
    console.log("Getting element by ID:", id);
    return mockElements[id] || mockViews[id] || null;
  },
  querySelectorAll: (selector) => {
    console.log("Query selector all:", selector);
    return [];
  },
};

// Variables globales
let plcStatusChart = null;
let responseTimeChart = null;
let currentEditingPLC = null;
const API_BASE_URL = "/api/v1";

// Simular la función fetch
global.fetch = async (url) => {
  console.log("Fetching URL:", url);
  if (url === "/api/v1/config") {
    return {
      json: async () => ({
        bind_address: "192.168.1.100",
        bind_port: "9090",
        log_level: "DEBUG",
        plc_port: "3300",
        scan_interval: "60",
        wms_endpoint: "https://test.wms.example.com/api/v1/gateways",
      }),
    };
  }
  return { json: async () => ({}) };
};

// Simular funciones de carga de datos
async function loadDashboardData() {
  console.log("Cargando datos del dashboard");
}

async function loadPLCsData() {
  console.log("Cargando datos de PLCs");
}

async function loadCommandsData() {
  console.log("Cargando datos de comandos");
}

async function loadEventsData() {
  console.log("Cargando datos de eventos");
}

// Función loadConfigData con más depuración
async function loadConfigData() {
  console.log("Iniciando loadConfigData");
  try {
    // Obtener configuraciones desde la API
    console.log("Obteniendo configuraciones desde la API...");
    const response = await fetch(`${API_BASE_URL}/config`);
    const configs = await response.json();
    console.log("Configuraciones obtenidas:", configs);

    // Establecer valores en el formulario si existen en la base de datos
    if (configs) {
      console.log("Configuraciones encontradas, estableciendo valores");
      document.getElementById("bind-address").value =
        configs["bind_address"] || "0.0.0.0";
      document.getElementById("bind-port").value =
        configs["bind_port"] || "8080";
      document.getElementById("plc-port").value = configs["plc_port"] || "3200";
      document.getElementById("scan-interval").value =
        configs["scan_interval"] || "30";
      document.getElementById("log-level").value =
        configs["log_level"] || "INFO";
      document.getElementById("wms-endpoint").value =
        configs["wms_endpoint"] || "https://wms.example.com/api/v1/gateways";

      console.log("Valores establecidos:");
      console.log(
        "bind-address:",
        document.getElementById("bind-address").value
      );
      console.log("bind-port:", document.getElementById("bind-port").value);
      console.log("plc-port:", document.getElementById("plc-port").value);
      console.log(
        "scan-interval:",
        document.getElementById("scan-interval").value
      );
      console.log("log-level:", document.getElementById("log-level").value);
      console.log(
        "wms-endpoint:",
        document.getElementById("wms-endpoint").value
      );
    } else {
      console.log(
        "No se encontraron configuraciones, usando valores por defecto"
      );
    }
  } catch (error) {
    console.error("Error cargando configuración:", error);
  }
}

// Función loadView
function loadView(viewName) {
  console.log("Cargando vista:", viewName);

  // Mostrar la vista solicitada
  const targetView = document.getElementById(viewName + "-view");
  if (targetView) {
    console.log("Vista encontrada, cargando datos específicos");

    // Cargar datos específicos de la vista
    switch (viewName) {
      case "dashboard":
        loadDashboardData();
        break;
      case "plcs":
        loadPLCsData();
        break;
      case "commands":
        loadCommandsData();
        break;
      case "events":
        loadEventsData();
        break;
      case "config":
        console.log("Llamando a loadConfigData para la vista de configuración");
        loadConfigData();
        break;
    }
  } else {
    console.log("Vista no encontrada:", viewName);
  }
}

// Probar la carga de la vista de configuración
console.log("Probando carga de la vista de configuración...");
loadView("config");
