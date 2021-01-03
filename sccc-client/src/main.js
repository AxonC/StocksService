import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import 'bulma/css/bulma.min.css'

import Login from "@/views/Login"

const routes = [
  {
    path: '/login',
    component: Login    
  }
]

console.log(process.env)

const router = createRouter({
  history: createWebHistory(),
  routes
})


const app = createApp(App)
app.use(router)

app.mount('#app')
