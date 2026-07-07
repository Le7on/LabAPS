import { defineStore } from 'pinia'
import { ref } from 'vue'
import { createPlan, listPlans } from '../api/plans'

// Client-side state for Plans (Pinia). Business state stays on the backend.
export const usePlansStore = defineStore('plans', () => {
  const plans = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchPlans() {
    loading.value = true
    error.value = null
    try {
      const data = await listPlans()
      plans.value = data.items
    } catch (e) {
      error.value = e?.response?.data?.message ?? 'Failed to load plans'
    } finally {
      loading.value = false
    }
  }

  async function addPlan(payload) {
    error.value = null
    try {
      await createPlan(payload)
      await fetchPlans()
      return true
    } catch (e) {
      error.value = e?.response?.data?.message ?? 'Failed to create plan'
      return false
    }
  }

  return { plans, loading, error, fetchPlans, addPlan }
})
