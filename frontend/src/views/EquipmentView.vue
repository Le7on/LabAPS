<script setup>
import { onMounted, reactive } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import { parseList, parseWindows, formatWindows } from '../utils/parse'

const store = useLaboratoryStore()
const form = reactive({ equipmentCode: '', name: '', capabilities: '', availability: '' })

onMounted(() => store.fetchEquipment())

async function submit() {
  const ok = await store.addEquipment({
    equipmentCode: form.equipmentCode,
    name: form.name,
    capabilities: parseList(form.capabilities),
    availability: parseWindows(form.availability),
  })
  if (ok) {
    form.equipmentCode = ''
    form.name = ''
    form.capabilities = ''
    form.availability = ''
  }
}
</script>

<template>
  <section class="stack">
    <h2>Equipment</h2>

    <div class="card">
      <div class="card__title">New equipment</div>
      <form class="form-row" @submit.prevent="submit">
        <div class="field">
          <label>Code</label>
          <input v-model="form.equipmentCode" placeholder="EQ-001" required />
        </div>
        <div class="field">
          <label>Name</label>
          <input v-model="form.name" placeholder="Thermocycler" required />
        </div>
        <div class="field">
          <label>Capabilities</label>
          <input v-model="form.capabilities" placeholder="pcr, spin" />
        </div>
        <div class="field">
          <label>Availability (start-end, …)</label>
          <input v-model="form.availability" placeholder="0-40, 60-100" />
        </div>
        <button class="btn btn--primary" type="submit">Add equipment</button>
      </form>
      <p v-if="store.error" class="error">{{ store.error }}</p>
    </div>

    <div class="card">
      <table v-if="store.equipment.length" class="table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Capabilities</th>
            <th>Availability</th>
            <th>Active</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in store.equipment" :key="item.id">
            <td>{{ item.equipmentCode }}</td>
            <td>{{ item.name }}</td>
            <td>
              <span v-for="c in item.capabilities" :key="c" class="badge badge--info">{{ c }}</span>
              <span v-if="!item.capabilities.length" class="muted">—</span>
            </td>
            <td>{{ formatWindows(item.availability) }}</td>
            <td>
              <span class="badge" :class="item.active ? 'badge--success' : ''">
                {{ item.active ? 'active' : 'inactive' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No equipment yet.</p>
    </div>
  </section>
</template>

<style scoped>
.badge + .badge {
  margin-left: 0.25rem;
}
</style>
