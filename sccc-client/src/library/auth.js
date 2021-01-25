import { ref } from 'vue'
import axios from 'axios'

export const user = ref({})
const token = ref(sessionStorage.getItem('shares_token'))

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
      token.value = data.access_token
      isAuthenticated.value = true
    } catch (e) {
      console.error(e)  
    }
  }

  async function checkExistingToken() {
    try {
      await axios.post(`${process.env.VUE_APP_API_URL}/login`, {}, {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })
      isAuthenticated.value = true;
    } catch (e) {
      isAuthenticated.value = false;
    }
  }

  async function fetchUserDetails() {
    try {
      const { data } = await axios.get(`${process.env.VUE_APP_API_URL}/me`,
        {
          headers: {
            Authorization: `Bearer ${token.value}`
          }
        })
      user.value = data.data
    } catch (e) {
      console.error(e)
    }
  }

  function generateAuthHeaders() {
    return {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    }
  }

  return {
    login,
    checkExistingToken,
    isAuthenticated,
    fetchUserDetails,
    user,
    token,
    generateAuthHeaders
  }
}