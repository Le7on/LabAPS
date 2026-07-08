<script setup>
// Lab APS application shell: header, navigation and routed content.
</script>

<template>
  <div class="app">
    <header class="app-header">
      <h1>Lab APS</h1>
      <nav>
        <RouterLink to="/plans">Plans</RouterLink>
        <RouterLink to="/equipment">Equipment</RouterLink>
        <RouterLink to="/staff">Staff</RouterLink>
      </nav>
    </header>
    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: baseline;
  gap: 1.5rem;
  padding: 1rem;
  border-bottom: 1px solid #ddd;
}
.app-main {
  padding: 1rem;
}
</style>
