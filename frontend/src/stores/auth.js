import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getToken, setToken } from '../api/client'
import { whoami } from '../api/auth'

// Authentication state (ADR-013). The token is a bearer token stored locally;
// the current user is resolved via /auth/whoami.
export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const ready = ref(false)
  const error = ref(null)

  const isAuthenticated = () => user.value !== null

  async function restore() {
    // On startup, if a token exists, try to resolve the user.
    if (getToken()) {
      try {
        user.value = await whoami()
      } catch {
        setToken(null)
      }
    }
    ready.value = true
  }

  async function login(token) {
    error.value = null
    setToken(token.trim())
    try {
      user.value = await whoami()
      return true
    } catch (e) {
      setToken(null)
      user.value = null
      error.value = e?.message ?? 'Invalid token'
      return false
    }
  }

  function logout() {
    setToken(null)
    user.value = null
  }

  return { user, ready, error, isAuthenticated, restore, login, logout }
})
