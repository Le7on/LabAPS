<script setup>
import { onMounted, reactive } from 'vue'
import { usePlansStore } from '../stores/plans'

const store = usePlansStore()
const form = reactive({ planningHorizon: '', name: '', description: '' })

onMounted(() => store.fetchPlans())

async function submit() {
  const ok = await store.addPlan({ ...form })
  if (ok) {
    form.planningHorizon = ''
    form.name = ''
    form.description = ''
  }
}
</script>

<template>
  <section class="stack">
    <h2>Plans</h2>

    <div class="card">
      <div class="card__title">New plan</div>
      <form class="form-row" @submit.prevent="submit">
        <div class="field">
          <label>Planning horizon</label>
          <input v-model="form.planningHorizon" placeholder="2026-W32" required />
        </div>
        <div class="field">
          <label>Name</label>
          <input v-model="form.name" placeholder="Week 32 plan" required />
        </div>
        <div class="field">
          <label>Description</label>
          <input v-model="form.description" placeholder="Routine production" />
        </div>
        <button class="btn btn--primary" type="submit">Create plan</button>
      </form>
      <p v-if="store.error" class="error">{{ store.error }}</p>
    </div>

    <div class="card">
      <table v-if="store.plans.length" class="table">
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
            <td>
              <span class="badge">{{ plan.status }}</span>
            </td>
            <td>{{ plan.versionCount }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No plans yet.</p>
    </div>
  </section>
</template>
