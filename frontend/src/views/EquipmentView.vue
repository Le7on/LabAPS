<script setup>
import { onMounted, reactive } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'

const store = useLaboratoryStore()

const form = reactive({ equipmentCode: '', name: '', capabilities: '' })

onMounted(() => {
  store.fetchEquipment()
})

function parseList(value) {
  return value
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

async function submit() {
  const created = await store.addEquipment({
    equipmentCode: form.equipmentCode,
    name: form.name,
    capabilities: parseList(form.capabilities),
  })
  if (created) {
    form.equipmentCode = ''
    form.name = ''
    form.capabilities = ''
  }
}
</script>

<template>
  <section>
    <h2>Equipment</h2>

    <form class="row-form" @submit.prevent="submit">
      <input v-model="form.equipmentCode" placeholder="Equipment code" required />
      <input v-model="form.name" placeholder="Name" required />
      <input v-model="form.capabilities" placeholder="Capabilities (comma separated)" />
      <button type="submit">Add equipment</button>
    </form>

    <p v-if="store.error" class="error">{{ store.error }}</p>

    <table v-if="store.equipment.length">
      <thead>
        <tr>
          <th>Code</th>
          <th>Name</th>
          <th>Capabilities</th>
          <th>Active</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in store.equipment" :key="item.id">
          <td>{{ item.equipmentCode }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.capabilities.join(', ') }}</td>
          <td>{{ item.active ? 'yes' : 'no' }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>No equipment yet.</p>
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
