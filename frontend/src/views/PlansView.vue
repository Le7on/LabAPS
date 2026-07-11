<script setup>
import { onMounted, reactive, ref } from 'vue'
import { usePlansStore } from '../stores/plans'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'
import StatusLed from '../components/StatusLed.vue'

const store = usePlansStore()
const open = ref(false)
const form = reactive({ planningHorizon: '', name: '', description: '' })

onMounted(() => store.fetchPlans())

async function submit() {
  const ok = await store.addPlan({ ...form })
  if (ok) {
    Object.assign(form, { planningHorizon: '', name: '', description: '' })
    open.value = false
  }
}
</script>

<template>
  <section>
    <PageHeader title="Plans" subtitle="Production plans by planning horizon">
      <template #actions>
        <button class="btn btn--primary" @click="open = true">+ New plan</button>
      </template>
    </PageHeader>

    <div class="panel">
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
            <td class="mono cell-strong">{{ plan.planCode }}</td>
            <td class="cell-strong">{{ plan.name }}</td>
            <td class="mono">{{ plan.planningHorizon }}</td>
            <td><StatusLed :status="plan.status" /></td>
            <td class="mono">{{ plan.versionCount }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No plans yet.</p>
    </div>

    <SlideOver :open="open" title="New plan" @close="open = false">
      <form class="stack" @submit.prevent="submit">
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
        <p v-if="store.error" class="error">{{ store.error }}</p>
        <button class="btn btn--primary" type="submit">Create plan</button>
      </form>
    </SlideOver>
  </section>
</template>
