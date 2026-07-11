<script setup>
import { computed } from 'vue'

// Instrument occupancy chart: assignments as bars on a shared time axis, one
// lane per resource. Reads like an equipment utilization strip, not a generic
// bar chart. Dependency-free.
const props = defineProps({
  assignments: { type: Array, required: true },
})

const STATUS = {
  pending: 'var(--led-idle)',
  ready: 'var(--led-info)',
  running: 'var(--led-warn)',
  completed: 'var(--led-ok)',
  failed: 'var(--led-danger)',
  cancelled: 'var(--led-danger)',
}

const horizon = computed(() => Math.max(1, ...props.assignments.map((a) => a.end)))

const rows = computed(() => {
  const groups = new Map()
  for (const a of props.assignments) {
    const key = a.equipmentId || a.staffId || 'unassigned'
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key).push(a)
  }
  return [...groups.entries()].map(([key, items]) => ({
    key,
    label: key === 'unassigned' ? 'Unassigned' : key.slice(0, 8),
    items,
  }))
})

const ticks = computed(() => {
  const step = Math.max(1, Math.ceil(horizon.value / 8))
  const out = []
  for (let t = 0; t <= horizon.value; t += step) out.push(t)
  return out
})

function barStyle(a) {
  return {
    left: `${(a.start / horizon.value) * 100}%`,
    width: `${Math.max(((a.end - a.start) / horizon.value) * 100, 1.5)}%`,
    background: STATUS[a.status] || 'var(--led-info)',
  }
}
</script>

<template>
  <div class="gantt">
    <div class="gantt__axis">
      <div class="gantt__lane-label label">Resource</div>
      <div class="gantt__track gantt__track--axis">
        <span
          v-for="t in ticks"
          :key="t"
          class="tick mono"
          :style="{ left: `${(t / horizon) * 100}%` }"
          >{{ t }}</span
        >
      </div>
    </div>
    <div v-for="row in rows" :key="row.key" class="gantt__row">
      <div class="gantt__lane-label mono" :title="row.key">{{ row.label }}</div>
      <div class="gantt__track">
        <div
          v-for="a in row.items"
          :key="a.id"
          class="bar"
          :style="barStyle(a)"
          :title="`${a.operationId.slice(0, 8)} · ${a.start}–${a.end} · ${a.status}`"
        >
          <span class="bar__t mono">{{ a.start }}–{{ a.end }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gantt {
  --lane-w: 96px;
}
.gantt__axis,
.gantt__row {
  display: flex;
  align-items: stretch;
}
.gantt__axis {
  height: 22px;
  border-bottom: 1px solid var(--line-2);
}
.gantt__row {
  min-height: 30px;
  border-bottom: 1px solid var(--line);
}
.gantt__row:last-child {
  border-bottom: none;
}
.gantt__lane-label {
  width: var(--lane-w);
  flex-shrink: 0;
  padding: 7px var(--s3);
  font-size: 12px;
  color: var(--ink-2);
  border-right: 1px solid var(--line);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  align-self: center;
}
.gantt__track {
  position: relative;
  flex: 1;
  background-image: repeating-linear-gradient(
    to right,
    transparent,
    transparent calc(12.5% - 1px),
    var(--line) calc(12.5% - 1px),
    var(--line) 12.5%
  );
}
.gantt__track--axis {
  background: none;
}
.tick {
  position: absolute;
  top: 5px;
  font-size: 10px;
  color: var(--ink-3);
  transform: translateX(-50%);
}
.bar {
  position: absolute;
  top: 5px;
  height: 20px;
  border-radius: var(--r-sm);
  display: flex;
  align-items: center;
  padding: 0 5px;
  overflow: hidden;
}
.bar__t {
  font-size: 10.5px;
  color: #fff;
  white-space: nowrap;
}
</style>
