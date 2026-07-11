<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'
import StatusLed from '../components/StatusLed.vue'
import MultiSelect from '../components/MultiSelect.vue'

const store = useLaboratoryStore()
const open = ref(false)
const editingId = ref(null)
const form = reactive({ equipmentCode: '', name: '', methodIds: [] })

onMounted(() => {
  store.fetchEquipment()
  store.fetchWorkflows()
})

const methodOptions = computed(() => {
  const out = []
  for (const wf of store.workflows) {
    for (const op of wf.operations) {
      out.push({ value: op.id, label: `${wf.name} · ${op.operationType}` })
    }
  }
  return out
})
const methodLabel = (id) => methodOptions.value.find((m) => m.value === id)?.label ?? id.slice(0, 6)

function openCreate() {
  editingId.value = null
  Object.assign(form, { equipmentCode: '', name: '', methodIds: [] })
  open.value = true
}
function openEdit(e) {
  editingId.value = e.id
  Object.assign(form, {
    equipmentCode: e.equipmentCode,
    name: e.name,
    methodIds: [...e.methodIds],
  })
  open.value = true
}

async function submit() {
  const payload = {
    equipmentCode: form.equipmentCode,
    name: form.name,
    methodIds: [...form.methodIds],
  }
  const ok = editingId.value
    ? await store.editEquipment(editingId.value, payload)
    : await store.addEquipment(payload)
  if (ok) open.value = false
}

async function remove(e) {
  if (window.confirm(`Delete equipment ${e.equipmentCode}?`)) await store.removeEquipment(e.id)
}
</script>

<template>
  <section>
    <PageHeader title="Equipment" subtitle="Machines and the methods that can run on them">
      <template #actions>
        <button class="btn btn--primary" @click="openCreate">+ New equipment</button>
      </template>
    </PageHeader>

    <div class="panel">
      <table v-if="store.equipment.length" class="table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Runs methods</th>
            <th>Status</th>
            <th class="right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in store.equipment" :key="item.id">
            <td class="mono cell-strong">{{ item.equipmentCode }}</td>
            <td class="cell-strong">{{ item.name }}</td>
            <td>
              <span v-for="mid in item.methodIds" :key="mid" class="chip">{{
                methodLabel(mid)
              }}</span>
              <span v-if="!item.methodIds.length" class="muted">—</span>
            </td>
            <td><StatusLed :status="item.active ? 'active' : 'inactive'" /></td>
            <td class="right actions">
              <button class="btn btn--sm btn--ghost" @click="openEdit(item)">Edit</button>
              <button
                class="btn btn--sm btn--ghost"
                @click="store.setActive('equipment', item.id, !item.active)"
              >
                {{ item.active ? 'Deactivate' : 'Activate' }}
              </button>
              <button class="btn btn--sm btn--ghost danger" @click="remove(item)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No equipment yet.</p>
      <p v-if="store.error" class="error err">{{ store.error }}</p>
    </div>

    <SlideOver
      :open="open"
      :title="editingId ? 'Edit equipment' : 'New equipment'"
      @close="open = false"
    >
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
          <label>Methods it can run</label>
          <MultiSelect
            v-model="form.methodIds"
            :options="methodOptions"
            placeholder="Select methods this machine supports…"
          />
        </div>
        <p v-if="!methodOptions.length" class="muted hint">
          Define workflows with methods first, then bind them here.
        </p>
        <p v-if="store.error" class="error">{{ store.error }}</p>
        <button class="btn btn--primary" type="submit">
          {{ editingId ? 'Save' : 'Add equipment' }}
        </button>
      </form>
    </SlideOver>
  </section>
</template>

<style scoped>
.right {
  text-align: right;
}
.actions {
  display: flex;
  gap: 4px;
  justify-content: flex-end;
}
.danger {
  color: var(--led-danger);
}
.hint {
  font-size: 12px;
  margin: 0;
}
.err {
  padding: var(--s3) var(--s4);
  margin: 0;
}
</style>
