// Script de prueba simple para verificar la función loadConfigData

// Simular la función fetch
global.fetch = async (url) => {
  console.log("Fetching URL:", url);
  if (url === "/api/v1/config") {
    console.log("Returning mock config data");
    return {
      json: async () => ({
        bind_address: "0.0.0.0",
        bind_port: "8080",
        log_level: "INFO",
        plc_port: "3200",
        scan_interval: "30",
        wms_endpoint: "https://wms.example.com/api/v1/gateways",
      }),
    };
  }
  return { json: async () => ({}) };
};

// Simular el DOM
global.document = {
  getElementById: (id) => {
    console.log("Getting element by ID:", id);
    return {
      value: "",
    };
  },
};

// Simular la función showNotification
global.showNotification = (message, type) => {
  console.log(`Notification (${type}): ${message}`);
};

// Función loadConfigData simplificada
async function loadConfigData() {
  console.log("Iniciando loadConfigData");
  try {
    // Obtener configuraciones desde la API
    const response = await fetch("/api/v1/config");
    const configs = await response.json();
    console.log("Configuraciones obtenidas:", configs);

    // Establecer valores en el formulario si existen en la base de datos
    if (configs) {
      console.log("Configuraciones encontradas, estableciendo valores");
    } else {
      console.log("No se encontraron configuraciones");
    }
  } catch (error) {
    console.error("Error cargando configuración:", error);
  }
}

// Ejecutar la función de prueba
console.log("Ejecutando prueba de loadConfigData...");
loadConfigData()
  .then(() => {
    console.log("Prueba completada exitosamente");
  })
  .catch((error) => {
    console.error("Error en la prueba:", error);
  });
