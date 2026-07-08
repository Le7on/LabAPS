<script setup>
import { onMounted, ref } from 'vue'
import { getDashboard } from '../api/reports'

const summary = ref(null)
const error = ref(null)

const CARDS = [
  { key: 'plans', label: 'Plans' },
  { key: 'planVersions', label: 'Plan Versions' },
  { key: 'publishedVersions', label: 'Published Versions' },
  { key: 'equipment', label: 'Equipment' },
  { key: 'activeEquipment', label: 'Active Equipment' },
  { key: 'staff', label: 'Staff' },
  { key: 'workflowDefinitions', label: 'Workflow Definitions' },
]

onMounted(async () => {
  try {
    summary.value = await getDashboard()
  } catch (e) {
    error.value = e?.message ?? 'Failed to load dashboard'
  }
})
</script>

<template>
  <section>
    <h2>Dashboard</h2>

    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="summary" class="cards">
      <div v-for="card in CARDS" :key="card.key" class="card">
        <div class="value">{{ summary[card.key] }}</div>
        <div class="label">{{ card.label }}</div>
      </div>
    </div>

    <p v-else-if="!error">Loading…</p>
  </section>
</template>

<style scoped>
.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.card {
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 1rem 1.5rem;
  min-width: 8rem;
  text-align: center;
}
.value {
  font-size: 2rem;
  font-weight: 600;
}
.label {
  color: #555;
  margin-top: 0.25rem;
}
.error {
  color: #b00020;
}
</style>
