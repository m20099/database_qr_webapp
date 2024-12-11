import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import UserRegister from '../views/UserRegister.vue'
import UserLogin from '../views/Login.vue'
import UserHome from '../views/UserHome.vue'
import ReadQR from '../views/ReadQR.vue'
import StoreHome from '../views/Storehome.vue'

const isAuthenticated = () => {
    return !!localStorage.getItem('token');
};

const routes = [
  { path: '/', name: 'Home', component: Home},
  { path: '/userregister', name: 'UserRegister', component: UserRegister },
  { path: '/login', name: 'UserLogin', component: UserLogin },
  {
    path: '/userhome',
    name: 'UserHome',
    component: UserHome,
    beforeEnter: (to, from, next) => {
      if (isAuthenticated()) {
        next();
      } else {
        next('/login'); 
      }
    },
  },
  {
    path: '/userhome/qr_reader',
    name: 'qr_reader',
    component: ReadQR,
    beforeEnter: (to, from, next) => {
      if (isAuthenticated()) {
        next();
      } else {
        next('/login');
      }
    },
  },  { path: '/StoreHome', name: 'StoreHome', component: StoreHome }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
