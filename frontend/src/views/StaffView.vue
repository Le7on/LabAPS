<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'
import StatusLed from '../components/StatusLed.vue'
import MultiSelect from '../components/MultiSelect.vue'

const store = useLaboratoryStore()
const open = ref(false)
const editingId = ref(null)
const form = reactive({ staffCode: '', name: '', qualifiedProjectIds: [] })

onMounted(() => {
  store.fetchStaff()
  store.fetchProjects()
})

const projectOptions = computed(() =>
  store.projects.map((p) => ({ value: p.id, label: `${p.projectCode} · ${p.name}` }))
)
const projectName = (id) => store.projects.find((p) => p.id === id)?.name ?? id.slice(0, 6)

function openCreate() {
  editingId.value = null
  Object.assign(form, { staffCode: '', name: '', qualifiedProjectIds: [] })
  open.value = true
}
function openEdit(s) {
  editingId.value = s.id
  Object.assign(form, {
    staffCode: s.staffCode,
    name: s.name,
    qualifiedProjectIds: [...s.qualifiedProjectIds],
  })
  open.value = true
}

async function submit() {
  const payload = {
    staffCode: form.staffCode,
    name: form.name,
    qualifiedProjectIds: [...form.qualifiedProjectIds],
  }
  const ok = editingId.value
    ? await store.editStaff(editingId.value, payload)
    : await store.addStaff(payload)
  if (ok) open.value = false
}

async function remove(s) {
  if (window.confirm(`Delete staff ${s.staffCode}?`)) await store.removeStaff(s.id)
}
</script>

<template>
  <section>
    <PageHeader title="Staff" subtitle="Operators and the projects they are qualified to run">
      <template #actions>
        <button class="btn btn--primary" @click="openCreate">+ New staff</button>
      </template>
    </PageHeader>

    <div class="panel">
      <table v-if="store.staff.length" class="table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Qualified projects (skills)</th>
            <th>Status</th>
            <th class="right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in store.staff" :key="s.id">
            <td class="mono cell-strong">{{ s.staffCode }}</td>
            <td class="cell-strong">{{ s.name }}</td>
            <td>
              <span v-for="pid in s.qualifiedProjectIds" :key="pid" class="chip">{{
                projectName(pid)
              }}</span>
              <span v-if="!s.qualifiedProjectIds.length" class="muted">—</span>
            </td>
            <td><StatusLed :status="s.active ? 'active' : 'inactive'" /></td>
            <td class="right actions">
              <button class="btn btn--sm btn--ghost" @click="openEdit(s)">Edit</button>
              <button
                class="btn btn--sm btn--ghost"
                @click="store.setActive('staff', s.id, !s.active)"
              >
                {{ s.active ? 'Deactivate' : 'Activate' }}
              </button>
              <button class="btn btn--sm btn--ghost danger" @click="remove(s)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No staff yet.</p>
      <p v-if="store.error" class="error err">{{ store.error }}</p>
    </div>

    <SlideOver
      :open="open"
      :title="editingId ? 'Edit staff' : 'New staff member'"
      @close="open = false"
    >
      <form class="stack" @submit.prevent="submit">
        <div class="field">
          <label>Code</label>
          <input v-model="form.staffCode" placeholder="ST-001" required />
        </div>
        <div class="field">
          <label>Name</label>
          <input v-model="form.name" placeholder="Alice" required />
        </div>
        <div class="field">
          <label>Qualified projects (skills)</label>
          <MultiSelect
            v-model="form.qualifiedProjectIds"
            :options="projectOptions"
            placeholder="Select projects this person can run…"
          />
        </div>
        <p class="muted hint">
          A staff member can perform any method of a project they are qualified for.
        </p>
        <p v-if="store.error" class="error">{{ store.error }}</p>
        <button class="btn btn--primary" type="submit">
          {{ editingId ? 'Save' : 'Add staff' }}
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
.hint {
  font-size: 12px;
  margin: 0;
}
.err {
  padding: var(--s3) var(--s4);
  margin: 0;
}
</style>
