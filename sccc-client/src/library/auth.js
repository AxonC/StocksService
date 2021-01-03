import { computed, ref } from 'vue'
import axios from 'axios'

export const user = ref()
const token = sessionStorage.getItem('shares_token')

export function useAuth() {
  const isAuthenticated = ref(false)
  async function login (username, password) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    try {
      const { data } = await axios.post(`${process.env.VUE_APP_API_URL}/token`, 
        formData,
        {
          headers: { 
            Accept: 'application/json'
          }
        }
      )
      sessionStorage.setItem('shares_token', data.access_token)
      isAuthenticated.value = true
    } catch (e) {
      console.error(e)  
    }
  }

  async function checkExistingToken() {
    try {
      await axios.post(`${process.env.VUE_APP_API_URL}/login`, {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      isAuthenticated.value = true;
    } catch (e) {
      isAuthenticated.value = false;
    }
  }

  return {
    login,
    checkExistingToken,
    isAuthenticated: computed(() => isAuthenticated),
    token: computed(() => token)
  }
}