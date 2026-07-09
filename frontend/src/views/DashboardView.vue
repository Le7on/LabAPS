<script setup>
import { onMounted, ref } from 'vue'
import { getDashboard } from '../api/reports'

const summary = ref(null)
const error = ref(null)

const CARDS = [
  { key: 'plans', label: 'Plans' },
  { key: 'planVersions', label: 'Plan Versions' },
  { key: 'publishedVersions', label: 'Published' },
  { key: 'equipment', label: 'Equipment' },
  { key: 'activeEquipment', label: 'Active Equipment' },
  { key: 'staff', label: 'Staff' },
  { key: 'workflowDefinitions', label: 'Workflows' },
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
  <section class="stack">
    <h2>Dashboard</h2>
    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="summary" class="grid">
      <div v-for="card in CARDS" :key="card.key" class="card metric">
        <div class="metric__value">{{ summary[card.key] }}</div>
        <div class="metric__label">{{ card.label }}</div>
      </div>
    </div>
    <p v-else-if="!error" class="muted">Loading…</p>
  </section>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}
.metric {
  text-align: center;
}
.metric__value {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--color-primary);
}
.metric__label {
  color: var(--color-muted);
  margin-top: 0.25rem;
  font-size: 0.85rem;
}
</style>
