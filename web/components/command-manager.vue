<template>
  <div class="command-manager">
    <div class="card">
      <div class="card-header">
        <h3>Comandos</h3>
        <div class="card-actions">
          <button class="btn btn-primary" @click="openCommandModal">
            <i class="fas fa-paper-plane"></i> Enviar Comando
          </button>
          <button class="btn btn-outline" @click="refreshCommands">
            <i class="fas fa-sync-alt"></i> Actualizar
          </button>
        </div>
      </div>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Fecha/Hora</th>
              <th>Comando</th>
              <th>Máquina</th>
              <th>Argumento</th>
              <th>Estado</th>
              <th>Respuesta</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="command in commands" :key="command.id">
              <td>{{ command.timestamp }}</td>
              <td>{{ command.command }}</td>
              <td>{{ command.machine }}</td>
              <td>{{ command.argument || "-" }}</td>
              <td>
                <span class="status-indicator" :class="command.status"></span>
                {{ command.status === "success" ? "Éxito" : "Error" }}
              </td>
              <td>{{ command.response }}</td>
            </tr>
            <tr v-if="commands.length === 0">
              <td colspan="6" class="text-center">
                No hay comandos registrados
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal para enviar comando -->
    <div class="modal" :class="{ 'is-active': showCommandModal }">
      <div class="modal-background" @click="closeCommandModal"></div>
      <div class="modal-content">
        <div class="card">
          <div class="card-header">
            <h3>Enviar Comando</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="sendCommand">
              <div class="form-group">
                <label for="commandType">Comando</label>
                <select
                  id="commandType"
                  v-model="currentCommand.command"
                  required
                >
                  <option value="">Seleccionar comando...</option>
                  <option value="STATUS">Obtener Estado</option>
                  <option value="MOVE">Mover a Posición</option>
                  <option value="START">Iniciar</option>
                  <option value="STOP">Detener</option>
                  <option value="RESET">Reiniciar</option>
                </select>
              </div>
              <div class="form-group">
                <label for="commandMachine">Máquina</label>
                <select
                  id="commandMachine"
                  v-model="currentCommand.machine"
                  required
                >
                  <option value="">Seleccionar máquina...</option>
                  <option v-for="plc in plcs" :key="plc.id" :value="plc.id">
                    {{ plc.name }} ({{ plc.id }})
                  </option>
                </select>
              </div>
              <div class="form-group" v-if="currentCommand.command === 'MOVE'">
                <label for="commandArgument">Posición</label>
                <input
                  type="number"
                  id="commandArgument"
                  v-model="currentCommand.argument"
                  min="0"
                />
              </div>
              <div class="form-actions">
                <button
                  type="button"
                  class="btn btn-outline"
                  @click="closeCommandModal"
                >
                  Cancelar
                </button>
                <button type="submit" class="btn btn-primary">Enviar</button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <button
        class="modal-close is-large"
        aria-label="close"
        @click="closeCommandModal"
      ></button>
    </div>
  </div>
</template>

<script>
export default {
  name: "CommandManager",
  props: {
    plcs: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      commands: [],
      showCommandModal: false,
      currentCommand: {
        command: "",
        machine: "",
        argument: null,
      },
    };
  },
  mounted() {
    this.loadCommands();
  },
  methods: {
    async loadCommands() {
      try {
        // En una implementación real, esto haría una llamada a la API
        // const response = await fetch('/api/v1/commands');
        // this.commands = await response.json();

        // Simulación de datos
        this.commands = [
          {
            id: 1,
            timestamp: "2023-05-15 10:30:25",
            command: "MOVE",
            machine: "PLC-001",
            argument: 5,
            status: "success",
            response: "OK",
          },
          {
            id: 2,
            timestamp: "2023-05-15 10:28:42",
            command: "STATUS",
            machine: "PLC-002",
            argument: null,
            status: "success",
            response: "Position: 3, Status: Running",
          },
        ];
      } catch (error) {
        console.error("Error cargando comandos:", error);
      }
    },
    refreshCommands() {
      this.loadCommands();
    },
    openCommandModal() {
      this.currentCommand = {
        command: "",
        machine: "",
        argument: null,
      };
      this.showCommandModal = true;
    },
    closeCommandModal() {
      this.showCommandModal = false;
    },
    async sendCommand() {
      try {
        // En una implementación real, esto haría una llamada a la API
        // const response = await fetch('/api/v1/command', {
        //   method: 'POST',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify(this.currentCommand)
        // });

        // Simulación de envío de comando
        const newCommand = {
          id: this.commands.length + 1,
          timestamp: new Date().toISOString().slice(0, 19).replace("T", " "),
          command: this.currentCommand.command,
          machine: this.currentCommand.machine,
          argument: this.currentCommand.argument,
          status: "success",
          response: "Command executed successfully",
        };

        this.commands.unshift(newCommand);
        this.closeCommandModal();
        this.$emit("notification", {
          message: "Comando enviado correctamente",
          type: "success",
        });
      } catch (error) {
        this.$emit("notification", {
          message: "Error al enviar el comando: " + error.message,
          type: "error",
        });
      }
    },
  },
};
</script>

<style scoped>
.command-manager {
  padding: 20px;
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

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.status-indicator {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 5px;
}

.status-indicator.success {
  background-color: #4ade80;
}

.status-indicator.error {
  background-color: #ef4444;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 0.8rem;
}

.text-center {
  text-align: center;
}

.modal {
  display: none;
}

.modal.is-active {
  display: block;
}

.modal-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.modal-content {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1001;
  width: 90%;
  max-width: 600px;
}

.modal-close {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1002;
}
</style>
