// Script para probar la carga de PLCs en el frontend

// Simular el entorno del navegador
const mockDocument = {
  readyState: "complete",
  getElementById: function (id) {
    console.log(`getElementById: ${id}`);
    // Simular los elementos necesarios
    const elements = {
      "plcs-table": {
        getElementsByTagName: function (tagName) {
          if (tagName === "tbody") {
            return [
              {
                innerHTML: "",
                insertRow: function () {
                  return {
                    innerHTML: "",
                  };
                },
              },
            ];
          }
          return [];
        },
      },
    };

    return elements[id] || null;
  },
};

// Simular fetch
async function mockFetch(url) {
  console.log(`fetch: ${url}`);
  if (url === "/api/v1/plcs") {
    return {
      ok: true,
      status: 200,
      json: async () => [
        {
          created_at: "2025-10-02 19:07:46",
          description: "",
          id: 3,
          ip_address: "192.168.1.50",
          name: "Vertical PIC Principal",
          plc_id: "PLC-1759432066207",
          port: 3200,
          type: "delta",
          updated_at: "2025-10-02 19:07:46",
        },
      ],
    };
  }
  return { ok: true, status: 200, json: async () => [] };
}

// Variables globales
const API_BASE_URL = "/api/v1";

// Función auxiliar
function showNotification(message, type = "info") {
  console.log(`[NOTIFICATION] ${type}: ${message}`);
}

// Función loadPLCsData (versión del frontend)
async function loadPLCsData() {
  console.log("Iniciando loadPLCsData");
  try {
    const response = await mockFetch(`${API_BASE_URL}/plcs`);
    const plcs = await response.json();
    console.log("PLCs obtenidos", plcs);

    const plcsTable = mockDocument
      .getElementById("plcs-table")
      .getElementsByTagName("tbody")[0];
    plcsTable.innerHTML = "";

    if (!plcs || plcs.length === 0) {
      console.log("No hay PLCs registrados");
      return;
    }

    plcs.forEach((plc) => {
      console.log("Procesando PLC", plc);
      console.log("Datos del PLC:", {
        plc_id: plc.plc_id || plc.id,
        name: plc.name || "Sin nombre",
        ip_address: plc.ip_address || "N/A",
        port: plc.port || "N/A",
        updated_at: plc.updated_at,
      });
    });
  } catch (error) {
    console.error("Error cargando PLCs:", error);
    showNotification("Error cargando PLCs", "error");
  }
}

// Ejecutar la prueba
console.log("Iniciando prueba de carga de PLCs");
loadPLCsData();
