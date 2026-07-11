<script setup>
// Signature element: an instrument readout. Tracked-uppercase label demoted; the
// monospace figure leads via size + weight; optional note as quiet metadata.
defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  note: { type: String, default: '' },
  tone: { type: String, default: 'ink' }, // ink | ok | warn | danger | accent
})
</script>

<template>
  <div class="readout-cell">
    <div class="label">{{ label }}</div>
    <div class="readout-cell__value readout" :class="`tone-${tone}`">{{ value }}</div>
    <div v-if="note" class="readout-cell__note">{{ note }}</div>
  </div>
</template>

<style scoped>
.readout-cell {
  padding: var(--s4);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.readout-cell__value {
  font-size: 30px;
  line-height: 1;
  letter-spacing: -0.02em;
}
.readout-cell__note {
  font-size: 11.5px;
  color: var(--ink-3);
}
.tone-ok {
  color: var(--led-ok);
}
.tone-warn {
  color: var(--led-warn);
}
.tone-danger {
  color: var(--led-danger);
}
.tone-accent {
  color: var(--accent);
}
</style>
