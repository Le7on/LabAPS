<script setup>
// Right-hand slide-over panel for create/edit forms. Overlay elevation uses a
// shadow (the one place shadows are allowed); enters origin-aware from the right.
defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, default: '' },
})
const emit = defineEmits(['close'])
</script>

<template>
  <Transition name="slideover">
    <div v-if="open" class="slideover" @keydown.esc="emit('close')">
      <div class="slideover__scrim" @click="emit('close')" />
      <aside class="slideover__panel" role="dialog" aria-modal="true">
        <header class="slideover__head">
          <span class="panel__title">{{ title }}</span>
          <button class="btn btn--ghost" aria-label="Close" @click="emit('close')">✕</button>
        </header>
        <div class="slideover__body">
          <slot />
        </div>
      </aside>
    </div>
  </Transition>
</template>

<style scoped>
.slideover {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  justify-content: flex-end;
}
.slideover__scrim {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.28);
}
.slideover__panel {
  position: relative;
  width: 420px;
  max-width: 92vw;
  background: var(--panel);
  border-left: 1px solid var(--line-2);
  box-shadow: var(--overlay-shadow);
  display: flex;
  flex-direction: column;
}
.slideover__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--s3) var(--s4);
  border-bottom: 1px solid var(--line);
}
.slideover__body {
  padding: var(--s5);
  overflow-y: auto;
}

/* Origin-aware enter from the right; scrim fades. */
.slideover-enter-active,
.slideover-leave-active {
  transition: opacity 0.2s cubic-bezier(0.23, 1, 0.32, 1);
}
.slideover-enter-active .slideover__panel,
.slideover-leave-active .slideover__panel {
  transition: transform 0.24s cubic-bezier(0.23, 1, 0.32, 1);
}
.slideover-enter-from,
.slideover-leave-to {
  opacity: 0;
}
.slideover-enter-from .slideover__panel,
.slideover-leave-to .slideover__panel {
  transform: translateX(24px);
}
@media (prefers-reduced-motion: reduce) {
  .slideover-enter-active .slideover__panel,
  .slideover-leave-active .slideover__panel {
    transition: none;
  }
}
</style>
