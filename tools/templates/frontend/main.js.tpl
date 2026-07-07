import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

// {{PROJECT_NAME}} application shell entry point.
const app = createApp(App)
app.use(createPinia())
app.mount('#app')
