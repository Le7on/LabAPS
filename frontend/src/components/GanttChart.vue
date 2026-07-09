<script setup>
import { computed } from 'vue'

// A lightweight, dependency-free Gantt chart. Renders assignments as bars on a
// shared time axis, grouped by resource (equipment, falling back to staff).
const props = defineProps({
  assignments: { type: Array, required: true },
})

const STATUS_COLORS = {
  pending: '#94a3b8',
  ready: '#2f6feb',
  running: '#b7791f',
  completed: '#0a7d28',
  failed: '#c0392b',
  cancelled: '#c0392b',
}

const horizon = computed(() => {
  const max = Math.max(1, ...props.assignments.map((a) => a.end))
  return max
})

function resourceKey(a) {
  return a.equipmentId || a.staffId || 'unassigned'
}

const rows = computed(() => {
  const groups = new Map()
  for (const a of props.assignments) {
    const key = resourceKey(a)
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key).push(a)
  }
  return [...groups.entries()].map(([key, items]) => ({
    key,
    label: key === 'unassigned' ? 'Unassigned' : key.slice(0, 8),
    items,
  }))
})

// Axis ticks: about 10 evenly spaced marks across the horizon.
const ticks = computed(() => {
  const step = Math.max(1, Math.ceil(horizon.value / 10))
  const out = []
  for (let t = 0; t <= horizon.value; t += step) out.push(t)
  return out
})

function barStyle(a) {
  const width = ((a.end - a.start) / horizon.value) * 100
  const left = (a.start / horizon.value) * 100
  return {
    left: `${left}%`,
    width: `${Math.max(width, 1)}%`,
    background: STATUS_COLORS[a.status] || '#2f6feb',
  }
}
</script>

<template>
  <div class="gantt">
    <div class="gantt__axis">
      <div class="gantt__rowlabel"></div>
      <div class="gantt__track">
        <span v-for="t in ticks" :key="t" class="tick" :style="{ left: `${(t / horizon) * 100}%` }">
          {{ t }}
        </span>
      </div>
    </div>
    <div v-for="row in rows" :key="row.key" class="gantt__row">
      <div class="gantt__rowlabel" :title="row.key">{{ row.label }}</div>
      <div class="gantt__track">
        <div
          v-for="a in row.items"
          :key="a.id"
          class="bar"
          :style="barStyle(a)"
          :title="`${a.operationId.slice(0, 8)} · ${a.start}–${a.end} · ${a.status}`"
        >
          {{ a.start }}–{{ a.end }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gantt {
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  overflow: hidden;
}
.gantt__axis,
.gantt__row {
  display: flex;
  align-items: stretch;
}
.gantt__axis {
  border-bottom: 1px solid var(--color-border);
  height: 1.5rem;
}
.gantt__row {
  border-bottom: 1px solid var(--color-border);
  min-height: 2rem;
}
.gantt__row:last-child {
  border-bottom: none;
}
.gantt__rowlabel {
  width: 90px;
  flex-shrink: 0;
  padding: 0.4rem 0.6rem;
  font-size: 0.8rem;
  color: var(--color-muted);
  border-right: 1px solid var(--color-border);
  background: #f9fafb;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.gantt__track {
  position: relative;
  flex: 1;
}
.tick {
  position: absolute;
  top: 0.2rem;
  font-size: 0.7rem;
  color: var(--color-muted);
  transform: translateX(-50%);
}
.bar {
  position: absolute;
  top: 0.35rem;
  height: 1.3rem;
  border-radius: 4px;
  color: #fff;
  font-size: 0.7rem;
  line-height: 1.3rem;
  text-align: center;
  overflow: hidden;
  white-space: nowrap;
}
</style>
