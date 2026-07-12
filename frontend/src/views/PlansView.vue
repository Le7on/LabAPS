<script setup>
import { onMounted, reactive, ref } from 'vue'
import { usePlansStore } from '../stores/plans'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'
import StatusLed from '../components/StatusLed.vue'

const store = usePlansStore()
const open = ref(false)
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

onMounted(() => store.fetchPlans())

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
            <th>Plan code</th>
            <th>Name</th>
            <th>Period</th>
            <th>Shifts</th>
            <th>Status</th>
            <th>Versions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="plan in store.plans" :key="plan.id">
            <td class="mono cell-strong">{{ plan.planCode }}</td>
            <td class="cell-strong">{{ plan.name }}</td>
            <td class="mono">
              <template v-if="plan.startDate">{{ plan.startDate }} → {{ plan.endDate }}</template>
              <template v-else>{{ plan.planningHorizon }}</template>
            </td>
            <td class="mono">{{ plan.shiftMode }}</td>
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
</style>
