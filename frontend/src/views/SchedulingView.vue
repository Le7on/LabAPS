<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { listPlans } from '../api/plans'
import { listWorkflowDefinitions, listProjects } from '../api/laboratory'
import {
  addDemand,
  createVersion,
  generateInstances,
  getPlanAvailability,
  listAssignments,
  publishVersion,
  reviewVersion,
  scheduleInstances,
  setPlanAvailability,
} from '../api/plans'
import {
  cancelAssignment,
  completeAssignment,
  failAssignment,
  startAssignment,
} from '../api/executions'
import GanttChart from '../components/GanttChart.vue'
import PageHeader from '../components/PageHeader.vue'
import StatusLed from '../components/StatusLed.vue'
import AvailabilityRow from '../components/AvailabilityRow.vue'
import CalendarGantt from '../components/CalendarGantt.vue'

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

// Per-method run counts for the selected workflow: { methodId: count }.
const runCounts = reactive({})

const selectedWorkflow = computed(() => workflows.value.find((w) => w.id === selected.workflow))

function onWorkflowChange() {
  for (const k of Object.keys(runCounts)) delete runCounts[k]
  const wf = selectedWorkflow.value
  if (wf) for (const op of wf.operations) runCounts[op.id] = 1
}

// Per-plan availability, loaded when a plan is chosen.
const availability = reactive({ staff: [], equipment: [] })

async function onPlanChange() {
  availability.staff = []
  availability.equipment = []
  if (!selected.plan) return
  const data = await run(() => getPlanAvailability(selected.plan))
  if (data) {
    availability.staff = data.staff
    availability.equipment = data.equipment
  }
}

// change = { available, unavailableDates } from AvailabilityRow.
async function updateAvailability(kind, row, change) {
  const ok = await run(() =>
    setPlanAvailability(selected.plan, kind, row.id, change.available, change.unavailableDates)
  )
  if (ok) {
    row.available = change.available
    row.unavailableDates = change.unavailableDates
  }
}

onMounted(async () => {
  const [p, w, pr] = await Promise.all([listPlans(), listWorkflowDefinitions(), listProjects()])
  plans.value = p.data
  workflows.value = w.data
  projects.value = pr.data
})

const makespan = computed(() => meta.value.makespan)
const feasible = computed(() => meta.value.feasible)

