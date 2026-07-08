import { defineStore } from 'pinia'
import { ref } from 'vue'
import { createEquipment, createStaff, listEquipment, listStaff } from '../api/laboratory'

// Client-side state for Laboratory Definition (equipment + staff).
export const useLaboratoryStore = defineStore('laboratory', () => {
  const equipment = ref([])
  const staff = ref([])
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

  return {
    equipment,
    staff,
    error,
    fetchEquipment,
    addEquipment,
    fetchStaff,
    addStaff,
  }
})
