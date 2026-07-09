<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const nav = [
  { to: '/dashboard', label: 'Dashboard', icon: '▚' },
  { to: '/plans', label: 'Plans', icon: '▤' },
  { to: '/scheduling', label: 'Scheduling', icon: '◷' },
  { section: 'Laboratory' },
  { to: '/projects', label: 'Projects', icon: '▣' },
  { to: '/equipment', label: 'Equipment', icon: '⚙' },
  { to: '/staff', label: 'Staff', icon: '☺' },
  { to: '/workflow-definitions', label: 'Workflows', icon: '⇄' },
]

// Show the chrome-less layout on the public login page.
const bare = computed(() => route.meta.public)

onMounted(() => auth.restore())

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <RouterView v-if="bare" />
  <div v-else class="layout">
    <aside class="sidebar">
      <div class="brand">Lab APS</div>
      <nav class="nav">
        <template v-for="(item, i) in nav" :key="i">
          <div v-if="item.section" class="nav__section">{{ item.section }}</div>
          <RouterLink v-else :to="item.to" class="nav__link">
            <span class="nav__icon">{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </RouterLink>
        </template>
      </nav>
      <div class="sidebar__footer">
        <template v-if="auth.isAuthenticated()">
          <div class="user">{{ auth.user.username }} · {{ auth.user.role }}</div>
          <button class="btn btn--ghost logout" @click="logout">Sign out</button>
        </template>
        <RouterLink v-else to="/login" class="nav__link">Sign in</RouterLink>
      </div>
    </aside>
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 220px;
  background: #101828;
  color: #cbd5e1;
  padding: 1.25rem 0.75rem;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}
.brand {
  color: #fff;
  font-size: 1.15rem;
  font-weight: 700;
  padding: 0.5rem 0.75rem 1rem;
  letter-spacing: 0.02em;
}
.nav {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}
.nav__section {
  color: #64748b;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 1rem 0.75rem 0.35rem;
}
.nav__link {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  color: #cbd5e1;
  font-size: 0.9rem;
}
.nav__link:hover {
  background: #1d2939;
  color: #fff;
}
.nav__link.router-link-active {
  background: #2f6feb;
  color: #fff;
}
.nav__icon {
  width: 1.1rem;
  text-align: center;
  opacity: 0.9;
}
.sidebar__footer {
  margin-top: auto;
  padding: 0.75rem;
  border-top: 1px solid #1d2939;
}
.user {
  font-size: 0.8rem;
  color: #94a3b8;
  margin-bottom: 0.5rem;
}
.logout {
  color: #cbd5e1;
  border-color: #334155;
  width: 100%;
}
.content {
  flex: 1;
  padding: 1.75rem 2rem;
  max-width: 1200px;
}
</style>
