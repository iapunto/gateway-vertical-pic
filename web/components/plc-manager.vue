<template>
  <div class="plc-manager">
    <div class="card">
      <div class="card-header">
        <h3>Gestión de PLCs</h3>
        <div class="card-actions">
          <button class="btn btn-primary" @click="openCreateModal">
            <i class="fas fa-plus"></i> Nuevo PLC
          </button>
          <button class="btn btn-outline" @click="refreshPLCs">
            <i class="fas fa-sync-alt"></i> Actualizar
          </button>
        </div>
      </div>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Dirección IP</th>
              <th>Puerto</th>
              <th>Estado</th>
              <th>Última Conexión</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="plc in plcs" :key="plc.id">
              <td>{{ plc.id }}</td>
              <td>{{ plc.name }}</td>
              <td>{{ plc.ip }}</td>
              <td>{{ plc.port }}</td>
              <td>
                <span class="status-indicator" :class="plc.status"></span>
                {{ plc.status === "online" ? "En línea" : "Fuera de línea" }}
              </td>
              <td>{{ plc.lastSeen }}</td>
              <td>
                <button class="btn btn-outline btn-sm" @click="editPLC(plc)">
                  <i class="fas fa-edit"></i>
                </button>
                <button
                  class="btn btn-danger btn-sm"
                  @click="deletePLC(plc.id)"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </td>
            </tr>
            <tr v-if="plcs.length === 0">
              <td colspan="7" class="text-center">No hay PLCs registrados</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal para crear/editar PLC -->
    <div class="modal" :class="{ 'is-active': showPLCModal }">
      <div class="modal-background" @click="closePLCModal"></div>
      <div class="modal-content">
        <div class="card">
          <div class="card-header">
            <h3>{{ editingPLC ? "Editar PLC" : "Nuevo PLC" }}</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="savePLC">
              <div class="form-group">
                <label for="plcId">ID del PLC</label>
                <input
                  type="text"
                  id="plcId"
                  v-model="currentPLC.id"
                  required
                  :disabled="editingPLC"
                />
              </div>
              <div class="form-group">
                <label for="plcName">Nombre</label>
                <input
                  type="text"
                  id="plcName"
                  v-model="currentPLC.name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="plcIP">Dirección IP</label>
                <input
                  type="text"
                  id="plcIP"
                  v-model="currentPLC.ip"
                  required
                />
              </div>
              <div class="form-group">
                <label for="plcPort">Puerto</label>
                <input
                  type="number"
                  id="plcPort"
                  v-model="currentPLC.port"
                  required
                />
              </div>
              <div class="form-group">
                <label for="plcType">Tipo</label>
                <select id="plcType" v-model="currentPLC.type" required>
                  <option value="delta">Delta</option>
                  <option value="siemens">Siemens</option>
                  <option value="allen-bradley">Allen-Bradley</option>
                </select>
              </div>
              <div class="form-group">
                <label for="plcDescription">Descripción</label>
                <textarea
                  id="plcDescription"
                  v-model="currentPLC.description"
                ></textarea>
              </div>
              <div class="form-actions">
                <button
                  type="button"
                  class="btn btn-outline"
                  @click="closePLCModal"
                >
                  Cancelar
                </button>
                <button type="submit" class="btn btn-primary">Guardar</button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <button
        class="modal-close is-large"
        aria-label="close"
        @click="closePLCModal"
      ></button>
    </div>

    <!-- Modal de confirmación de eliminación -->
    <div class="modal" :class="{ 'is-active': showDeleteConfirm }">
      <div class="modal-background" @click="closeDeleteConfirm"></div>
      <div class="modal-content">
        <div class="card">
          <div class="card-header">
            <h3>Confirmar Eliminación</h3>
          </div>
          <div class="card-body">
            <p>¿Está seguro que desea eliminar el PLC {{ plcToDelete }}?</p>
            <div class="form-actions">
              <button class="btn btn-outline" @click="closeDeleteConfirm">
                Cancelar
              </button>
              <button class="btn btn-danger" @click="confirmDelete">
                Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>
      <button
        class="modal-close is-large"
        aria-label="close"
        @click="closeDeleteConfirm"
      ></button>
    </div>
  </div>
