<script setup>
import { onMounted, ref } from 'vue'
import { listPlans } from '../api/plans'
import { listWorkflowDefinitions } from '../api/laboratory'
import {
  createVersion,
  listAssignments,
  publishVersion,
  reviewVersion,
  scheduleFromWorkflow,
} from '../api/plans'
import { completeAssignment, startAssignment } from '../api/executions'

const plans = ref([])
const workflows = ref([])
const selectedPlan = ref('')
const selectedWorkflow = ref('')
const versionId = ref('')
const assignments = ref([])
const meta = ref({})
const error = ref(null)
const info = ref('')

onMounted(async () => {
  const [p, w] = await Promise.all([listPlans(), listWorkflowDefinitions()])
  plans.value = p.data
  workflows.value = w.data
})

async function run(fn, message) {
  error.value = null
  info.value = ''
  try {
    const result = await fn()
    if (message) info.value = message
    return result
  } catch (e) {
    error.value = e?.message ?? 'Request failed'
    return null
  }
}

async function schedule() {
  if (!selectedPlan.value || !selectedWorkflow.value) {
    error.value = 'Select a plan and a workflow'
    return
  }
  const version = await run(() => createVersion(selectedPlan.value))
  if (!version) return
  versionId.value = version.id

  const result = await run(
    () => scheduleFromWorkflow(selectedPlan.value, version.id, selectedWorkflow.value),
    'Scheduled'
  )
  if (result) await refreshAssignments()
}

async function refreshAssignments() {
  const listing = await run(() => listAssignments(selectedPlan.value, versionId.value))
  if (listing) {
    assignments.value = listing.data
    meta.value = listing.meta
  }
}

async function publish() {
  await run(() => reviewVersion(selectedPlan.value, versionId.value))
  await run(() => publishVersion(selectedPlan.value, versionId.value), 'Published')
  await refreshAssignments()
}

async function start(id) {
  await run(() => startAssignment(id), 'Started')
  await refreshAssignments()
}

async function complete(id) {
  await run(() => completeAssignment(id), 'Completed')
  await refreshAssignments()
}
</script>

<template>
  <section>
    <h2>Scheduling</h2>

    <div class="controls">
      <select v-model="selectedPlan">
        <option value="">Select plan…</option>
        <option v-for="p in plans" :key="p.id" :value="p.id">{{ p.name }}</option>
      </select>
      <select v-model="selectedWorkflow">
        <option value="">Select workflow…</option>
        <option v-for="w in workflows" :key="w.id" :value="w.id">{{ w.name }}</option>
      </select>
      <button @click="schedule">Create version &amp; schedule</button>
      <button v-if="versionId" @click="publish">Review &amp; publish</button>
    </div>

    <p v-if="info" class="info">{{ info }}</p>
    <p v-if="error" class="error">{{ error }}</p>

    <table v-if="assignments.length">
      <thead>
        <tr>
          <th>Operation</th>
          <th>Start</th>
          <th>End</th>
          <th>Equipment</th>
          <th>Staff</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in assignments" :key="a.id">
          <td>{{ a.operationId }}</td>
          <td>{{ a.start }}</td>
          <td>{{ a.end }}</td>
          <td>{{ a.equipmentId || '—' }}</td>
          <td>{{ a.staffId || '—' }}</td>
          <td>{{ a.status }}</td>
          <td>
            <button v-if="a.status === 'ready'" @click="start(a.id)">Start</button>
            <button v-else-if="a.status === 'running'" @click="complete(a.id)">Complete</button>
            <span v-else>—</span>
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<style scoped>
.controls {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}
.info {
  color: #0a7d28;
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
