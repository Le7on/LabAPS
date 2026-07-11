<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'
import StatusLed from '../components/StatusLed.vue'
import MultiSelect from '../components/MultiSelect.vue'

const store = useLaboratoryStore()
const open = ref(false)
const form = reactive({ staffCode: '', name: '', qualifiedProjectIds: [] })

onMounted(() => {
  store.fetchStaff()
  store.fetchProjects()
})

const projectOptions = computed(() =>
  store.projects.map((p) => ({ value: p.id, label: `${p.projectCode} · ${p.name}` }))
)
const projectName = (id) => store.projects.find((p) => p.id === id)?.name ?? id.slice(0, 6)

async function submit() {
  const ok = await store.addStaff({
    staffCode: form.staffCode,
    name: form.name,
    qualifiedProjectIds: [...form.qualifiedProjectIds],
  })
  if (ok) {
    Object.assign(form, { staffCode: '', name: '', qualifiedProjectIds: [] })
    open.value = false
  }
}
</script>

<template>
  <section>
    <PageHeader title="Staff" subtitle="Operators and the projects they are qualified to run">
      <template #actions>
        <button class="btn btn--primary" @click="open = true">+ New staff</button>
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
            <th></th>
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
            <td class="right">
              <button
                class="btn btn--sm btn--ghost"
                @click="store.setActive('staff', s.id, !s.active)"
              >
                {{ s.active ? 'Deactivate' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No staff yet.</p>
    </div>

    <SlideOver :open="open" title="New staff member" @close="open = false">
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
        <button class="btn btn--primary" type="submit">Add staff</button>
      </form>
    </SlideOver>
  </section>
</template>

<style scoped>
.right {
  text-align: right;
}
.hint {
  font-size: 12px;
  margin: 0;
}
</style>