</template>

<script>
export default {
  name: "PLCManager",
  data() {
    return {
      plcs: [],
      showPLCModal: false,
      showDeleteConfirm: false,
      editingPLC: false,
      plcToDelete: null,
      currentPLC: {
        id: "",
        name: "",
        ip: "",
        port: 3200,
        type: "delta",
        description: "",
      },
    };
  },
  mounted() {
    this.loadPLCs();
  },
  methods: {
    async loadPLCs() {
      try {
        // En una implementación real, esto haría una llamada a la API
        // const response = await fetch('/api/v1/plcs');
        // this.plcs = await response.json();

        // Simulación de datos
        this.plcs = [
          {
            id: "PLC-001",
            name: "Carrusel Principal",
            ip: "192.168.1.101",
            port: 3200,
            type: "delta",
            description: "PLC Delta AS Series principal",
            status: "online",
            lastSeen: "2023-05-15 10:30:25",
          },
          {
            id: "PLC-002",
            name: "Carrusel Secundario",
            ip: "192.168.1.102",
            port: 3200,
            type: "delta",
            description: "PLC Delta AS Series secundario",
            status: "online",
            lastSeen: "2023-05-15 10:28:42",
          },
        ];
      } catch (error) {
        console.error("Error cargando PLCs:", error);
      }
    },
    refreshPLCs() {
      this.loadPLCs();
    },
    openCreateModal() {
      this.editingPLC = false;
      this.currentPLC = {
        id: "",
        name: "",
        ip: "",
        port: 3200,
        type: "delta",
        description: "",
      };
      this.showPLCModal = true;
    },
    editPLC(plc) {
      this.editingPLC = true;
      this.currentPLC = { ...plc };
      this.showPLCModal = true;
    },
    closePLCModal() {
      this.showPLCModal = false;
    },
    async savePLC() {
      try {
        // En una implementación real, esto haría una llamada a la API
        // const response = await fetch('/api/v1/plcs', {
        //   method: this.editingPLC ? 'PUT' : 'POST',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify(this.currentPLC)
        // });

        // Simulación de guardado
        if (this.editingPLC) {
          const index = this.plcs.findIndex((p) => p.id === this.currentPLC.id);
          if (index !== -1) {
            this.plcs.splice(index, 1, { ...this.currentPLC });
          }
        } else {
          this.plcs.push({
            ...this.currentPLC,
            status: "offline",
            lastSeen: new Date().toISOString(),
          });
        }

        this.closePLCModal();
        this.$emit("notification", {
          message: this.editingPLC
            ? "PLC actualizado correctamente"
            : "PLC creado correctamente",
          type: "success",
        });
      } catch (error) {
        this.$emit("notification", {
          message: "Error al guardar el PLC: " + error.message,
          type: "error",
        });
      }
    },
    deletePLC(plcId) {
      this.plcToDelete = plcId;
      this.showDeleteConfirm = true;
    },
    closeDeleteConfirm() {
      this.showDeleteConfirm = false;
      this.plcToDelete = null;
    },
    async confirmDelete() {
      try {
        // En una implementación real, esto haría una llamada a la API
        // await fetch(`/api/v1/plcs/${this.plcToDelete}`, { method: 'DELETE' });

        // Simulación de eliminación
        this.plcs = this.plcs.filter((p) => p.id !== this.plcToDelete);

        this.closeDeleteConfirm();
        this.$emit("notification", {
          message: "PLC eliminado correctamente",
          type: "success",
        });
      } catch (error) {
        this.$emit("notification", {
          message: "Error al eliminar el PLC: " + error.message,
          type: "error",
        });
      }
    },
  },
};
</script>

<style scoped>
.plc-manager {
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
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
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

.status-indicator.online {
  background-color: #4ade80;
}

.status-indicator.offline {
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
