import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import PlansView from '../views/PlansView.vue'
import EquipmentView from '../views/EquipmentView.vue'
import StaffView from '../views/StaffView.vue'
import WorkflowDefinitionsView from '../views/WorkflowDefinitionsView.vue'

// Application routes. The Dashboard is the default landing view.
const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', name: 'dashboard', component: DashboardView },
  { path: '/plans', name: 'plans', component: PlansView },
  { path: '/equipment', name: 'equipment', component: EquipmentView },
  { path: '/staff', name: 'staff', component: StaffView },
  {
    path: '/workflow-definitions',
    name: 'workflow-definitions',
    component: WorkflowDefinitionsView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
