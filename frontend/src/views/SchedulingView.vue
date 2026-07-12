<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { listPlans, schedulePlans } from '../api/plans'
import { useLaboratoryStore } from '../stores/laboratory'
import PageHeader from '../components/PageHeader.vue'
import StatusLed from '../components/StatusLed.vue'
import CalendarGantt from '../components/CalendarGantt.vue'

const lab = useLaboratoryStore()
const plans = ref([])
const selected = reactive({}) // planId -> bool
const shiftMode = ref('single')
const result = ref(null)
const meta = ref({})
const error = ref(null)
const running = ref(false)

onMounted(async () => {
  const [p] = await Promise.all([
    listPlans(),
    lab.fetchStaff(),
    lab.fetchEquipment(),
    lab.fetchWorkflows(),
    lab.fetchProjects(),
  ])
  plans.value = p.data
  for (const plan of plans.value) selected[plan.id] = false
})

const chosenIds = computed(() => plans.value.filter((p) => selected[p.id]).map((p) => p.id))
const totalRequests = computed(() =>
  plans.value.filter((p) => selected[p.id]).reduce((n, p) => n + (p.demandLines || []).length, 0)
)

const assignments = computed(() => result.value?.assignments ?? [])
const feasible = computed(() => meta.value.feasible)

const equipmentLabels = computed(() =>
  Object.fromEntries(lab.equipment.map((e) => [e.id, `${e.equipmentCode} · ${e.name}`]))
)
const staffLabels = computed(() =>
  Object.fromEntries(lab.staff.map((s) => [s.id, `${s.staffCode} · ${s.name}`]))
)
const methodLabels = computed(() => {
  const map = {}
  for (const wf of lab.workflows) for (const op of wf.operations) map[op.id] = op.operationType
  return map
})

async function run() {
  error.value = null
  result.value = null
  meta.value = {}
  if (!chosenIds.value.length) {
    error.value = 'Select at least one plan'
    return
  }
  running.value = true
  try {
    const r = await schedulePlans(chosenIds.value, shiftMode.value)
    result.value = r.data
    meta.value = r.meta
  } catch (e) {
    error.value = e?.message ?? 'Scheduling failed'
  } finally {
    running.value = false
  }
}
</script>

<template>
  <section>
    <PageHeader
      title="Scheduling"
      subtitle="Select plans and schedule them together on one calendar"
    >
      <template #actions>
        <span v-if="feasible != null" class="ctx">
          <StatusLed :status="feasible ? 'feasible' : 'infeasible'" />
        </span>
      </template>
    </PageHeader>

    <p v-if="error" class="error note">{{ error }}</p>

    <div class="console">
      <div class="setup stack">
        <div class="panel">
          <div class="panel__head"><span class="panel__title">1 · Select plans</span></div>
          <div class="panel__body">
            <label v-for="p in plans" :key="p.id" class="plan-pick">
              <input type="checkbox" v-model="selected[p.id]" />
              <span class="plan-pick__body">
                <span class="cell-strong">{{ p.name }}</span>
                <span class="muted mono plan-pick__meta">
                  {{ p.startDate }} → {{ p.endDate }} · {{ (p.demandLines || []).length }} req
                </span>
              </span>
            </label>
            <p v-if="!plans.length" class="empty">No plans. Create one with PI requests first.</p>
          </div>
        </div>

        <div class="panel">
          <div class="panel__head"><span class="panel__title">2 · Run</span></div>
          <div class="panel__body stack">
            <div class="field">
              <label>Shift mode</label>
              <select v-model="shiftMode">
                <option value="single">Single (1 shift/day)</option>
                <option value="double">Double (2 shifts/day)</option>
              </select>
            </div>
            <div class="muted mono">
              {{ chosenIds.length }} plans · {{ totalRequests }} requests
            </div>
            <button class="btn btn--primary" :disabled="running || !chosenIds.length" @click="run">
              {{ running ? 'Scheduling…' : 'Run scheduler' }}
            </button>
          </div>
        </div>
      </div>

      <div class="result stack">
        <div v-if="assignments.length" class="panel">
          <div class="panel__head">
            <span class="panel__title">Schedule by day</span>
            <span class="muted opt">{{ result.startDate }} → {{ result.endDate }}</span>
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

        <div v-else-if="feasible === false" class="panel placeholder">
          <div class="placeholder__inner">
            <div class="placeholder__mark">⚠</div>
            <p class="muted">
              Infeasible — a target day lacks capacity (a required machine or qualified operator is
              unavailable, or too many rounds for the day's shifts). Adjust requests, availability,
              or shift mode and re-run.
            </p>
          </div>
        </div>

        <div v-else class="panel placeholder">
          <div class="placeholder__inner">
            <div class="placeholder__mark">◷</div>
            <p class="muted">Select plans and run the scheduler to see the schedule by day.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.ctx {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--panel);
}
.note {
  margin: 0 0 var(--s4);
  font-size: 13px;
}
.console {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: var(--s4);
  align-items: start;
}
.setup {
  gap: var(--s3);
}
.plan-pick {
  display: flex;
  align-items: flex-start;
  gap: var(--s2);
  padding: 7px 4px;
  border-bottom: 1px solid var(--line);
  cursor: pointer;
}
.plan-pick:last-child {
  border-bottom: none;
}
.plan-pick input {
  width: auto;
  margin-top: 2px;
}
.plan-pick__body {
  display: flex;
  flex-direction: column;
}
.plan-pick__meta {
  font-size: 11px;
}
.opt {
  margin-left: auto;
  font-size: 11px;
}
.placeholder {
  min-height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.placeholder__inner {
  text-align: center;
  max-width: 320px;
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
