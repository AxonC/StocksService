import { computed, ref } from 'vue'
import axios from 'axios'

export const user = ref()
const token = localStorage.getItem('shares_token')

export function useAuth() {
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
      localStorage.setItem('shares_token', data.access_token) 
    } catch (e) {
      console.error(e)  
    }
  }

  return {
    login,
    token: computed(() => token.value)
  }
}