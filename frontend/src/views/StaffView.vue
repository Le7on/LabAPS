<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import {
  parseList,
  parseWindows,
  parseQualifications,
  formatWindows,
  formatQualifications,
} from '../utils/parse'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'
import StatusLed from '../components/StatusLed.vue'

const store = useLaboratoryStore()
const open = ref(false)
const form = reactive({ staffCode: '', name: '', skills: '', qualifications: '', availability: '' })

onMounted(() => store.fetchStaff())

async function submit() {
  const ok = await store.addStaff({
    staffCode: form.staffCode,
    name: form.name,
    skills: parseList(form.skills),
    qualifications: parseQualifications(form.qualifications),
    availability: parseWindows(form.availability),
  })
  if (ok) {
    Object.assign(form, {
      staffCode: '',
      name: '',
      skills: '',
      qualifications: '',
      availability: '',
    })
    open.value = false
  }
}
</script>

<template>
  <section>
    <PageHeader title="Staff" subtitle="Operators, their skills, qualifications and availability">
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
            <th>Skills</th>
            <th>Qualifications</th>
            <th>Availability</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in store.staff" :key="s.id">
            <td class="mono cell-strong">{{ s.staffCode }}</td>
            <td class="cell-strong">{{ s.name }}</td>
            <td>
              <span v-for="sk in s.skills" :key="sk" class="chip">{{ sk }}</span>
              <span v-if="!s.skills.length" class="muted">—</span>
            </td>
            <td class="mono">{{ formatQualifications(s.qualifications) }}</td>
            <td class="mono">{{ formatWindows(s.availability) }}</td>
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
          <label>Skills (comma separated)</label>
          <input v-model="form.skills" placeholder="pcr, elisa" />
        </div>
        <div class="field">
          <label>Qualifications (name:expiry, …)</label>
          <input v-model="form.qualifications" placeholder="gmp:2099-12-31, iso" />
        </div>
        <div class="field">
          <label>Availability (start-end, …)</label>
          <input v-model="form.availability" placeholder="0-40" />
        </div>
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
</style>
