<script setup>
import { onMounted, reactive } from 'vue'
import { usePlansStore } from '../stores/plans'

const store = usePlansStore()

const form = reactive({
  planningHorizon: '',
  name: '',
  description: '',
})

onMounted(() => {
  store.fetchPlans()
})

async function submit() {
  const created = await store.addPlan({ ...form })
  if (created) {
    form.planningHorizon = ''
    form.name = ''
    form.description = ''
  }
}
</script>

<template>
  <section class="plans">
    <h2>Plans</h2>

    <form class="plan-form" @submit.prevent="submit">
      <input
        v-model="form.planningHorizon"
        placeholder="Planning horizon (e.g. 2026-W32)"
        required
      />
      <input v-model="form.name" placeholder="Plan name" required />
      <input v-model="form.description" placeholder="Description" />
      <button type="submit">Create plan</button>
    </form>

    <p v-if="store.error" class="error">{{ store.error }}</p>
    <p v-if="store.loading">Loading…</p>

    <table v-if="store.plans.length">
      <thead>
        <tr>
          <th>Plan code</th>
          <th>Name</th>
          <th>Horizon</th>
          <th>Status</th>
          <th>Versions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="plan in store.plans" :key="plan.id">
          <td>{{ plan.planCode }}</td>
          <td>{{ plan.name }}</td>
          <td>{{ plan.planningHorizon }}</td>
          <td>{{ plan.status }}</td>
          <td>{{ plan.versionCount }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else-if="!store.loading">No plans yet.</p>
  </section>
</template>

<style scoped>
.plan-form {
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
