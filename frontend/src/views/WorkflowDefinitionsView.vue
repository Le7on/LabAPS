<script setup>
import { onMounted, reactive } from 'vue'
import { useLaboratoryStore } from '../stores/laboratory'

const store = useLaboratoryStore()

const form = reactive({
  workflowCode: '',
  name: '',
  operations: [{ operationType: '', duration: 1, requiredCapability: '', requiredSkill: '' }],
})

onMounted(() => {
  store.fetchWorkflows()
})

function addOperationRow() {
  form.operations.push({
    operationType: '',
    duration: 1,
    requiredCapability: '',
    requiredSkill: '',
  })
}

function removeOperationRow(index) {
  form.operations.splice(index, 1)
}

async function submit() {
  const operations = form.operations
    .filter((op) => op.operationType.trim())
    .map((op) => ({
      operationType: op.operationType.trim(),
      duration: Number(op.duration) || 1,
      requiredCapability: op.requiredCapability.trim() || undefined,
      requiredSkill: op.requiredSkill.trim() || undefined,
    }))

  const created = await store.addWorkflow({
    workflowCode: form.workflowCode,
    name: form.name,
    operations,
  })
  if (created) {
    form.workflowCode = ''
    form.name = ''
    form.operations = [
      { operationType: '', duration: 1, requiredCapability: '', requiredSkill: '' },
    ]
  }
}
</script>

<template>
  <section>
    <h2>Workflow Definitions</h2>

    <form class="wf-form" @submit.prevent="submit">
      <div class="row">
        <input v-model="form.workflowCode" placeholder="Workflow code" required />
        <input v-model="form.name" placeholder="Name" required />
      </div>

      <div v-for="(op, index) in form.operations" :key="index" class="row">
        <input v-model="op.operationType" placeholder="Operation type" />
        <input v-model.number="op.duration" type="number" min="1" placeholder="Duration" />
        <input v-model="op.requiredCapability" placeholder="Capability" />
        <input v-model="op.requiredSkill" placeholder="Skill" />
        <button type="button" @click="removeOperationRow(index)">Remove</button>
      </div>

      <div class="row">
        <button type="button" @click="addOperationRow">Add operation</button>
        <button type="submit">Create workflow</button>
      </div>
    </form>

    <p v-if="store.error" class="error">{{ store.error }}</p>

    <table v-if="store.workflows.length">
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

    <p v-else>No workflow definitions yet.</p>
  </section>
</template>

<style scoped>
.wf-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.error {
  color: #b00020;
}
table {
  border-collapse: collapse;
  width: 100%;
}
th,
td {
  border: 1px solid #ddd;
  padding: 0.4rem 0.6rem;
  text-align: left;
}
</style>
