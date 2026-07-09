<script setup>
// Lab APS application shell: sidebar navigation + routed content.
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
</script>

<template>
  <div class="layout">
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
.content {
  flex: 1;
  padding: 1.75rem 2rem;
  max-width: 1200px;
}
</style>
