<script setup>
import { computed, onMounted, ref } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import { setUnavailableDates } from '../api/laboratory'
import PageHeader from '../components/PageHeader.vue'
import MonthCalendar from '../components/MonthCalendar.vue'

const store = useLaboratoryStore()
const kind = ref('staff') // 'staff' | 'equipment'
const selectedId = ref(null)
const error = ref(null)

// Local working set of unavailable dates for the selected resource.
const unavailable = ref(new Set())

onMounted(async () => {
  await Promise.all([store.fetchStaff(), store.fetchEquipment()])
  selectFirst()
})

const list = computed(() => (kind.value === 'staff' ? store.staff : store.equipment))
const selected = computed(() => list.value.find((r) => r.id === selectedId.value) || null)

function labelOf(r) {
  return kind.value === 'staff' ? `${r.staffCode} · ${r.name}` : `${r.equipmentCode} · ${r.name}`
}

function selectFirst() {
  selectedId.value = list.value[0]?.id ?? null
  loadDates()
}

function loadDates() {
  unavailable.value = new Set(selected.value?.unavailableDates ?? [])
}

function switchKind(k) {
  kind.value = k
  selectFirst()
}

function pick(id) {
  selectedId.value = id
  loadDates()
}

async function toggle(date) {
  const next = new Set(unavailable.value)
  if (next.has(date)) next.delete(date)
  else next.add(date)
  unavailable.value = next
  error.value = null
  try {
    const dates = [...next].sort()
    await setUnavailableDates(kind.value, selectedId.value, dates)
    // reflect into the store copy so re-selecting keeps state
    if (selected.value) selected.value.unavailableDates = dates
  } catch (e) {
    error.value = e?.message ?? 'Failed to save'
  }
}
</script>

<template>
  <section>
    <PageHeader
      title="Availability"
      subtitle="Staff leave and equipment maintenance — days off apply to all plans"
    >
      <template #actions>
        <div class="switch">
          <button
            class="btn btn--sm"
            :class="{ 'btn--primary': kind === 'staff' }"
            @click="switchKind('staff')"
          >
            Staff
          </button>
          <button
            class="btn btn--sm"
            :class="{ 'btn--primary': kind === 'equipment' }"
            @click="switchKind('equipment')"
          >
            Equipment
          </button>
        </div>
      </template>
    </PageHeader>

    <div class="layout">
      <div class="panel roster">
        <div class="panel__head">
          <span class="panel__title">{{ kind }}</span>
        </div>
        <div class="roster__list">
          <button
            v-for="r in list"
            :key="r.id"
            class="roster__item"
            :class="{ 'roster__item--active': r.id === selectedId }"
            @click="pick(r.id)"
          >
            <span class="mono">{{ labelOf(r) }}</span>
            <span v-if="(r.unavailableDates || []).length" class="badge badge--danger">
              {{ r.unavailableDates.length }} off
            </span>
          </button>
          <p v-if="!list.length" class="empty">None yet.</p>
        </div>
      </div>

      <div class="panel cal-panel">
        <div class="panel__head">
          <span class="panel__title">{{ selected ? labelOf(selected) : 'Select a resource' }}</span>
        </div>
        <div class="panel__body">
          <MonthCalendar v-if="selected" :unavailable="unavailable" @toggle="toggle" />
          <p v-else class="muted">Pick someone or something on the left.</p>
          <p v-if="error" class="error">{{ error }}</p>
          <p class="muted hint">
            Click a day to toggle it available / unavailable. Green = available, red = off.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.switch {
  display: flex;
  gap: 4px;
}
.layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: var(--s4);
  align-items: start;
}
.roster__list {
  display: flex;
  flex-direction: column;
  padding: var(--s2);
  gap: 2px;
}
.roster__item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--s2);
  padding: 7px 10px;
  border: 1px solid transparent;
  border-radius: var(--r-sm);
  background: none;
  cursor: pointer;
  font-size: 13px;
  text-align: left;
}
.roster__item:hover {
  background: var(--inset);
}
.roster__item--active {
  background: var(--accent-soft);
  border-color: color-mix(in srgb, var(--accent) 30%, transparent);
}
.hint {
  font-size: 12px;
  margin-top: var(--s3);
}
</style>
