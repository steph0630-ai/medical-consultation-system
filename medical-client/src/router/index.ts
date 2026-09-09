import { createRouter, createWebHistory } from 'vue-router'
import { currentUser, loadCurrentUser } from '../stores/auth'
import { getToken } from '../utils/request'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: () => import('../views/Login.vue') },
    { path: '/', component: () => import('../views/Home.vue') },
    { path: '/departments', component: () => import('../views/Departments.vue') },
  ],
})

router.beforeEach(async (to) => {
  const token = getToken()
  if (to.path !== '/login' && !token) return '/login'
  if (token && !currentUser.value && !(await loadCurrentUser())) return '/login'
  if (to.path === '/login' && currentUser.value) return '/'
})

export default router
