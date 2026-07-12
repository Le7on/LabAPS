<script setup>
import { computed } from 'vue'

// Calendar schedule grid: rows = equipment (machines), columns = days. Each cell
// lists what runs on that machine that day — method name and the operator —
// answering "on this day, who uses which machine for which methods".
const props = defineProps({
  assignments: { type: Array, required: true },
  // lookup maps: id -> display label
  equipmentLabels: { type: Object, default: () => ({}) },
  staffLabels: { type: Object, default: () => ({}) },
  methodLabels: { type: Object, default: () => ({}) },
})

const STATUS_TONE = {
  pending: 'idle',
  ready: 'info',
  running: 'warn',
  completed: 'ok',
  failed: 'danger',
  cancelled: 'danger',
}

// Day key "YYYY-MM-DD" from an assignment's startAt (calendar mode).
function dayOf(a) {
  return a.startAt ? a.startAt.slice(0, 10) : null
}

const hasCalendar = computed(() => props.assignments.some((a) => a.startAt))

const days = computed(() => {
  const set = new Set()
  for (const a of props.assignments) {
    const d = dayOf(a)
    if (d) set.add(d)
  }
  return [...set].sort()
})

const machines = computed(() => {
  const set = new Set()
  for (const a of props.assignments) set.add(a.equipmentId || 'unassigned')
  return [...set]
})

function methodName(a) {
  // Instance id is "<methodDefId>#r<run>"; strip the run suffix for the label.
  const defId = String(a.operationId).split('#')[0]
  return props.methodLabels[defId] || defId.slice(0, 8)
}

// assignments for a given machine + day.
function cell(machineId, day) {
  return props.assignments.filter(
    (a) => (a.equipmentId || 'unassigned') === machineId && dayOf(a) === day
  )
}

function label(map, id, fallback = '—') {
  if (!id) return fallback
  return map[id] || id.slice(0, 8)
}
</script>

<template>
  <div v-if="!hasCalendar" class="cg-empty muted">
    This plan has no calendar dates, so a day grid isn't available. Add start/end dates to the plan
    to see the schedule by day.
  </div>
  <div v-else class="cg-wrap">
    <table class="cg">
      <thead>
        <tr>
          <th class="cg__corner">Machine \ Day</th>
          <th v-for="d in days" :key="d" class="cg__day">{{ d.slice(5) }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="m in machines" :key="m">
          <th class="cg__machine">{{ label(equipmentLabels, m, 'Unassigned') }}</th>
          <td v-for="d in days" :key="d" class="cg__cell">
            <div
              v-for="a in cell(m, d)"
              :key="a.id"
              class="task"
              :class="`task--${STATUS_TONE[a.status] || 'idle'}`"
              :title="`${methodName(a)} · ${label(staffLabels, a.staffId)} · ${a.shift || ''} · ${a.status}`"
            >
              <span class="task__method">{{ methodName(a) }}</span>
              <span class="task__staff">{{ label(staffLabels, a.staffId) }}</span>
            </div>
            <span v-if="!cell(m, d).length" class="cg__idle">·</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.cg-wrap {
  overflow-x: auto;
}
.cg-empty {
  padding: var(--s4);
  font-size: 13px;
}
.cg {
  border-collapse: collapse;
  font-size: 12px;
  min-width: 100%;
}
.cg th,
.cg td {
  border: 1px solid var(--line);
  vertical-align: top;
}
.cg__corner,
.cg__machine {
  background: var(--panel-2);
  text-align: left;
  padding: 6px 10px;
  font-weight: 600;
  color: var(--ink-2);
  white-space: nowrap;
  position: sticky;
  left: 0;
}
.cg__day {
  padding: 6px 8px;
  color: var(--ink-3);
  font-family: var(--font-mono);
  font-weight: 600;
  white-space: nowrap;
}
.cg__cell {
  padding: 3px;
  min-width: 84px;
}
.cg__idle {
  color: var(--line-strong);
}
.task {
  border-radius: var(--r-sm);
  padding: 3px 6px;
  margin: 2px 0;
  display: flex;
  flex-direction: column;
  line-height: 1.25;
  border-left: 3px solid var(--led-idle);
  background: var(--inset);
}
.task--ok {
  border-left-color: var(--led-ok);
}
.task--warn {
  border-left-color: var(--led-warn);
}
.task--danger {
  border-left-color: var(--led-danger);
}
.task--info {
  border-left-color: var(--led-info);
}
.task__method {
  font-weight: 600;
  color: var(--ink);
}
.task__staff {
  color: var(--ink-3);
  font-size: 11px;
}
</style>
