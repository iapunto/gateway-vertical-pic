<template>
  <div class="config-manager">
    <div class="card">
      <div class="card-header">
        <h3>Configuración del Gateway</h3>
      </div>
      <div class="card-body">
        <form @submit.prevent="saveConfig">
          <div class="config-section">
            <h4>Configuración de Red</h4>
            <div class="form-group">
              <label for="bindAddress">Dirección IP de Escucha</label>
              <input
                type="text"
                id="bindAddress"
                v-model="config.network.bindAddress"
                required
              />
            </div>
            <div class="form-group">
              <label for="bindPort">Puerto de Escucha</label>
              <input
                type="number"
                id="bindPort"
                v-model="config.network.bindPort"
                required
              />
            </div>
            <div class="form-group">
              <label for="plcPort">Puerto PLC</label>
              <input
                type="number"
                id="plcPort"
                v-model="config.network.plcPort"
                required
              />
            </div>
          </div>

          <div class="config-section">
            <h4>Configuración WMS</h4>
            <div class="form-group">
              <label for="wmsEndpoint">Endpoint WMS</label>
              <input
                type="text"
                id="wmsEndpoint"
                v-model="config.wms.endpoint"
              />
            </div>
            <div class="form-group">
              <label for="reconnectInterval"
                >Intervalo de Reconexión (segundos)</label
              >
              <input
                type="number"
                id="reconnectInterval"
                v-model="config.wms.reconnectInterval"
              />
            </div>
            <div class="form-group">
              <label for="heartbeatInterval"
                >Intervalo de Heartbeat (segundos)</label
              >
              <input
                type="number"
                id="heartbeatInterval"
                v-model="config.wms.heartbeatInterval"
              />
            </div>
          </div>

          <div class="config-section">
            <h4>Configuración de Seguridad</h4>
            <div class="form-group">
              <label for="requireTLS">Requerir TLS</label>
              <input
                type="checkbox"
                id="requireTLS"
                v-model="config.security.requireTLS"
              />
            </div>
          </div>

          <div class="config-section">
            <h4>Configuración de Logging</h4>
            <div class="form-group">
              <label for="logLevel">Nivel de Log</label>
              <select id="logLevel" v-model="config.logging.level">
                <option value="DEBUG">DEBUG</option>
                <option value="INFO">INFO</option>
                <option value="WARNING">WARNING</option>
                <option value="ERROR">ERROR</option>
              </select>
            </div>
            <div class="form-group">
              <label for="logFile">Archivo de Log</label>
              <input type="text" id="logFile" v-model="config.logging.file" />
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary">
              <i class="fas fa-save"></i> Guardar Configuración
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConfigManager",
  data() {
    return {
      config: {
        network: {
          bindAddress: "0.0.0.0",
          bindPort: 8080,
          plcPort: 3200,
        },
        wms: {
          endpoint: "",
          reconnectInterval: 30,
          heartbeatInterval: 60,
        },
        security: {
          requireTLS: false,
        },
        logging: {
          level: "INFO",
          file: "logs/gateway.log",
        },
      },
    };
  },
  mounted() {
    this.loadConfig();
  },
  methods: {
    async loadConfig() {
      try {
        // En una implementación real, esto haría una llamada a la API
        // const response = await fetch('/api/v1/config');
        // this.config = await response.json();

        // Simulación de datos
        this.config = {
          network: {
            bindAddress: "0.0.0.0",
            bindPort: 8080,
            plcPort: 3200,
          },
          wms: {
            endpoint: "https://wms.example.com/api/v1/gateways",
            reconnectInterval: 30,
            heartbeatInterval: 60,
          },
          security: {
            requireTLS: false,
          },
          logging: {
            level: "INFO",
            file: "logs/gateway.log",
          },
        };
      } catch (error) {
        console.error("Error cargando configuración:", error);
      }
    },
    async saveConfig() {
      try {
        // En una implementación real, esto haría una llamada a la API
        // const response = await fetch('/api/v1/config', {
        //   method: 'PUT',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify(this.config)
        // });

        // Simulación de guardado
        this.$emit("notification", {
          message: "Configuración guardada correctamente",
          type: "success",
        });
      } catch (error) {
        this.$emit("notification", {
          message: "Error al guardar la configuración: " + error.message,
          type: "error",
        });
      }
    },
  },
};
</script>

<style scoped>
.config-manager {
  padding: 20px;
}

.config-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.config-section:last-child {
  border-bottom: none;
}

.config-section h4 {
  margin-bottom: 15px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
}

.form-group input[type="checkbox"] {
  width: auto;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
}
</style>
