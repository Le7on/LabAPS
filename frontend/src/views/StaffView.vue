<script setup>
import { onMounted, reactive } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'

const store = useLaboratoryStore()

const form = reactive({ staffCode: '', name: '', skills: '' })

onMounted(() => {
  store.fetchStaff()
})

function parseList(value) {
  return value
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

async function submit() {
  const created = await store.addStaff({
    staffCode: form.staffCode,
    name: form.name,
    skills: parseList(form.skills),
  })
  if (created) {
    form.staffCode = ''
    form.name = ''
    form.skills = ''
  }
}
</script>

<template>
  <section>
    <h2>Staff</h2>

    <form class="row-form" @submit.prevent="submit">
      <input v-model="form.staffCode" placeholder="Staff code" required />
      <input v-model="form.name" placeholder="Name" required />
      <input v-model="form.skills" placeholder="Skills (comma separated)" />
      <button type="submit">Add staff</button>
    </form>

    <p v-if="store.error" class="error">{{ store.error }}</p>

    <table v-if="store.staff.length">
      <thead>
        <tr>
          <th>Code</th>
          <th>Name</th>
          <th>Skills</th>
          <th>Active</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in store.staff" :key="item.id">
          <td>{{ item.staffCode }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.skills.join(', ') }}</td>
          <td>{{ item.active ? 'yes' : 'no' }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>No staff yet.</p>
  </section>
</template>

<style scoped>
.row-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}
.error {
  color: #b00020;
}
table {
  border-collapse: collapse;
  width: 100%;
}
th,
td {
  border: 1px solid #ddd;
  padding: 0.4rem 0.6rem;
  text-align: left;
}
</style>
