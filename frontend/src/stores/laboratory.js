import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  createEquipment,
  createStaff,
  createWorkflowDefinition,
  listEquipment,
  listStaff,
  listWorkflowDefinitions,
} from '../api/laboratory'

// Client-side state for Laboratory Definition (equipment, staff, workflows).
export const useLaboratoryStore = defineStore('laboratory', () => {
  const equipment = ref([])
  const staff = ref([])
  const workflows = ref([])
  const error = ref(null)

  async function fetchEquipment() {
    error.value = null
    try {
      const { data } = await listEquipment()
      equipment.value = data
    } catch (e) {
      error.value = e?.message ?? 'Failed to load equipment'
    }
  }

  async function addEquipment(payload) {
    error.value = null
    try {
      await createEquipment(payload)
      await fetchEquipment()
      return true
    } catch (e) {
      error.value = e?.message ?? 'Failed to create equipment'
      return false
    }
  }

  async function fetchStaff() {
    error.value = null
    try {
      const { data } = await listStaff()
      staff.value = data
    } catch (e) {
      error.value = e?.message ?? 'Failed to load staff'
    }
  }

  async function addStaff(payload) {
    error.value = null
    try {
      await createStaff(payload)
      await fetchStaff()
      return true
    } catch (e) {
      error.value = e?.message ?? 'Failed to create staff'
      return false
    }
  }

  async function fetchWorkflows() {
    error.value = null
    try {
      const { data } = await listWorkflowDefinitions()
      workflows.value = data
    } catch (e) {
      error.value = e?.message ?? 'Failed to load workflow definitions'
    }
  }

  async function addWorkflow(payload) {
    error.value = null
    try {
      await createWorkflowDefinition(payload)
      await fetchWorkflows()
      return true
    } catch (e) {
      error.value = e?.message ?? 'Failed to create workflow definition'
      return false
    }
  }

  return {
    equipment,
    staff,
    workflows,
    error,
    fetchEquipment,
    addEquipment,
    fetchStaff,
    addStaff,
    fetchWorkflows,
    addWorkflow,
  }
})
