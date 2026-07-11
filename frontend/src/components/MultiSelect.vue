<script setup>
import { computed, ref } from 'vue'

// A checkbox dropdown for many-to-many selection. options: [{value,label}];
// modelValue: array of selected values. Closes on outside click.
const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  options: { type: Array, default: () => [] },
  placeholder: { type: String, default: 'Select…' },
})
const emit = defineEmits(['update:modelValue'])

const open = ref(false)
const root = ref(null)

const selectedLabels = computed(() =>
  props.options.filter((o) => props.modelValue.includes(o.value)).map((o) => o.label)
)

function toggle(value) {
  const next = props.modelValue.includes(value)
    ? props.modelValue.filter((v) => v !== value)
    : [...props.modelValue, value]
  emit('update:modelValue', next)
}

function onDocClick(e) {
  if (root.value && !root.value.contains(e.target)) open.value = false
}
function setOpen(v) {
  open.value = v
  if (v) document.addEventListener('click', onDocClick)
  else document.removeEventListener('click', onDocClick)
}
</script>

<template>
  <div ref="root" class="ms">
    <button type="button" class="ms__control" @click="setOpen(!open)">
      <span v-if="selectedLabels.length" class="ms__tags">
        <span v-for="l in selectedLabels" :key="l" class="chip">{{ l }}</span>
      </span>
      <span v-else class="ms__placeholder">{{ placeholder }}</span>
      <span class="ms__caret">▾</span>
    </button>
    <div v-if="open" class="ms__menu">
      <p v-if="!options.length" class="ms__empty">No options</p>
      <label v-for="o in options" :key="o.value" class="ms__option">
        <input type="checkbox" :checked="modelValue.includes(o.value)" @change="toggle(o.value)" />
        <span>{{ o.label }}</span>
      </label>
    </div>
  </div>
</template>

<style scoped>
.ms {
  position: relative;
}
.ms__control {
  width: 100%;
  min-height: 34px;
  display: flex;
  align-items: center;
  gap: var(--s2);
  background: var(--inset);
  border: 1px solid var(--line-2);
  border-radius: var(--r-sm);
  padding: 4px 8px;
  cursor: pointer;
  font-family: inherit;
  font-size: 13px;
  text-align: left;
}
.ms__control:hover {
  border-color: var(--line-strong);
}
.ms__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 3px;
  flex: 1;
}
.ms__placeholder {
  flex: 1;
  color: var(--ink-muted);
}
.ms__caret {
  color: var(--ink-3);
  font-size: 11px;
}
.ms__menu {
  position: absolute;
  z-index: 30;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  max-height: 220px;
  overflow-y: auto;
  background: var(--panel);
  border: 1px solid var(--line-2);
  border-radius: var(--r-md);
  box-shadow: var(--overlay-shadow);
  padding: 4px;
}
.ms__option {
  display: flex;
  align-items: center;
  gap: var(--s2);
  padding: 6px 8px;
  border-radius: var(--r-sm);
  cursor: pointer;
  font-size: 13px;
}
.ms__option:hover {
  background: var(--inset);
}
.ms__option input {
  width: auto;
  padding: 0;
}
.ms__empty {
  padding: 8px;
  color: var(--ink-3);
  font-size: 12px;
  margin: 0;
}
</style>
