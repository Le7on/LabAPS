<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'
import MultiSelect from '../components/MultiSelect.vue'

const store = useLaboratoryStore()
const open = ref(false)
const editingId = ref(null)

function emptyMethod() {
  return {
    key: crypto.randomUUID(),
    operationType: '',
    duration: 1,
    equipmentIds: [],
    dependsOn: [],
  }
}

const form = reactive({ workflowCode: '', name: '', projectId: '', methods: [emptyMethod()] })

function openCreate() {
  editingId.value = null
  Object.assign(form, { workflowCode: '', name: '', projectId: '', methods: [emptyMethod()] })
  open.value = true
}

function openEdit(wf) {
  editingId.value = wf.id
  Object.assign(form, {
    workflowCode: wf.workflowCode,
    name: wf.name,
    projectId: wf.projectId,
    methods: wf.operations.map((op) => ({
      key: crypto.randomUUID(),
      operationType: op.operationType,
      duration: op.duration,
      equipmentIds: [...op.equipmentIds],
      // dependsOn is stored as method ids; map back to method names for the UI.
      dependsOn: op.dependsOn
        .map((depId) => wf.operations.find((o) => o.id === depId)?.operationType)
        .filter(Boolean),
    })),
  })
  if (!form.methods.length) form.methods.push(emptyMethod())
  open.value = true
}

onMounted(() => {
  store.fetchWorkflows()
  store.fetchProjects()
  store.fetchEquipment()
})

const projectOptions = computed(() =>
  store.projects.map((p) => ({ value: p.id, label: `${p.projectCode} · ${p.name}` }))
)
const equipmentOptions = computed(() =>
  store.equipment.map((e) => ({ value: e.id, label: `${e.equipmentCode} · ${e.name}` }))
)
// Prerequisites = earlier methods, referenced by their (unique) method name.
function prereqOptions(index) {
  return form.methods
    .slice(0, index)
    .filter((m) => m.operationType.trim())
    .map((m) => ({ value: m.operationType.trim(), label: m.operationType.trim() }))
}

const projectName = (id) => store.projects.find((p) => p.id === id)?.name ?? '—'

function addMethod() {
  form.methods.push(emptyMethod())
}
function removeMethod(i) {
  form.methods.splice(i, 1)
}

async function submit() {
  // Dependencies are expressed by prerequisite method name (unique per workflow).
  const operations = form.methods
    .filter((m) => m.operationType.trim())
    .map((m) => ({
      operationType: m.operationType.trim(),
      duration: Number(m.duration) || 1,
      equipmentIds: [...m.equipmentIds],
      dependsOn: [...m.dependsOn],
    }))

  const payload = {
    workflowCode: form.workflowCode,
    name: form.name,
    projectId: form.projectId,
    operations,
  }
  const ok = editingId.value
    ? await store.editWorkflow(editingId.value, payload)
    : await store.addWorkflow(payload)
  if (ok) open.value = false
}

async function remove(wf) {
  if (window.confirm(`Delete workflow ${wf.workflowCode}?`)) await store.removeWorkflow(wf.id)
}
</script>

<template>
  <section>
    <PageHeader
      title="Workflows"
      subtitle="Per project: the methods that make it, with work-hours and order"
    >
      <template #actions>
        <button class="btn btn--primary" :disabled="!store.projects.length" @click="openCreate">
          + New workflow
        </button>
      </template>
    </PageHeader>

    <p v-if="!store.projects.length" class="empty">
      Create a Project first — a workflow belongs to one project.
    </p>

    <div v-else class="panel">
      <table v-if="store.workflows.length" class="table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Project</th>
            <th>Methods</th>
            <th class="right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="wf in store.workflows" :key="wf.id">
            <td class="mono cell-strong">{{ wf.workflowCode }}</td>
            <td class="cell-strong">{{ wf.name }}</td>
            <td>{{ projectName(wf.projectId) }}</td>
            <td class="mono">{{ wf.operations.length }}</td>
            <td class="right actions">
              <button class="btn btn--sm btn--ghost" @click="openEdit(wf)">Edit</button>
              <button class="btn btn--sm btn--ghost danger" @click="remove(wf)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No workflows yet.</p>
      <p v-if="store.error" class="error err">{{ store.error }}</p>
    </div>

    <SlideOver
      :open="open"
      :title="editingId ? 'Edit workflow' : 'New workflow'"
      @close="open = false"
    >
      <form class="stack" @submit.prevent="submit">
        <div class="field">
          <label>Project</label>
          <select v-model="form.projectId" required>
            <option value="">Select project…</option>
            <option v-for="p in projectOptions" :key="p.value" :value="p.value">
              {{ p.label }}
            </option>
          </select>
        </div>
        <div class="field">
          <label>Workflow code</label>
          <input v-model="form.workflowCode" placeholder="WF-001" required />
        </div>
        <div class="field">
          <label>Name</label>
          <input v-model="form.name" placeholder="Standard prep" required />
        </div>

        <div class="methods">
          <div class="label">Methods</div>
          <div v-for="(m, i) in form.methods" :key="m.key" class="method">
            <div class="method__head">
              <span class="method__n mono">#{{ i + 1 }}</span>
              <button class="btn btn--sm btn--ghost" type="button" @click="removeMethod(i)">
                ✕
              </button>
            </div>
            <div class="field">
              <label>Method name</label>
              <input v-model="m.operationType" placeholder="e.g. amplify" />
            </div>
            <div class="field">
              <label>Work-hours (hours)</label>
              <input v-model.number="m.duration" type="number" min="1" step="1" />
            </div>
            <div class="field">
              <label>Runs on equipment</label>
              <MultiSelect
                v-model="m.equipmentIds"
                :options="equipmentOptions"
                placeholder="Any bound equipment…"
              />
            </div>
            <div v-if="prereqOptions(i).length" class="field">
              <label>Depends on (prerequisite methods)</label>
              <MultiSelect v-model="m.dependsOn" :options="prereqOptions(i)" placeholder="None…" />
            </div>
          </div>
          <button class="btn btn--sm" type="button" @click="addMethod">+ Method</button>
        </div>

        <p v-if="store.error" class="error">{{ store.error }}</p>
        <button class="btn btn--primary" type="submit">
          {{ editingId ? 'Save workflow' : 'Create workflow' }}
        </button>
      </form>
    </SlideOver>
  </section>
</template>

<style scoped>
.right {
  text-align: right;
}
.actions {
  display: flex;
  gap: 4px;
  justify-content: flex-end;
}
.danger {
  color: var(--led-danger);
}
.err {
  padding: var(--s3) var(--s4);
  margin: 0;
}
.methods {
  display: flex;
  flex-direction: column;
  gap: var(--s2);
}
.method {
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  padding: var(--s3);
  background: var(--panel-2);
  display: flex;
  flex-direction: column;
  gap: var(--s2);
}
.method__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.method__n {
  font-size: 11px;
  color: var(--ink-3);
}
</style>
