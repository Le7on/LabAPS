<script setup>
import { onMounted, reactive } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import {
  parseList,
  parseWindows,
  parseQualifications,
  formatWindows,
  formatQualifications,
} from '../utils/parse'

const store = useLaboratoryStore()
const form = reactive({
  staffCode: '',
  name: '',
  skills: '',
  qualifications: '',
  availability: '',
})

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
    form.staffCode = ''
    form.name = ''
    form.skills = ''
    form.qualifications = ''
    form.availability = ''
  }
}
</script>

<template>
  <section class="stack">
    <h2>Staff</h2>

    <div class="card">
      <div class="card__title">New staff member</div>
      <form class="form-row" @submit.prevent="submit">
        <div class="field">
          <label>Code</label>
          <input v-model="form.staffCode" placeholder="ST-001" required />
        </div>
        <div class="field">
          <label>Name</label>
          <input v-model="form.name" placeholder="Alice" required />
        </div>
        <div class="field">
          <label>Skills</label>
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
        <button class="btn btn--primary" type="submit">Add staff</button>
      </form>
      <p v-if="store.error" class="error">{{ store.error }}</p>
    </div>

    <div class="card">
      <table v-if="store.staff.length" class="table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Skills</th>
            <th>Qualifications</th>
            <th>Availability</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in store.staff" :key="s.id">
            <td>{{ s.staffCode }}</td>
            <td>{{ s.name }}</td>
            <td>
              <span v-for="sk in s.skills" :key="sk" class="badge badge--info">{{ sk }}</span>
              <span v-if="!s.skills.length" class="muted">—</span>
            </td>
            <td>{{ formatQualifications(s.qualifications) }}</td>
            <td>{{ formatWindows(s.availability) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No staff yet.</p>
    </div>
  </section>
</template>

<style scoped>
.badge + .badge {
  margin-left: 0.25rem;
}
</style>
