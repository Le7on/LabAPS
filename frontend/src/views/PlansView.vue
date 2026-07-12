<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { usePlansStore } from '../stores/plans'
import { useLaboratoryStore } from '../stores/laboratory'
import { addDemandLine, removeDemandLine } from '../api/plans'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'
import StatusLed from '../components/StatusLed.vue'

const store = usePlansStore()
const lab = useLaboratoryStore()
const open = ref(false)

// Expanded plan (to edit its demand lines) + the inline add-line form.
const expanded = ref(null)
const lineForm = reactive({
  workflowDefinitionId: '',
  operationDefinitionId: '',
  rounds: 1,
  targetDate: '',
})
const lineError = ref(null)

const workflowOptions = computed(() =>
  lab.workflows.map((w) => ({ value: w.id, label: `${w.workflowCode} · ${w.name}` }))
)
const workflowName = (id) => lab.workflows.find((w) => w.id === id)?.name ?? id.slice(0, 8)

// Methods (SMDP/SAP/…) of the selected workflow, for the Method dropdown.
const methodOptions = computed(() => {
  const wf = lab.workflows.find((w) => w.id === lineForm.workflowDefinitionId)
  return wf ? wf.operations.map((op) => ({ value: op.id, label: op.operationType })) : []
})
function methodName(workflowId, methodId) {
  const wf = lab.workflows.find((w) => w.id === workflowId)
  return wf?.operations.find((op) => op.id === methodId)?.operationType ?? '—'
}

// Reset the method when the workflow changes.
function onWorkflowChange() {
  lineForm.operationDefinitionId = ''
}

function toggleExpand(plan) {
  expanded.value = expanded.value === plan.id ? null : plan.id
  lineError.value = null
  Object.assign(lineForm, {
    workflowDefinitionId: '',
    operationDefinitionId: '',
    rounds: 1,
    targetDate: plan.startDate,
  })
}

async function addLine(plan) {
  lineError.value = null
  try {
    await addDemandLine(plan.id, { ...lineForm })
    await store.fetchPlans()
    Object.assign(lineForm, {
      workflowDefinitionId: '',
      operationDefinitionId: '',
      rounds: 1,
      targetDate: plan.startDate,
    })
  } catch (e) {
    lineError.value = e?.message ?? 'Failed to add line'
  }
}

async function deleteLine(plan, lineId) {
  try {
    await removeDemandLine(plan.id, lineId)
    await store.fetchPlans()
  } catch (e) {
    lineError.value = e?.message ?? 'Failed to remove line'
  }
}
const form = reactive({
  name: '',
  description: '',
  startDate: '',
  endDate: '',
  shiftMode: 'single',
  skippedDates: [],
})
const holiday = ref('')

function addHoliday() {
  if (holiday.value && !form.skippedDates.includes(holiday.value)) {
    form.skippedDates.push(holiday.value)
    form.skippedDates.sort()
  }
  holiday.value = ''
}
function removeHoliday(d) {
  form.skippedDates = form.skippedDates.filter((x) => x !== d)
}

onMounted(() => {
  store.fetchPlans()
  lab.fetchWorkflows()
})

// ISO week label (e.g. "2026-W32") derived from a YYYY-MM-DD date.
function isoWeek(dateStr) {
  const d = new Date(dateStr + 'T00:00:00')
  const day = (d.getUTCDay() + 6) % 7 // Mon=0
  d.setUTCDate(d.getUTCDate() - day + 3) // nearest Thursday
  const firstThu = new Date(Date.UTC(d.getUTCFullYear(), 0, 4))
  const week = 1 + Math.round((d - firstThu) / 604800000)
  return `${d.getUTCFullYear()}-W${String(week).padStart(2, '0')}`
}

