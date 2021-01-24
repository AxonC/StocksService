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

  async function getCompany(symbol) {
    const { token } = useAuth()
    const { data } = await axios.get(`${process.env.VUE_APP_API_URL}/companies/${symbol}`, {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    return data
  }

  async function getCompanyPriceHistory(symbol) {
    const { token } = useAuth()
    const { data } = await axios.get(`${process.env.VUE_APP_API_URL}/companies/${symbol}/history`, {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    return data
  }


  async function getCompanyTransactionHistory(symbol) {
    const { generateAuthHeaders } = useAuth()
    const { data } = await axios.get(`${process.env.VUE_APP_API_URL}/companies/${symbol}/transactions`, generateAuthHeaders())
    return data
  }

  async function purchaseShares(symbol, currency, amount_of_shares) {
    const { token } = useAuth()
    await axios.post(`${process.env.VUE_APP_API_URL}/companies/${symbol}/purchase`, 
      {
        currency,
        symbol,
        amount_of_shares
      },
      {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })
  }

  async function sellShares(symbol, currency, amount_of_shares) {
    const { generateAuthHeaders } = useAuth()
    await axios.post(`${process.env.VUE_APP_API_URL}/companies/${symbol}/sell`, 
      {
        currency,
        symbol,
        amount_of_shares
      },
      generateAuthHeaders()
    )
  }

  async function createCompany({ name, symbol, available_shares }, currency = 'USD') {
    const { generateAuthHeaders } = useAuth()
    await axios.post(`${process.env.VUE_APP_API_URL}/admin/companies`, 
      {
        company: {
          name,
          symbol,
          available_shares,
        },
        currency
      },
      generateAuthHeaders()
    )
  }

  async function modifyCompany(symbol, { available_shares }) {
    const {generateAuthHeaders} = useAuth()
    await axios.patch(`${process.env.VUE_APP_API_URL}/admin/companies/${symbol}`, 
      {
        available_shares
      },
      generateAuthHeaders())
  }

  async function refreshPrices(symbol, currency) {
    const { generateAuthHeaders } = useAuth()
    await axios.patch(`${process.env.VUE_APP_API_URL}/companies/${symbol}/update-prices`, {
      currency
    }, generateAuthHeaders())
  }
  return {
    getCompanies,
    getCompany,
    getCompanyPriceHistory,
    getCompanyTransactionHistory,
    purchaseShares,
    sellShares,
    createCompany,
    modifyCompany,
    refreshPrices,
    companies: computed(() => companies.value)
  }
}