// Script para probar la carga inmediata de datos

// Simular el entorno del navegador
const mockElements = {
  "bind-address": { value: "", placeholder: "" },
  "bind-port": { value: "", placeholder: "" },
  "plc-port": { value: "", placeholder: "" },
  "scan-interval": { value: "", placeholder: "" },
  "log-level": { value: "INFO", tagName: "SELECT" },
  "wms-endpoint": { value: "", placeholder: "" },
};

const mockDocument = {
  readyState: "complete",
  addEventListener: function (event, callback) {
    console.log(`addEventListener: ${event}`);
    if (event === "DOMContentLoaded") {
      console.log("Simulando DOMContentLoaded");
      callback();
    }
  },
  getElementById: function (id) {
    console.log(`getElementById: ${id}`);
    return mockElements[id] || null;
  },
};

// Simular fetch
async function mockFetch(url) {
  console.log(`fetch: ${url}`);
  if (url === "/api/v1/config") {
    return {
      ok: true,
      status: 200,
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
  return { ok: true, status: 200, json: async () => ({}) };
}

// Variables globales
const API_BASE_URL = "/api/v1";

// Función auxiliar
function showNotification(message, type = "info") {
  console.log(`[NOTIFICATION] ${type}: ${message}`);
}

// Función loadConfigData mejorada
async function loadConfigData() {
  console.log("Iniciando loadConfigData");

  // Establecer placeholders de carga
  const loadingElements = [
    "bind-address",
    "bind-port",
    "plc-port",
    "scan-interval",
    "wms-endpoint",
  ];
  loadingElements.forEach((id) => {
    const element = mockDocument.getElementById(id);
    if (element && !element.value) {
      element.placeholder = "Cargando...";
      console.log(`Placeholder establecido para ${id}:`, element.placeholder);
    }
  });

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

    // Valores por defecto
    const defaultValues = {
      bind_address: "0.0.0.0",
      bind_port: "8080",
      plc_port: "3200",
      scan_interval: "30",
      log_level: "INFO",
      wms_endpoint: "https://wms.example.com/api/v1/gateways",
    };

    // Combinar configuraciones obtenidas con valores por defecto
    const finalConfigs = { ...defaultValues, ...configs };

    // Establecer valores en el formulario inmediatamente
    if (finalConfigs) {
      console.log("Configuraciones encontradas, estableciendo valores");

      // Establecer valores inmediatamente
      const elements = {
        "bind-address": finalConfigs["bind_address"],
        "bind-port": finalConfigs["bind_port"],
        "plc-port": finalConfigs["plc_port"],
        "scan-interval": finalConfigs["scan_interval"],
        "log-level": finalConfigs["log_level"],
        "wms-endpoint": finalConfigs["wms_endpoint"],
      };

      // Actualizar todos los elementos
      Object.keys(elements).forEach((id) => {
        const element = mockDocument.getElementById(id);
        if (element) {
          // Para select, seleccionar la opción correcta
          if (element.tagName === "SELECT") {
            element.value = elements[id];
          } else {
            element.value = elements[id];
          }
          // Remover placeholder de carga
          element.placeholder = "";
          console.log(`Valor establecido para ${id}:`, element.value);
        }
      });
    }
  } catch (error) {
    console.error("Error cargando configuración:", error);
    showNotification("Error cargando configuración", "error");

    // Establecer valores por defecto en caso de error
    const defaultElements = {
      "bind-address": "0.0.0.0",
      "bind-port": "8080",
      "plc-port": "3200",
      "scan-interval": "30",
      "log-level": "INFO",
      "wms-endpoint": "https://wms.example.com/api/v1/gateways",
    };

    Object.keys(defaultElements).forEach((id) => {
      const element = mockDocument.getElementById(id);
      if (element) {
        if (element.tagName === "SELECT") {
          element.value = defaultElements[id];
        } else {
          element.value = defaultElements[id];
        }
        element.placeholder = "";
        console.log(`Valor por defecto establecido para ${id}:`, element.value);
      }
    });
  }
}

// Simular el script inline del HTML
mockDocument.addEventListener("DOMContentLoaded", function () {
  // Establecer placeholders temporales
  mockDocument.getElementById("bind-address").placeholder = "Cargando...";
  mockDocument.getElementById("bind-port").placeholder = "Cargando...";
  mockDocument.getElementById("plc-port").placeholder = "Cargando...";
  mockDocument.getElementById("scan-interval").placeholder = "Cargando...";
  mockDocument.getElementById("wms-endpoint").placeholder = "Cargando...";
  console.log("Placeholders de carga establecidos");
});

// Mostrar estado inicial
console.log("Estado inicial de los elementos:");
Object.keys(mockElements).forEach((id) => {
  console.log(
    `${id}: value="${mockElements[id].value}", placeholder="${mockElements[id].placeholder}"`
  );
});

// Ejecutar la carga de configuración
console.log("\nIniciando carga de configuración...");
loadConfigData();

// Mostrar estado final
console.log("\nEstado final de los elementos:");
Object.keys(mockElements).forEach((id) => {
  console.log(
    `${id}: value="${mockElements[id].value}", placeholder="${mockElements[id].placeholder}"`
  );
});
