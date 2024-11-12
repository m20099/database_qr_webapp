import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Storehome from '../views/Storehome.vue'
import Userhome from '../views/Userhome.vue'

const routes = [
  { path: '/', name: 'Home', component: Home},
  { path: '/storehome', name: 'Storehome', component: Storehome },
  { path: '/userhome', name: 'Userhome', component: Userhome }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
