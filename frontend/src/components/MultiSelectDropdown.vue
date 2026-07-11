<script setup>
// A click-to-open dropdown whose items are checkboxes, supporting multi-select.
// options: [{ value, label }]; modelValue: array of selected values.
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  options: { type: Array, default: () => [] },
  placeholder: { type: String, default: 'Select…' },
})
const emit = defineEmits(['update:modelValue'])

const open = ref(false)
const root = ref(null)

const selected = computed(() => props.modelValue ?? [])

const summary = computed(() => {
  if (!selected.value.length) return props.placeholder
  const labels = props.options.filter((o) => selected.value.includes(o.value)).map((o) => o.label)
  return labels.length ? labels.join(', ') : `${selected.value.length} selected`
})

function toggle(value) {
  const next = selected.value.includes(value)
    ? selected.value.filter((v) => v !== value)
    : [...selected.value, value]
  emit('update:modelValue', next)
}

function isChecked(value) {
  return selected.value.includes(value)
}

function onClickOutside(e) {
  if (root.value && !root.value.contains(e.target)) open.value = false
}
onMounted(() => document.addEventListener('click', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <div ref="root" class="msd">
    <button type="button" class="msd__toggle" @click="open = !open">
      <span class="msd__summary" :class="{ 'msd__summary--empty': !selected.length }">
        {{ summary }}
      </span>
      <span class="msd__caret">▾</span>
    </button>
    <div v-if="open" class="msd__menu">
      <label v-for="o in options" :key="o.value" class="msd__item">
        <input type="checkbox" :checked="isChecked(o.value)" @change="toggle(o.value)" />
        <span>{{ o.label }}</span>
      </label>
      <p v-if="!options.length" class="msd__empty">No options.</p>
    </div>
  </div>
</template>

<style scoped>
.msd {
  position: relative;
}
.msd__toggle {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.45rem 0.6rem;
  border: 1px solid var(--color-border, #cbd5e1);
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  text-align: left;
}
.msd__summary {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.msd__summary--empty {
  color: var(--color-muted, #94a3b8);
}
.msd__caret {
  color: var(--color-muted, #94a3b8);
}
.msd__menu {
  position: absolute;
  z-index: 20;
  top: calc(100% + 2px);
  left: 0;
  right: 0;
  max-height: 220px;
  overflow-y: auto;
  background: #fff;
  border: 1px solid var(--color-border, #cbd5e1);
  border-radius: 6px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
  padding: 0.25rem;
}
.msd__item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
}
.msd__item:hover {
  background: #f1f5f9;
}
.msd__empty {
  padding: 0.5rem;
  color: var(--color-muted, #94a3b8);
  margin: 0;
}
</style>
