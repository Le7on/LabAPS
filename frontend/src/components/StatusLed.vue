<script setup>
import { computed } from 'vue'

// Instrument status LED: maps a domain status to a signal color + label.
const props = defineProps({
  status: { type: String, required: true },
})

// Map every status the app produces to one of four instrument signals.
const TONE = {
  // plan version
  working: 'idle',
  scheduled: 'info',
  reviewed: 'info',
  published: 'ok',
  archived: 'idle',
  // assignment execution
  pending: 'idle',
  ready: 'info',
  running: 'warn',
  completed: 'ok',
  failed: 'danger',
  cancelled: 'danger',
  // resource / feasibility
  active: 'ok',
  inactive: 'idle',
  feasible: 'ok',
  infeasible: 'danger',
  optimal: 'ok',
}

const tone = computed(() => TONE[props.status] ?? 'idle')
</script>

<template>
  <span class="led" :class="`led--${tone}`">{{ status }}</span>
</template>
