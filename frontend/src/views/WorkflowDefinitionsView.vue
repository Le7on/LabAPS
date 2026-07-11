<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'
import PageHeader from '../components/PageHeader.vue'
import SlideOver from '../components/SlideOver.vue'

const store = useLaboratoryStore()
const open = ref(false)

function emptyOp() {
  return {
    operationType: '',
    duration: 1,
    requiredCapability: '',
    requiredSkill: '',
    requiredQualification: '',
  }
}

const form = reactive({ workflowCode: '', name: '', operations: [emptyOp()] })

onMounted(() => store.fetchWorkflows())

function addOp() {
  form.operations.push(emptyOp())
}
function removeOp(i) {
  form.operations.splice(i, 1)
}

async function submit() {
  const operations = form.operations
    .filter((op) => op.operationType.trim())
    .map((op) => ({
      operationType: op.operationType.trim(),
      duration: Number(op.duration) || 1,
      requiredCapability: op.requiredCapability.trim() || undefined,
      requiredSkill: op.requiredSkill.trim() || undefined,
      requiredQualification: op.requiredQualification.trim() || undefined,
    }))

  const ok = await store.addWorkflow({
    workflowCode: form.workflowCode,
    name: form.name,
    operations,
  })
  if (ok) {
    form.workflowCode = ''
    form.name = ''
    form.operations = [emptyOp()]
    open.value = false
  }
}
</script>

<template>
  <section>
    <PageHeader title="Workflows" subtitle="Reusable operation templates with requirements">
      <template #actions>
        <button class="btn btn--primary" @click="open = true">+ New workflow</button>
      </template>
    </PageHeader>

    <div class="panel">
      <table v-if="store.workflows.length" class="table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Operations</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="wf in store.workflows" :key="wf.id">
            <td class="mono cell-strong">{{ wf.workflowCode }}</td>
            <td class="cell-strong">{{ wf.name }}</td>
            <td class="mono">{{ wf.operations.length }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No workflow definitions yet.</p>
    </div>

    <SlideOver :open="open" title="New workflow" @close="open = false">
      <form class="stack" @submit.prevent="submit">
        <div class="field">
          <label>Workflow code</label>
          <input v-model="form.workflowCode" placeholder="WF-001" required />
        </div>
        <div class="field">
          <label>Name</label>
          <input v-model="form.name" placeholder="Sample prep" required />
        </div>

        <div class="ops">
          <div class="label">Operations</div>
          <div v-for="(op, i) in form.operations" :key="i" class="op">
            <div class="op__head">
              <span class="op__n mono">#{{ i + 1 }}</span>
              <button class="btn btn--sm btn--ghost" type="button" @click="removeOp(i)">✕</button>
            </div>
            <div class="op__grid">
              <input v-model="op.operationType" placeholder="type (amplify)" />
              <input v-model.number="op.duration" type="number" min="1" placeholder="dur" />
              <input v-model="op.requiredCapability" placeholder="capability" />
              <input v-model="op.requiredSkill" placeholder="skill" />
              <input v-model="op.requiredQualification" placeholder="qualification" />
            </div>
          </div>
          <button class="btn btn--sm" type="button" @click="addOp">+ Operation</button>
        </div>

        <p v-if="store.error" class="error">{{ store.error }}</p>
        <button class="btn btn--primary" type="submit">Create workflow</button>
      </form>
    </SlideOver>
  </section>
</template>

<style scoped>
.ops {
  display: flex;
  flex-direction: column;
  gap: var(--s2);
}
.op {
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  padding: var(--s2);
  background: var(--panel-2);
}
.op__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--s2);
}
.op__n {
  font-size: 11px;
  color: var(--ink-3);
}
.op__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--s2);
}
.op__grid > input:first-child {
  grid-column: 1 / -1;
}
</style>
