<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'
import StatusLed from '../components/StatusLed.vue'

const store = useLaboratoryStore()
const open = ref(false)
const editingId = ref(null)
const form = reactive({ projectCode: '', name: '' })

onMounted(() => store.fetchProjects())

function openCreate() {
  editingId.value = null
  Object.assign(form, { projectCode: '', name: '' })
  open.value = true
}
function openEdit(p) {
  editingId.value = p.id
  Object.assign(form, { projectCode: p.projectCode, name: p.name })
  open.value = true
}

async function submit() {
  const ok = editingId.value
    ? await store.editProject(editingId.value, { ...form })
    : await store.addProject({ ...form })
  if (ok) open.value = false
}

async function remove(p) {
  if (window.confirm(`Delete project ${p.projectCode}? This cannot be undone.`)) {
    await store.removeProject(p.id)
  }
}
</script>

<template>
  <section>
    <PageHeader title="Projects" subtitle="Work that demand is raised against">
      <template #actions>
        <button class="btn btn--primary" @click="openCreate">+ New project</button>
      </template>
    </PageHeader>

    <div class="panel">
      <table v-if="store.projects.length" class="table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Status</th>
            <th class="right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in store.projects" :key="p.id">
            <td class="mono cell-strong">{{ p.projectCode }}</td>
            <td class="cell-strong">{{ p.name }}</td>
            <td><StatusLed :status="p.active ? 'active' : 'inactive'" /></td>
            <td class="right actions">
              <button class="btn btn--sm btn--ghost" @click="openEdit(p)">Edit</button>
              <button
                class="btn btn--sm btn--ghost"
                @click="store.setActive('projects', p.id, !p.active)"
              >
                {{ p.active ? 'Deactivate' : 'Activate' }}
              </button>
              <button class="btn btn--sm btn--ghost danger" @click="remove(p)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No projects yet. Create one to raise demand against it.</p>
      <p v-if="store.error" class="error err">{{ store.error }}</p>
    </div>

    <SlideOver
      :open="open"
      :title="editingId ? 'Edit project' : 'New project'"
      @close="open = false"
    >
      <form class="stack" @submit.prevent="submit">
        <div class="field">
          <label>Project code</label>
          <input v-model="form.projectCode" placeholder="PRJ-001" required />
        </div>
        <div class="field">
          <label>Name</label>
          <input v-model="form.name" placeholder="Assay development" required />
        </div>
        <p v-if="store.error" class="error">{{ store.error }}</p>
        <button class="btn btn--primary" type="submit">
          {{ editingId ? 'Save' : 'Add project' }}
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
</style>
