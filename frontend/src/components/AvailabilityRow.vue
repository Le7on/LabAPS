<script setup>
import { ref } from 'vue'

// One resource's per-plan availability: a whole-plan toggle plus a list of
// unavailable date ranges (leave / breakdown). Emits changes to the parent,
// which persists them.
const props = defineProps({
  row: { type: Object, required: true }, // { id, code, name, available, unavailableDates }
})
const emit = defineEmits(['change'])

const from = ref('')
const to = ref('')

function toggleWholePlan() {
  emit('change', {
    available: !props.row.available,
    unavailableDates: props.row.unavailableDates,
  })
}

function addRange() {
  if (!from.value || !to.value || to.value < from.value) return
  emit('change', {
    available: props.row.available,
    unavailableDates: [...props.row.unavailableDates, [from.value, to.value]],
  })
  from.value = ''
  to.value = ''
}

function removeRange(i) {
  const next = props.row.unavailableDates.filter((_, idx) => idx !== i)
  emit('change', { available: props.row.available, unavailableDates: next })
}
</script>

<template>
  <div class="ar" :class="{ 'ar--off': !row.available }">
    <div class="ar__head">
      <label class="ar__toggle">
        <input type="checkbox" :checked="row.available" @change="toggleWholePlan" />
        <span class="ar__name">{{ row.code }} · {{ row.name }}</span>
      </label>
      <span v-if="!row.available" class="badge badge--danger">off all plan</span>
    </div>

    <template v-if="row.available">
      <div v-if="row.unavailableDates.length" class="ar__ranges">
        <span v-for="(r, i) in row.unavailableDates" :key="i" class="chip ar__range">
          {{ r[0] }} → {{ r[1] }}
          <button type="button" class="ar__x" @click="removeRange(i)">✕</button>
        </span>
      </div>
      <div class="ar__add">
        <input v-model="from" type="date" title="Unavailable from" />
        <span class="muted">→</span>
        <input v-model="to" type="date" title="Unavailable to" />
        <button type="button" class="btn btn--sm" @click="addRange">Add leave/downtime</button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.ar {
  padding: var(--s2) 0;
  border-bottom: 1px solid var(--line);
}
.ar:last-child {
  border-bottom: none;
}
.ar--off {
  opacity: 0.7;
}
.ar__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--s2);
}
.ar__toggle {
  display: flex;
  align-items: center;
  gap: var(--s2);
  cursor: pointer;
}
.ar__toggle input {
  width: auto;
}
.ar__name {
  font-family: var(--font-mono);
  font-size: 13px;
}
.ar__ranges {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin: 6px 0;
}
.ar__range {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
.ar__x {
  border: none;
  background: none;
  cursor: pointer;
  color: var(--led-danger);
  padding: 0;
  font-size: 11px;
}
.ar__add {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
}
.ar__add input {
  padding: 4px 6px;
}
</style>
