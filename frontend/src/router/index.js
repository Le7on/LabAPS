import { createRouter, createWebHistory } from 'vue-router'
import PlansView from '../views/PlansView.vue'
import EquipmentView from '../views/EquipmentView.vue'
import StaffView from '../views/StaffView.vue'

// Application routes. The Plans workspace is the default landing view.
const routes = [
  { path: '/', redirect: '/plans' },
  { path: '/plans', name: 'plans', component: PlansView },
  { path: '/equipment', name: 'equipment', component: EquipmentView },
  { path: '/staff', name: 'staff', component: StaffView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
