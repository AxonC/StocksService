import axios from 'axios'
import { computed, ref } from 'vue'
import { useAuth } from './auth'

export function useCompanies() {
  let companies = ref([])
  async function getCompanies() {
    const { token } = useAuth()
    const { data } = await axios.get(`${process.env.VUE_APP_API_URL}/companies`, {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    companies.value = data.data
  }
  return {
    getCompanies,
    companies: computed(() => companies.value)
  }
}