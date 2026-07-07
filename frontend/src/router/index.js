import { createRouter, createWebHistory } from 'vue-router'
import PlansView from '../views/PlansView.vue'

// Application routes. The Plans workspace is the default landing view.
const routes = [
  { path: '/', redirect: '/plans' },
  { path: '/plans', name: 'plans', component: PlansView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
