<script setup>
import { computed, ref } from 'vue'

// A month calendar. Days are available (green) by default; days in
// `unavailable` (Set of "YYYY-MM-DD") render red. Clicking a day emits toggle.
defineProps({
  unavailable: { type: Object, required: true }, // Set<string>
})
const emit = defineEmits(['toggle'])

const WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const cursor = ref(new Date())

const monthLabel = computed(() =>
  cursor.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
)

function iso(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

// Grid cells: leading blanks (Mon-based) + each day of the month.
const cells = computed(() => {
  const year = cursor.value.getFullYear()
  const month = cursor.value.getMonth()
  const first = new Date(year, month, 1)
  const lead = (first.getDay() + 6) % 7 // Mon=0
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const out = []
  for (let i = 0; i < lead; i++) out.push(null)
  for (let d = 1; d <= daysInMonth; d++) out.push(new Date(year, month, d))
  return out
})

function shift(delta) {
  cursor.value = new Date(cursor.value.getFullYear(), cursor.value.getMonth() + delta, 1)
}
</script>

<template>
  <div class="cal">
    <div class="cal__head">
      <button class="btn btn--sm btn--ghost" @click="shift(-1)">‹</button>
      <span class="cal__month">{{ monthLabel }}</span>
      <button class="btn btn--sm btn--ghost" @click="shift(1)">›</button>
    </div>
    <div class="cal__grid cal__weekdays">
      <span v-for="w in WEEKDAYS" :key="w" class="cal__wd">{{ w }}</span>
    </div>
    <div class="cal__grid">
      <template v-for="(d, i) in cells" :key="i">
        <span v-if="!d" class="cal__blank" />
        <button
          v-else
          class="cal__day"
          :class="unavailable.has(iso(d)) ? 'cal__day--off' : 'cal__day--on'"
          @click="emit('toggle', iso(d))"
        >
          {{ d.getDate() }}
        </button>
      </template>
    </div>
    <div class="cal__legend">
      <span class="dot dot--on"></span> Available <span class="dot dot--off"></span> Unavailable
    </div>
  </div>
</template>

<style scoped>
.cal {
  width: 320px;
}
.cal__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--s2);
}
.cal__month {
  font-weight: 600;
  font-size: 14px;
}
.cal__grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 3px;
}
.cal__weekdays {
  margin-bottom: 3px;
}
.cal__wd {
  text-align: center;
  font-size: 10px;
  color: var(--ink-3);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.cal__blank {
  aspect-ratio: 1;
}
.cal__day {
  aspect-ratio: 1;
  border: 1px solid var(--line);
  border-radius: var(--r-sm);
  cursor: pointer;
  font-size: 12px;
  font-family: var(--font-mono);
  transition:
    background 0.12s,
    border-color 0.12s;
}
.cal__day--on {
  background: var(--ok-soft);
  color: var(--led-ok);
  border-color: color-mix(in srgb, var(--led-ok) 25%, transparent);
}
.cal__day--on:hover {
  border-color: var(--led-ok);
}
.cal__day--off {
  background: var(--danger-soft);
  color: var(--led-danger);
  border-color: color-mix(in srgb, var(--led-danger) 30%, transparent);
}
.cal__day--off:hover {
  border-color: var(--led-danger);
}
.cal__legend {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: var(--s3);
  font-size: 11px;
  color: var(--ink-3);
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
  display: inline-block;
}
.dot--on {
  background: var(--ok-soft);
  border: 1px solid var(--led-ok);
}
.dot--off {
  background: var(--danger-soft);
  border: 1px solid var(--led-danger);
  margin-left: 8px;
}
</style>