// Label maps for the calendar grid (id -> human label).
const equipmentLabels = computed(() =>
  Object.fromEntries(availability.equipment.map((e) => [e.id, `${e.code} · ${e.name}`]))
)
const staffLabels = computed(() =>
  Object.fromEntries(availability.staff.map((s) => [s.id, `${s.code} · ${s.name}`]))
)
const methodLabels = computed(() => {
  const map = {}
  for (const wf of workflows.value) {
    for (const op of wf.operations) map[op.id] = op.operationType
  }
  return map
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

async function createAndGenerate() {
  if (!selected.plan || !selected.workflow) {
    error.value = 'Select a plan and a workflow'
    return
  }
  const version = await run(() => createVersion(selected.plan))
  if (!version) return
  versionId.value = version.id
  versionStatus.value = version.status
  meta.value = {}
  const ok = await run(
    () => generateInstances(selected.plan, version.id, selected.workflow, { ...runCounts }),
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

function formatAt(iso) {
  const [d, t] = iso.split('T')
  return `${d.slice(5)} ${t.slice(0, 5)}`
}
</script>

<template>
  <section>
    <PageHeader title="Scheduling" subtitle="Build a plan version, solve it, and drive execution">
      <template #actions>
        <span v-if="versionId" class="ctx">
          <span class="label">version</span>
          <StatusLed :status="versionStatus" />
        </span>
        <span v-if="makespan != null" class="ctx">
          <span class="label">makespan</span>
          <span class="readout ctx__v">{{ makespan }}</span>
        </span>
        <span v-if="feasible != null" class="ctx">
          <StatusLed :status="feasible ? 'feasible' : 'infeasible'" />
        </span>
      </template>
    </PageHeader>

    <p v-if="info" class="ok note">{{ info }}</p>
    <p v-if="error" class="error note">{{ error }}</p>

    <div class="console">
      <!-- Left: the build controls, stacked as a sequence. -->
      <div class="setup stack">
        <div class="panel">
          <div class="panel__head"><span class="panel__title">1 · Source</span></div>
          <div class="panel__body stack">
            <div class="field">
              <label>Plan</label>
              <select v-model="selected.plan" @change="onPlanChange">
                <option value="">Select plan…</option>
                <option v-for="p in plans" :key="p.id" :value="p.id">{{ p.name }}</option>
              </select>
            </div>
            <div class="field">
              <label>Workflow</label>
              <select v-model="selected.workflow" @change="onWorkflowChange">
                <option value="">Select workflow…</option>
                <option v-for="w in workflows" :key="w.id" :value="w.id">{{ w.name }}</option>
              </select>
            </div>
            <div v-if="selectedWorkflow" class="field">
              <label>Runs per method</label>
              <div class="runs">
                <div v-for="op in selectedWorkflow.operations" :key="op.id" class="runs__row">
                  <span class="runs__name">{{ op.operationType }}</span>
                  <span class="muted runs__hrs mono">{{ op.duration }}h</span>
                  <input v-model.number="runCounts[op.id]" type="number" min="1" class="runs__n" />
                </div>
              </div>
            </div>
            <button class="btn btn--primary" @click="createAndGenerate">
              Create version &amp; generate
            </button>
          </div>
        </div>

        <div v-if="selected.plan" class="panel">
          <div class="panel__head">
            <span class="panel__title">Availability</span>
            <span class="muted opt">for this plan</span>
          </div>
          <div class="panel__body stack">
            <p class="muted avail__hint">
              Uncheck to exclude for the whole plan, or add leave / breakdown date ranges. Set
              before generating.
            </p>
            <div v-if="availability.staff.length" class="avail">
              <div class="label">Staff</div>
              <AvailabilityRow
                v-for="s in availability.staff"
                :key="s.id"
                :row="s"
                @change="(c) => updateAvailability('staff', s, c)"
              />
            </div>
            <div v-if="availability.equipment.length" class="avail">
              <div class="label">Equipment</div>
              <AvailabilityRow
                v-for="e in availability.equipment"
                :key="e.id"
                :row="e"
                @change="(c) => updateAvailability('equipment', e, c)"
              />
            </div>
          </div>
        </div>

        <div class="panel" :class="{ 'is-disabled': !versionId }">
          <div class="panel__head">
            <span class="panel__title">2 · Demand</span><span class="muted opt">optional</span>
          </div>
          <div class="panel__body stack">
            <div class="field">
              <label>Project</label>
              <select v-model="selected.project" :disabled="!versionId">
                <option value="">Select project…</option>
                <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.name }}</option>
              </select>
            </div>
            <div class="row">
              <div class="field" style="flex: 1">
                <label>Qty</label>
                <input
                  v-model.number="demandForm.quantity"
                  type="number"
                  min="1"
                  :disabled="!versionId"
                />
              </div>
              <div class="field" style="flex: 1">
                <label>Priority</label>
                <select v-model="demandForm.priority" :disabled="!versionId">
                  <option value="low">low</option>
                  <option value="normal">normal</option>
                  <option value="high">high</option>
                </select>
              </div>
            </div>
            <button class="btn" :disabled="!versionId" @click="addDemandRow">Add demand</button>
          </div>
        </div>

        <div class="panel" :class="{ 'is-disabled': !versionId }">
          <div class="panel__head"><span class="panel__title">3 · Solve</span></div>
          <div class="panel__body stack">
            <div class="field">
              <label>Frozen until</label>
              <input v-model.number="frozenUntil" type="number" min="0" :disabled="!versionId" />
            </div>
            <button class="btn btn--primary" :disabled="!versionId" @click="schedule">
              Run scheduler
            </button>
            <button v-if="versionStatus === 'scheduled'" class="btn" @click="publish">
              Review &amp; publish
            </button>
          </div>
        </div>
      </div>

      <!-- Right: the result — timeline hero, then detail. -->
      <div class="result stack">
        <div v-if="assignments.length" class="panel">
          <div class="panel__head">
            <span class="panel__title">Schedule by day</span>
          </div>
          <div class="panel__body">
            <CalendarGantt
              :assignments="assignments"
              :equipment-labels="equipmentLabels"
              :staff-labels="staffLabels"
              :method-labels="methodLabels"
            />
          </div>
        </div>

        <div v-if="assignments.length" class="panel">
          <div class="panel__head"><span class="panel__title">Resource timeline</span></div>
          <div class="panel__body">
            <GanttChart :assignments="assignments" />
          </div>
        </div>

        <div v-if="assignments.length" class="panel">
          <div class="panel__head"><span class="panel__title">Assignments</span></div>
          <table class="table">
            <thead>
              <tr>
                <th>Operation</th>
                <th>Start</th>
                <th>End</th>
                <th>Equipment</th>
                <th>Staff</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in assignments" :key="a.id">
                <td class="mono">{{ a.operationId.slice(0, 8) }}</td>
                <td class="mono">
                  <template v-if="a.startAt">{{ formatAt(a.startAt) }}</template>
                  <template v-else>{{ a.start }}</template>
                  <span v-if="a.shift" class="chip">{{ a.shift }}</span>
                </td>
                <td class="mono">{{ a.endAt ? formatAt(a.endAt) : a.end }}</td>
                <td class="mono">{{ a.equipmentId ? a.equipmentId.slice(0, 8) : '—' }}</td>
                <td class="mono">{{ a.staffId ? a.staffId.slice(0, 8) : '—' }}</td>
                <td><StatusLed :status="a.status" /></td>
                <td class="actions">
                  <template v-if="a.status === 'ready'">
                    <button class="btn btn--sm" @click="act(startAssignment, a.id, 'Start')">
                      Start
                    </button>
                    <button
                      class="btn btn--sm btn--ghost"
                      @click="act(cancelAssignment, a.id, 'Cancel', true)"
                    >
                      Cancel
                    </button>
                  </template>
                  <template v-else-if="a.status === 'running'">
                    <button class="btn btn--sm" @click="act(completeAssignment, a.id, 'Complete')">
                      Complete
                    </button>
                    <button
                      class="btn btn--sm btn--ghost"
                      @click="act(failAssignment, a.id, 'Fail', true)"
                    >
                      Fail
                    </button>
                  </template>
                  <span v-else class="muted">—</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="panel placeholder">
          <div class="placeholder__inner">
            <div class="placeholder__mark">◷</div>
            <p class="muted">
              Create a version and run the scheduler to see the resource timeline.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.avail {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.avail + .avail {
  margin-top: var(--s2);
}
.avail__hint {
  font-size: 12px;
  margin: 0;
}
.avail__row {
  display: flex;
  align-items: center;
  gap: var(--s2);
  font-size: 13px;
  cursor: pointer;
}
.avail__row input {
  width: auto;
}
.avail__name {
  font-family: var(--font-mono);
}
.runs {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.runs__row {
  display: flex;
  align-items: center;
  gap: var(--s2);
}
.runs__name {
  flex: 1;
  font-size: 13px;
}
.runs__hrs {
  font-size: 11px;
}
.runs__n {
  width: 56px;
}
.ctx {
  display: inline-flex;
  align-items: center;
  gap: var(--s2);
  padding: 5px 10px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--panel);
}
.ctx__v {
  font-size: 14px;
}
.note {
  margin: 0 0 var(--s4);
  font-size: 13px;
}
.console {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: var(--s4);
  align-items: start;
}
.setup {
  gap: var(--s3);
}
.is-disabled {
  opacity: 0.6;
}
.opt {
  font-size: 11px;
  margin-left: auto;
}
.actions {
  display: flex;
  gap: 5px;
  justify-content: flex-end;
}
.placeholder {
  min-height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.placeholder__inner {
  text-align: center;
  max-width: 260px;
}
.placeholder__mark {
  font-size: 2rem;
  color: var(--line-strong);
  margin-bottom: var(--s2);
}
@media (max-width: 900px) {
  .console {
    grid-template-columns: 1fr;
  }
}
</style>
