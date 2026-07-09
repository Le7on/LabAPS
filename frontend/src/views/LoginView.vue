<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const token = ref('')

async function submit() {
  const ok = await auth.login(token.value)
  if (ok) router.push('/dashboard')
}
</script>

<template>
  <div class="login">
    <div class="card login__card">
      <div class="brand">Lab APS</div>
      <p class="muted">Sign in with your API token.</p>
      <form class="stack" @submit.prevent="submit">
        <div class="field">
          <label>API token</label>
          <input v-model="token" type="password" placeholder="Paste your token" required />
        </div>
        <button class="btn btn--primary" type="submit">Sign in</button>
      </form>
      <p v-if="auth.error" class="error">{{ auth.error }}</p>
    </div>
  </div>
</template>

<style scoped>
.login {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--color-bg);
}
.login__card {
  width: 340px;
}
.brand {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}
</style>
