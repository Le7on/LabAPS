<script setup>
// Editor for availability windows. Windows are integer intervals in the
// scheduler's time units (see backend calendar constraint), not calendar
// dates — each window is [start, end] with end > start. Emits an array of
// [start, end] pairs via v-model.
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
})
const emit = defineEmits(['update:modelValue'])

const windows = computed(() => props.modelValue ?? [])

function update(next) {
  emit('update:modelValue', next)
}

function addWindow() {
  update([...windows.value, [0, 0]])
}

function removeWindow(index) {
  update(windows.value.filter((_, i) => i !== index))
}

function setBound(index, bound, value) {
  const n = Number(value)
  const next = windows.value.map((w, i) =>
    i === index ? (bound === 'start' ? [n, w[1]] : [w[0], n]) : w
  )
  update(next)
}
</script>

<template>
  <div class="windows">
    <div v-for="(w, i) in windows" :key="i" class="windows__row">
      <input
        type="number"
        class="windows__num"
        :value="w[0]"
        min="0"
        aria-label="Window start"
        @input="setBound(i, 'start', $event.target.value)"
      />
      <span class="windows__sep">–</span>
      <input
        type="number"
        class="windows__num"
        :value="w[1]"
        min="0"
        aria-label="Window end"
        @input="setBound(i, 'end', $event.target.value)"
      />
      <button type="button" class="btn btn--ghost" @click="removeWindow(i)">Remove</button>
    </div>
    <button type="button" class="btn btn--ghost" @click="addWindow">+ Add window</button>
    <p class="muted windows__hint">
      Availability windows in scheduler time units (hours). Leave empty for always available.
    </p>
  </div>
</template>

<style scoped>
.windows__row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.35rem;
}
.windows__num {
  width: 6rem;
}
.windows__sep {
  color: var(--muted, #888);
}
.windows__hint {
  margin-top: 0.25rem;
  font-size: 0.85em;
}
</style>
