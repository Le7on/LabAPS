<script setup>
// Page header: a title zone with room for a primary action on the right.
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
</script>

<template>
  <header class="page-header">
    <div>
      <h1 class="page-header__title">{{ title }}</h1>
      <p v-if="subtitle" class="page-header__sub">{{ subtitle }}</p>
    </div>
    <div class="page-header__actions">
      <slot name="actions" />
    </div>
  </header>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--s4);
  margin-bottom: var(--s5);
}
.page-header__title {
  font-size: 20px;
}
.page-header__sub {
  margin: 3px 0 0;
  color: var(--ink-3);
  font-size: 13px;
}
.page-header__actions {
  display: flex;
  gap: var(--s2);
  flex-shrink: 0;
}
</style>
