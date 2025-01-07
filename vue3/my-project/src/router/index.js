import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import UserRegister from '../views/UserRegister.vue'
import UserLogin from '../views/Login.vue'
import UserHome from '../views/UserHome.vue'
import ReadQR from '../views/ReadQR.vue'
import ReceiptSimulator from '../views/ReceiptSimulator.vue'
import ReceiptList from '../views/ReceiptList.vue'
import UserSettings from '../views/UserSettings.vue'

const isAuthenticated = () => {
    return !!localStorage.getItem('token');
};

const routes = [
  { path: '/', name: 'Home', component: Home},
  { path: '/signup', name: 'UserRegister', component: UserRegister },
  { path: '/login', name: 'UserLogin', component: UserLogin },
  {
    path: '/mypage',
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
    path: '/mypage/qr_reader',
    name: 'qr_reader',
    component: ReadQR,
    beforeEnter: (to, from, next) => {
      if (isAuthenticated()) {
        next();
      } else {
        next('/login');
      }
    },
  },
  { path: '/mypage/receipt_list', name: 'ReceiptList', component: ReceiptList, 
    beforeEnter: (to, from, next) => {
        if (isAuthenticated()) {
        next();
        } else {
        next('/login');
        }
    },
  },
  { path: '/mypage/settings', name: 'UserSettings', component: UserSettings, 
  beforeEnter: (to, from, next) => {
      if (isAuthenticated()) {
      next();
      } else {
      next('/login');
      }
  },
},
  { path: '/receipt_simulator', name: 'ReceiptSimulator', component: ReceiptSimulator },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
