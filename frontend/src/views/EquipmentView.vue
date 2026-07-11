<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import { parseList, parseWindows, formatWindows } from '../utils/parse'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'
import StatusLed from '../components/StatusLed.vue'

const store = useLaboratoryStore()
const open = ref(false)
const form = reactive({ equipmentCode: '', name: '', capabilities: '', availability: '' })

onMounted(() => store.fetchEquipment())

async function submit() {
  const ok = await store.addEquipment({
    equipmentCode: form.equipmentCode,
    name: form.name,
    capabilities: parseList(form.capabilities),
    availability: parseWindows(form.availability),
  })
  if (ok) {
    Object.assign(form, { equipmentCode: '', name: '', capabilities: '', availability: '' })
    open.value = false
  }
}
</script>

<template>
  <section>
    <PageHeader title="Equipment" subtitle="Machines, their capabilities and availability">
      <template #actions>
        <button class="btn btn--primary" @click="open = true">+ New equipment</button>
      </template>
    </PageHeader>

    <div class="panel">
      <table v-if="store.equipment.length" class="table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Capabilities</th>
            <th>Availability</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in store.equipment" :key="item.id">
            <td class="mono cell-strong">{{ item.equipmentCode }}</td>
            <td class="cell-strong">{{ item.name }}</td>
            <td>
              <span v-for="c in item.capabilities" :key="c" class="chip">{{ c }}</span>
              <span v-if="!item.capabilities.length" class="muted">—</span>
            </td>
            <td class="mono">{{ formatWindows(item.availability) }}</td>
            <td><StatusLed :status="item.active ? 'active' : 'inactive'" /></td>
            <td class="right">
              <button
                class="btn btn--sm btn--ghost"
                @click="store.setActive('equipment', item.id, !item.active)"
              >
                {{ item.active ? 'Deactivate' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No equipment yet.</p>
    </div>

    <SlideOver :open="open" title="New equipment" @close="open = false">
      <form class="stack" @submit.prevent="submit">
        <div class="field">
          <label>Code</label>
          <input v-model="form.equipmentCode" placeholder="EQ-001" required />
        </div>
        <div class="field">
          <label>Name</label>
          <input v-model="form.name" placeholder="Thermocycler" required />
        </div>
        <div class="field">
          <label>Capabilities (comma separated)</label>
          <input v-model="form.capabilities" placeholder="pcr, spin" />
        </div>
        <div class="field">
          <label>Availability (start-end, …)</label>
          <input v-model="form.availability" placeholder="0-40, 60-100" />
        </div>
        <p v-if="store.error" class="error">{{ store.error }}</p>
        <button class="btn btn--primary" type="submit">Add equipment</button>
      </form>
    </SlideOver>
  </section>
</template>

<style scoped>
.right {
  text-align: right;
}
</style>
