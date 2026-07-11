import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  createEquipment,
  createProject,
  createStaff,
  createWorkflowDefinition,
  deleteEquipment,
  deleteProject,
  deleteStaff,
  deleteWorkflowDefinition,
  listEquipment,
  listProjects,
  listStaff,
  listWorkflowDefinitions,
  setResourceActive,
  updateEquipment,
  updateProject,
  updateStaff,
} from '../api/laboratory'

// Client-side state for Laboratory Definition (equipment, staff, workflows, projects).
export const useLaboratoryStore = defineStore('laboratory', () => {
  const equipment = ref([])
  const staff = ref([])
  const workflows = ref([])
  const projects = ref([])
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

  async function fetchProjects() {
    error.value = null
    try {
      const { data } = await listProjects()
      projects.value = data
    } catch (e) {
      error.value = e?.message ?? 'Failed to load projects'
    }
  }

  async function addProject(payload) {
    error.value = null
    try {
      await createProject(payload)
      await fetchProjects()
      return true
    } catch (e) {
      error.value = e?.message ?? 'Failed to create project'
      return false
    }
  }

  const REFRESH = {
    equipment: fetchEquipment,
    staff: fetchStaff,
    projects: fetchProjects,
  }

  async function setActive(kind, id, active) {
    error.value = null
    try {
      await setResourceActive(kind, id, active)
      await REFRESH[kind]()
      return true
    } catch (e) {
      error.value = e?.message ?? 'Failed to update status'
      return false
    }
  }

  // Wrap a write op with error capture + refresh; returns true on success.
  async function _mutate(fn, refresh, msg) {
    error.value = null
    try {
      await fn()
      await refresh()
      return true
    } catch (e) {
      error.value = e?.message ?? msg
      return false
    }
  }

  const editProject = (id, p) =>
    _mutate(() => updateProject(id, p), fetchProjects, 'Failed to update project')
  const removeProject = (id) =>
    _mutate(() => deleteProject(id), fetchProjects, 'Failed to delete project')
  const editEquipment = (id, p) =>
    _mutate(() => updateEquipment(id, p), fetchEquipment, 'Failed to update equipment')
  const removeEquipment = (id) =>
    _mutate(() => deleteEquipment(id), fetchEquipment, 'Failed to delete equipment')
  const editStaff = (id, p) =>
    _mutate(() => updateStaff(id, p), fetchStaff, 'Failed to update staff')
  const removeStaff = (id) => _mutate(() => deleteStaff(id), fetchStaff, 'Failed to delete staff')
  const removeWorkflow = (id) =>
    _mutate(() => deleteWorkflowDefinition(id), fetchWorkflows, 'Failed to delete workflow')

  return {
    equipment,
    staff,
    workflows,
    projects,
    error,
    fetchEquipment,
    addEquipment,
    fetchStaff,
    addStaff,
    fetchWorkflows,
    addWorkflow,
    fetchProjects,
    addProject,
    setActive,
    editProject,
    removeProject,
    editEquipment,
    removeEquipment,
    editStaff,
    removeStaff,
    removeWorkflow,
  }
})