async function submit() {
  if (form.endDate < form.startDate) {
    store.error = 'End date must be on or after start date'
    return
  }
  const ok = await store.addPlan({
    name: form.name,
    description: form.description,
    startDate: form.startDate,
    endDate: form.endDate,
    shiftMode: form.shiftMode,
    skippedDates: [...form.skippedDates],
    planningHorizon: isoWeek(form.startDate),
  })
  if (ok) {
    Object.assign(form, {
      name: '',
      description: '',
      startDate: '',
      endDate: '',
      shiftMode: 'single',
      skippedDates: [],
    })
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
            <th></th>
            <th>Plan code</th>
            <th>Name</th>
            <th>Period</th>
            <th>Shifts</th>
            <th>Requests</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="plan in store.plans" :key="plan.id">
            <tr class="plan-row" @click="toggleExpand(plan)">
              <td class="expand">{{ expanded === plan.id ? '▾' : '▸' }}</td>
              <td class="mono cell-strong">{{ plan.planCode }}</td>
              <td class="cell-strong">{{ plan.name }}</td>
              <td class="mono">{{ plan.startDate }} → {{ plan.endDate }}</td>
              <td class="mono">{{ plan.shiftMode }}</td>
              <td class="mono">{{ (plan.demandLines || []).length }}</td>
              <td><StatusLed :status="plan.status" /></td>
            </tr>
            <tr v-if="expanded === plan.id" class="detail-row">
              <td colspan="7">
                <div class="detail">
                  <div class="label">PI requests — method × rounds on a target day</div>
                  <table class="lines">
                    <tbody>
                      <tr v-for="line in plan.demandLines" :key="line.id">
                        <td class="cell-strong">
                          {{ workflowName(line.workflowDefinitionId) }} ·
                          {{ methodName(line.workflowDefinitionId, line.operationDefinitionId) }}
                        </td>
                        <td class="mono">× {{ line.rounds }}</td>
                        <td class="mono">{{ line.targetDate }}</td>
                        <td class="right">
                          <button
                            class="btn btn--sm btn--ghost danger"
                            @click="deleteLine(plan, line.id)"
                          >
                            ✕
                          </button>
                        </td>
                      </tr>
                      <tr v-if="!plan.demandLines || !plan.demandLines.length">
                        <td colspan="4" class="muted">No requests yet.</td>
                      </tr>
                    </tbody>
                  </table>
                  <div class="add-line row">
                    <select v-model="lineForm.workflowDefinitionId" @change="onWorkflowChange">
                      <option value="">Workflow…</option>
                      <option v-for="w in workflowOptions" :key="w.value" :value="w.value">
                        {{ w.label }}
                      </option>
                    </select>
                    <select
                      v-model="lineForm.operationDefinitionId"
                      :disabled="!methodOptions.length"
                    >
                      <option value="">Method…</option>
                      <option v-for="m in methodOptions" :key="m.value" :value="m.value">
                        {{ m.label }}
                      </option>
                    </select>
                    <input
                      v-model.number="lineForm.rounds"
                      type="number"
                      min="1"
                      class="rounds"
                      title="Rounds"
                    />
                    <input
                      v-model="lineForm.targetDate"
                      type="date"
                      :min="plan.startDate"
                      :max="plan.endDate"
                      title="Target date"
                    />
                    <button class="btn btn--sm btn--primary" @click="addLine(plan)">
                      Add request
                    </button>
                  </div>
                  <p v-if="lineError" class="error">{{ lineError }}</p>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
      <p v-else class="empty">No plans yet.</p>
    </div>

    <SlideOver :open="open" title="New plan" @close="open = false">
      <form class="stack" @submit.prevent="submit">
        <div class="field">
          <label>Name</label>
          <input v-model="form.name" placeholder="Week 32 production" required />
        </div>
        <div class="row">
          <div class="field" style="flex: 1">
            <label>Start date</label>
            <input v-model="form.startDate" type="date" required />
          </div>
          <div class="field" style="flex: 1">
            <label>End date</label>
            <input v-model="form.endDate" type="date" required />
          </div>
        </div>
        <div class="field">
          <label>Shift mode</label>
          <select v-model="form.shiftMode">
            <option value="single">Single (1 shift/day)</option>
            <option value="double">Double (2 shifts/day)</option>
          </select>
        </div>
        <div class="field">
          <label>Holidays (no work these days)</label>
          <div class="row">
            <input v-model="holiday" type="date" />
            <button type="button" class="btn btn--sm" @click="addHoliday">Add</button>
          </div>
          <div v-if="form.skippedDates.length" class="holidays">
            <span v-for="d in form.skippedDates" :key="d" class="chip">
              {{ d }}
              <button type="button" class="hol__x" @click="removeHoliday(d)">✕</button>
            </span>
          </div>
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

<style scoped>
.holidays {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 6px;
}
.hol__x {
  border: none;
  background: none;
  cursor: pointer;
  color: var(--led-danger);
  padding: 0 0 0 4px;
  font-size: 11px;
}
.plan-row {
  cursor: pointer;
}
.expand {
  color: var(--ink-3);
  width: 24px;
  text-align: center;
}
.detail-row td {
  background: var(--panel-2);
  padding: var(--s3) var(--s4);
}
.detail {
  display: flex;
  flex-direction: column;
  gap: var(--s2);
}
.lines {
  width: auto;
  border-collapse: collapse;
}
.lines td {
  padding: 4px 12px 4px 0;
  border: none;
}
.add-line {
  align-items: center;
}
.add-line .rounds {
  width: 64px;
}
.right {
  text-align: right;
}
.danger {
  color: var(--led-danger);
}
</style>
