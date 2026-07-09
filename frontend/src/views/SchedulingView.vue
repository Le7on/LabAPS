<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { listPlans } from '../api/plans'
import { listWorkflowDefinitions, listProjects } from '../api/laboratory'
import {
  addDemand,
  createVersion,
  generateInstances,
  listAssignments,
  publishVersion,
  reviewVersion,
  scheduleInstances,
} from '../api/plans'
import {
  cancelAssignment,
  completeAssignment,
  failAssignment,
  startAssignment,
} from '../api/executions'

const plans = ref([])
const workflows = ref([])
const projects = ref([])

const selected = reactive({ plan: '', workflow: '', project: '' })
const versionId = ref('')
const versionStatus = ref('')
const assignments = ref([])
const meta = ref({})
const demandForm = reactive({ quantity: 10, priority: 'normal' })
const frozenUntil = ref(0)
const error = ref(null)
const info = ref('')

onMounted(async () => {
  const [p, w, pr] = await Promise.all([listPlans(), listWorkflowDefinitions(), listProjects()])
  plans.value = p.data
  workflows.value = w.data
  projects.value = pr.data
})

const makespan = computed(() => meta.value.makespan)

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

async function createAndGenerate() {
  if (!selected.plan || !selected.workflow) {
    error.value = 'Select a plan and a workflow'
    return
  }
  const version = await run(() => createVersion(selected.plan))
  if (!version) return
  versionId.value = version.id
  versionStatus.value = version.status
  const ok = await run(
    () => generateInstances(selected.plan, version.id, selected.workflow),
    'Instances generated'
  )
  if (ok) assignments.value = []
}

async function addDemandRow() {
  if (!versionId.value || !selected.project) {
    error.value = 'Create a version and select a project first'
    return
  }
  await run(
    () =>
      addDemand(selected.plan, versionId.value, {
        projectId: selected.project,
        quantity: Number(demandForm.quantity) || 1,
        priority: demandForm.priority,
      }),
    'Demand added'
  )
}

async function schedule() {
  const result = await run(
    () => scheduleInstances(selected.plan, versionId.value, Number(frozenUntil.value) || 0),
    'Scheduled'
  )
  if (result) {
    meta.value = result.meta
    versionStatus.value = 'scheduled'
    await refresh()
  }
}

async function refresh() {
  const listing = await run(() => listAssignments(selected.plan, versionId.value))
  if (listing) assignments.value = listing.data
}

async function publish() {
  await run(() => reviewVersion(selected.plan, versionId.value))
  const pub = await run(() => publishVersion(selected.plan, versionId.value), 'Published')
  if (pub) {
    versionStatus.value = 'published'
    await refresh()
  }
}

async function act(fn, id, message, needsReason) {
  let reason
  if (needsReason) {
    reason = window.prompt(`${message} reason?`)
    if (!reason) return
  }
  await run(() => fn(id, reason), message)
  await refresh()
}

function badgeClass(status) {
  return {
    ready: 'badge--info',
    running: 'badge--warning',
    completed: 'badge--success',
    failed: 'badge--danger',
    cancelled: 'badge--danger',
  }[status]
}
</script>
<!-- template below -->
<template>
  <section class="stack">
    <h2>Scheduling</h2>
    <p v-if="info" class="success">{{ info }}</p>
    <p v-if="error" class="error">{{ error }}</p>

    <div class="card">
      <div class="card__title">1 · Plan &amp; workflow</div>
      <div class="form-row">
        <div class="field">
          <label>Plan</label>
          <select v-model="selected.plan">
            <option value="">Select plan…</option>
            <option v-for="p in plans" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>
        <div class="field">
          <label>Workflow</label>
          <select v-model="selected.workflow">
            <option value="">Select workflow…</option>
            <option v-for="w in workflows" :key="w.id" :value="w.id">{{ w.name }}</option>
          </select>
        </div>
        <button class="btn btn--primary" @click="createAndGenerate">
          Create version &amp; generate
        </button>
        <span v-if="versionId" class="badge badge--info">version: {{ versionStatus }}</span>
      </div>
    </div>

    <div v-if="versionId" class="card">
      <div class="card__title">2 · Demand (optional)</div>
      <div class="form-row">
        <div class="field">
          <label>Project</label>
          <select v-model="selected.project">
            <option value="">Select project…</option>
            <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>
        <div class="field">
          <label>Quantity</label>
          <input v-model.number="demandForm.quantity" type="number" min="1" />
        </div>
        <div class="field">
          <label>Priority</label>
          <select v-model="demandForm.priority">
            <option value="low">low</option>
            <option value="normal">normal</option>
            <option value="high">high</option>
          </select>
        </div>
        <button class="btn" @click="addDemandRow">Add demand</button>
      </div>
    </div>

    <div v-if="versionId" class="card">
      <div class="card__title">3 · Schedule</div>
      <div class="form-row">
        <div class="field">
          <label>Frozen until</label>
          <input v-model.number="frozenUntil" type="number" min="0" />
        </div>
        <button class="btn btn--primary" @click="schedule">Run scheduler</button>
        <button v-if="versionStatus === 'scheduled'" class="btn" @click="publish">
          Review &amp; publish
        </button>
        <span v-if="makespan != null" class="badge">makespan: {{ makespan }}</span>
      </div>
    </div>

    <div v-if="assignments.length" class="card">
      <div class="card__title">Assignments</div>
      <table class="table">
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
            <td>{{ a.operationId.slice(0, 8) }}</td>
            <td>{{ a.start }}</td>
            <td>{{ a.end }}</td>
            <td>{{ a.equipmentId ? a.equipmentId.slice(0, 8) : '—' }}</td>
            <td>{{ a.staffId ? a.staffId.slice(0, 8) : '—' }}</td>
            <td>
              <span class="badge" :class="badgeClass(a.status)">{{ a.status }}</span>
            </td>
            <td class="actions">
              <template v-if="a.status === 'ready'">
                <button class="btn btn--ghost" @click="act(startAssignment, a.id, 'Start')">
                  Start
                </button>
                <button class="btn btn--ghost" @click="act(cancelAssignment, a.id, 'Cancel', true)">
                  Cancel
                </button>
              </template>
              <template v-else-if="a.status === 'running'">
                <button class="btn btn--ghost" @click="act(completeAssignment, a.id, 'Complete')">
                  Complete
                </button>
                <button class="btn btn--ghost" @click="act(failAssignment, a.id, 'Fail', true)">
                  Fail
                </button>
              </template>
              <span v-else class="muted">—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.actions {
  display: flex;
  gap: 0.35rem;
}
</style>
