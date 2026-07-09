import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import PlansView from '../views/PlansView.vue'
import EquipmentView from '../views/EquipmentView.vue'
import StaffView from '../views/StaffView.vue'
import WorkflowDefinitionsView from '../views/WorkflowDefinitionsView.vue'
import SchedulingView from '../views/SchedulingView.vue'
import ProjectsView from '../views/ProjectsView.vue'

// Application routes. The Dashboard is the default landing view.
const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', name: 'dashboard', component: DashboardView },
  { path: '/plans', name: 'plans', component: PlansView },
  { path: '/projects', name: 'projects', component: ProjectsView },
  { path: '/equipment', name: 'equipment', component: EquipmentView },
  { path: '/staff', name: 'staff', component: StaffView },
  {
    path: '/workflow-definitions',
    name: 'workflow-definitions',
    component: WorkflowDefinitionsView,
  },
  { path: '/scheduling', name: 'scheduling', component: SchedulingView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
