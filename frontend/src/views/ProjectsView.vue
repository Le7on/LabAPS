<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'
import StatusLed from '../components/StatusLed.vue'

const store = useLaboratoryStore()
const open = ref(false)
const form = reactive({ projectCode: '', name: '' })

onMounted(() => store.fetchProjects())

async function submit() {
  const ok = await store.addProject({ ...form })
  if (ok) {
    form.projectCode = ''
    form.name = ''
    open.value = false
  }
}
</script>

<template>
  <section>
    <PageHeader title="Projects" subtitle="Work that demand is raised against">
      <template #actions>
        <button class="btn btn--primary" @click="open = true">+ New project</button>
      </template>
    </PageHeader>

    <div class="panel">
      <table v-if="store.projects.length" class="table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in store.projects" :key="p.id">
            <td class="mono cell-strong">{{ p.projectCode }}</td>
            <td class="cell-strong">{{ p.name }}</td>
            <td><StatusLed :status="p.active ? 'active' : 'inactive'" /></td>
            <td class="right">
              <button
                class="btn btn--sm btn--ghost"
                @click="store.setActive('projects', p.id, !p.active)"
              >
                {{ p.active ? 'Deactivate' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No projects yet. Create one to raise demand against it.</p>
    </div>

    <SlideOver :open="open" title="New project" @close="open = false">
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
        <button class="btn btn--primary" type="submit">Add project</button>
      </form>
    </SlideOver>
  </section>
</template>

<style scoped>
.right {
  text-align: right;
}
</style>
