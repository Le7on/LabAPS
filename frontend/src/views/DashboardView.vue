<script setup>
import { onMounted, ref } from 'vue'
import { getDashboard } from '../api/reports'
import PageHeader from '../components/PageHeader.vue'
import StatReadout from '../components/StatReadout.vue'

const summary = ref(null)
const error = ref(null)

onMounted(async () => {
  try {
    summary.value = await getDashboard()
  } catch (e) {
    error.value = e?.message ?? 'Failed to load overview'
  }
})
</script>

<template>
  <section>
    <PageHeader title="Overview" subtitle="Current state across planning and the laboratory" />
    <p v-if="error" class="error">{{ error }}</p>

    <template v-if="summary">
      <!-- Focal readout strip: planning throughput leads. -->
      <div class="panel strip">
        <StatReadout label="Plans" :value="summary.plans" tone="accent" />
        <StatReadout label="Plan Versions" :value="summary.planVersions" />
        <StatReadout
          label="Published"
          :value="summary.publishedVersions"
          :tone="summary.publishedVersions ? 'ok' : 'ink'"
          note="live schedules"
        />
      </div>

      <!-- Supporting tier: laboratory capacity, demoted. -->
      <div class="panel resources">
        <div class="panel__head"><span class="panel__title">Laboratory capacity</span></div>
        <div class="resources__grid">
          <div class="resource">
            <span class="label">Equipment</span>
            <span class="readout resource__v"
              >{{ summary.activeEquipment
              }}<span class="resource__of">/ {{ summary.equipment }}</span></span
            >
            <span class="muted resource__c">active / total</span>
          </div>
          <div class="resource">
            <span class="label">Staff</span>
            <span class="readout resource__v">{{ summary.staff }}</span>
            <span class="muted resource__c">operators</span>
          </div>
          <div class="resource">
            <span class="label">Workflows</span>
            <span class="readout resource__v">{{ summary.workflowDefinitions }}</span>
            <span class="muted resource__c">definitions</span>
          </div>
        </div>
      </div>
    </template>
    <p v-else-if="!error" class="muted">Loading…</p>
  </section>
</template>

<style scoped>
.strip {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  margin-bottom: var(--s4);
}
.strip > * + * {
  border-left: 1px solid var(--line);
}
.resources__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
.resource {
  padding: var(--s4);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.resource + .resource {
  border-left: 1px solid var(--line);
}
.resource__v {
  font-size: 22px;
  letter-spacing: -0.01em;
}
.resource__of {
  color: var(--ink-3);
  font-size: 15px;
  margin-left: 3px;
}
.resource__c {
  font-size: 11.5px;
}
</style>
