import { ref } from 'vue'
import axios from 'axios'
import { useAuth } from './auth'
export function useCurrencies() {
  let currencies = ref([])

  async function getCurrencies() {
    const { generateAuthHeaders } = useAuth() 
    const { data } = await axios.get(`${process.env.VUE_APP_API_URL}/currencies`, generateAuthHeaders())
    currencies.value = data.data
  }

  return {
    getCurrencies,
    currencies
  }
}