import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import 'bulma/css/bulma.min.css'

import Login from "@/views/Login"
import Dashboard from "@/views/Dashboard"

import { useAuth } from './library/auth'

const routes = [
  {
    path: '/login',
    component: Login,
    name: 'Login'    
  },
  {
    path: '/dashboard',
    component: Dashboard,
    name: 'Dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const {
    isAuthenticated,
    checkExistingToken
  } = useAuth()

  await checkExistingToken()

  if (!isAuthenticated && to.name !== 'Login') {
    next({ name: 'Login'})
  } else {
    next()
  }
})

const app = createApp(App)
app.use(router)

app.mount('#app')
