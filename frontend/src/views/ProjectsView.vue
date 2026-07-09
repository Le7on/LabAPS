<script setup>
import { onMounted, reactive } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'

const store = useLaboratoryStore()
const form = reactive({ projectCode: '', name: '' })

onMounted(() => store.fetchProjects())

async function submit() {
  const ok = await store.addProject({ ...form })
  if (ok) {
    form.projectCode = ''
    form.name = ''
  }
}
</script>

<template>
  <section class="stack">
    <h2>Projects</h2>

    <div class="card">
      <div class="card__title">New project</div>
      <form class="form-row" @submit.prevent="submit">
        <div class="field">
          <label>Project code</label>
          <input v-model="form.projectCode" placeholder="PRJ-001" required />
        </div>
        <div class="field">
          <label>Name</label>
          <input v-model="form.name" placeholder="Assay development" required />
        </div>
        <button class="btn btn--primary" type="submit">Add project</button>
      </form>
      <p v-if="store.error" class="error">{{ store.error }}</p>
    </div>

    <div class="card">
      <table v-if="store.projects.length" class="table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Active</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in store.projects" :key="p.id">
            <td>{{ p.projectCode }}</td>
            <td>{{ p.name }}</td>
            <td>
              <span class="badge" :class="p.active ? 'badge--success' : ''">
                {{ p.active ? 'active' : 'inactive' }}
              </span>
            </td>
            <td>
              <button class="btn btn--ghost" @click="store.setActive('projects', p.id, !p.active)">
                {{ p.active ? 'Deactivate' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No projects yet.</p>
    </div>
  </section>
</template>
