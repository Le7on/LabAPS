<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

const groups = [
  {
    title: 'Operate',
    items: [
      { to: '/dashboard', label: 'Overview', icon: '◧' },
      { to: '/scheduling', label: 'Scheduling', icon: '◷' },
      { to: '/plans', label: 'Plans', icon: '▤' },
      { to: '/availability', label: 'Availability', icon: '▦' },
    ],
  },
  {
    title: 'Laboratory',
    items: [
      { to: '/projects', label: 'Projects', icon: '▣' },
      { to: '/equipment', label: 'Equipment', icon: '⬡' },
      { to: '/staff', label: 'Staff', icon: '◎' },
      { to: '/workflow-definitions', label: 'Workflows', icon: '⇥' },
    ],
  },
]

const bare = computed(() => route.meta.public)

onMounted(() => auth.restore())

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <RouterView v-if="bare" />
  <div v-else class="shell">
    <aside class="rail">
      <div class="rail__brand">
        <span class="rail__mark">◇</span>
        <span class="rail__name">Lab APS</span>
      </div>
      <nav class="rail__nav">
        <div v-for="g in groups" :key="g.title" class="rail__group">
          <div class="rail__grouptitle">{{ g.title }}</div>
          <RouterLink v-for="it in g.items" :key="it.to" :to="it.to" class="rail__link">
            <span class="rail__icon">{{ it.icon }}</span>
            <span>{{ it.label }}</span>
          </RouterLink>
        </div>
      </nav>
      <div class="rail__foot">
        <template v-if="auth.isAuthenticated()">
          <div class="rail__user">
            <div class="rail__username">{{ auth.user.username }}</div>
            <div class="rail__role">{{ auth.user.role }}</div>
          </div>
          <button class="rail__signout" @click="logout">Sign out</button>
        </template>
        <RouterLink v-else to="/login" class="rail__link">Sign in</RouterLink>
      </div>
    </aside>
    <main class="workspace">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.shell {
  display: flex;
  min-height: 100vh;
}
.rail {
  width: 216px;
  flex-shrink: 0;
  background: var(--rail);
  color: var(--rail-ink);
  display: flex;
  flex-direction: column;
  padding: var(--s4) var(--s3);
}
.rail__brand {
  display: flex;
  align-items: center;
  gap: var(--s2);
  padding: var(--s2) var(--s3) var(--s5);
}
.rail__mark {
  color: var(--accent);
  font-size: 1.2rem;
}
.rail__name {
  color: var(--rail-ink-strong);
  font-weight: 600;
  letter-spacing: 0.04em;
  font-size: 0.95rem;
}
.rail__group {
  margin-bottom: var(--s5);
}
.rail__grouptitle {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  color: #55607a;
  padding: 0 var(--s3) var(--s2);
}
.rail__link {
  display: flex;
  align-items: center;
  gap: var(--s3);
  padding: 7px var(--s3);
  border-radius: var(--r-md);
  color: var(--rail-ink);
  font-size: 13.5px;
  transition: background 0.14s;
}
.rail__link:hover {
  background: rgba(255, 255, 255, 0.06);
  color: var(--rail-ink-strong);
}
.rail__link.router-link-active {
  background: rgba(255, 255, 255, 0.08);
  color: var(--rail-ink-strong);
  box-shadow: inset 2px 0 0 var(--accent);
}
.rail__icon {
  width: 18px;
  text-align: center;
  opacity: 0.85;
}
.rail__foot {
  margin-top: auto;
  padding-top: var(--s4);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}
.rail__user {
  padding: 0 var(--s3) var(--s2);
}
.rail__username {
  color: var(--rail-ink-strong);
  font-size: 13px;
  font-weight: 500;
}
.rail__role {
  font-size: 11px;
  color: #55607a;
  font-family: var(--font-mono);
}
.rail__signout {
  width: 100%;
  margin-top: var(--s1);
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: var(--rail-ink);
  padding: 6px;
  border-radius: var(--r-md);
  cursor: pointer;
  font-family: inherit;
  font-size: 12.5px;
}
.rail__signout:hover {
  background: rgba(255, 255, 255, 0.06);
  color: var(--rail-ink-strong);
}
.workspace {
  flex: 1;
  min-width: 0;
  padding: var(--s6) var(--s6);
  max-width: 1240px;
}
</style>
