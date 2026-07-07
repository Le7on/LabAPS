import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

// Lab APS application shell entry point.
const app = createApp(App)
app.use(createPinia())
app.mount('#app')
