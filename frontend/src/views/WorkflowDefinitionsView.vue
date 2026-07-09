<script setup>
import { onMounted, reactive } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'

const store = useLaboratoryStore()

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
  }
}
</script>

<template>
  <section class="stack">
    <h2>Workflow Definitions</h2>

    <div class="card">
      <div class="card__title">New workflow</div>
      <form class="stack" @submit.prevent="submit">
        <div class="form-row">
          <div class="field">
            <label>Workflow code</label>
            <input v-model="form.workflowCode" placeholder="WF-001" required />
          </div>
          <div class="field">
            <label>Name</label>
            <input v-model="form.name" placeholder="Sample prep" required />
          </div>
        </div>

        <div class="ops">
          <div class="ops__head row">
            <span>Operation type</span>
            <span>Duration</span>
            <span>Capability</span>
            <span>Skill</span>
            <span>Qualification</span>
            <span></span>
          </div>
          <div v-for="(op, i) in form.operations" :key="i" class="ops__row row">
            <input v-model="op.operationType" placeholder="amplify" />
            <input v-model.number="op.duration" type="number" min="1" />
            <input v-model="op.requiredCapability" placeholder="pcr" />
            <input v-model="op.requiredSkill" placeholder="pcr" />
            <input v-model="op.requiredQualification" placeholder="gmp" />
            <button class="btn btn--ghost" type="button" @click="removeOp(i)">✕</button>
          </div>
        </div>

        <div class="row">
          <button class="btn" type="button" @click="addOp">+ Operation</button>
          <div class="spacer"></div>
          <button class="btn btn--primary" type="submit">Create workflow</button>
        </div>
      </form>
      <p v-if="store.error" class="error">{{ store.error }}</p>
    </div>

    <div class="card">
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
            <td>{{ wf.workflowCode }}</td>
            <td>{{ wf.name }}</td>
            <td>{{ wf.operations.length }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="empty">No workflow definitions yet.</p>
    </div>
  </section>
</template>

<style scoped>
.ops__head,
.ops__row {
  display: grid;
  grid-template-columns: 1.5fr 0.7fr 1fr 1fr 1fr auto;
  gap: 0.5rem;
  align-items: center;
}
.ops__head {
  font-size: 0.75rem;
  color: var(--color-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.ops__row + .ops__row {
  margin-top: 0.4rem;
}
</style>
