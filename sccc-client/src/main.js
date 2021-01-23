import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import 'bulma/css/bulma.min.css'

import Login from "@/views/Login"
import Dashboard from "@/views/Dashboard"
import Company from '@/views/Company'

import { useAuth } from './library/auth'

const routes = [
  {
    path: '/',
    redirect: { name: 'Login'}
  },
  {
    path: '/login',
    component: Login,
    name: 'Login'    
  },
  {
    path: '/dashboard',
    component: Dashboard,
    name: 'Dashboard'
  },
  {
    path: '/company/:symbol:',
    component: Company,
    name: 'Company',
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const {
    isAuthenticated,
    checkExistingToken,
    fetchUserDetails
  } = useAuth()
  
  if (to.name !== 'Login') {
    await checkExistingToken();
  }


  if (!isAuthenticated.value && to.name !== 'Login') {
    next({ name: 'Login'})
  } else if (isAuthenticated.value && to.name == 'Login') {
    next({ name: 'Dashboard'})
  } else {
    await checkExistingToken()
    if (isAuthenticated.value) {
      await fetchUserDetails();
    }
    next()
  }
})

const app = createApp(App)
app.use(router)

app.mount('#app')
