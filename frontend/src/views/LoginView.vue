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
    <div class="panel login__card">
      <div class="login__brand"><span class="login__mark">◇</span> Lab APS</div>
      <p class="muted login__hint">Sign in with your API token.</p>
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
  background: var(--canvas);
}
.login__card {
  width: 360px;
  padding: var(--s6);
}
.login__brand {
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  display: flex;
  align-items: center;
  gap: var(--s2);
}
.login__mark {
  color: var(--accent);
}
.login__hint {
  margin: 6px 0 var(--s4);
  font-size: 13px;
}
</style>
