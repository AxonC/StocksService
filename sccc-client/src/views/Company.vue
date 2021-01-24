<template>
  <div>
    <modal :close-callback="toggleModal" :active="showBuyModal">
      <template v-slot:title>Buy Shares</template>
      <template v-slot:default>
        <div>
          Cost (USD): {{ company.last * sharesToBuy }}
        </div>
        <div class="control">
          <label for="">Shares</label>
          <input class="input" type="text" v-model="sharesToBuy" />
        </div>
          <div class="select mt-3">
            <select name="" id="" v-model="currencyToBuy">
              <option :value="currency.code" :key="currency.code" v-for="currency in currencies">{{ currency.name }} ({{ currency.code}})</option>
            </select>
          </div>
      </template>
      <template v-slot:footer>
        <button class="button is-success" @click="purchase">
          Buy Shares
        </button>
      </template>
    </modal>
    <modal :close-callback="toggleModal" :active="showSellModal">
      <template v-slot:title>Sell Shares</template>
      <template v-slot:default>
        <div>
          Sale Price: {{ company.last * sharesToSell }}
        </div>
        <label for="">Shares</label>
        <input class="input" type="text" v-model="sharesToSell" />
      </template>
      <template v-slot:footer>
        <button class="button is-success" @click="sell">
          Sell Shares
        </button>
      </template>
    </modal>
    <div class="is-flex is-justify-content-space-between mb-2">
      <router-link :to="{ name: 'Dashboard' }">Back</router-link>
      <a @click="refreshPricing">
        Refresh Prices
      </a>

    </div>
    <div class="box">
      <div class="block is-flex is-justify-content-space-between is-align-items-center">
        <div>
          <h1 class="title">{{ company.symbol }}</h1>
          <p class="subtitle">{{ company.description }}</p>
        </div>
        <div>
          <span class="title is-4">
            ${{ company.last }} /
          </span>
          <span class="title is-4" :class="[formatColor(company.change_percentage)]">
            {{ company.change_percentage }}%
          </span>
        </div>
      </div>
      <hr />
      <div class="block">
        <div class="is-flex is-justify-content-space-between is-align-items-center">
          <div class="is-flex is-flex-direction-column is-align-items-baseline">
            <span class="is-size-3">
              {{ company.available_shares }}
            </span>
            <span class="is-size-6 is-uppercase is-italic has-text-weight-bold has-text-grey-light">
              Available Shares
            </span>
          </div>
          <button class="button is-primary" @click="toggleModal('buy')">Buy Shares</button>
        </div>
      </div>
      <hr />
      <div class="block">
        <div class="is-flex is-justify-content-space-between is-align-items-center">
          <div class="is-flex is-flex-direction-column is-align-items-baseline">
            <span class="is-size-3">
            {{ company.shares_owned }}
            </span>
            <span class="is-size-6 is-uppercase is-italic has-text-weight-bold has-text-grey-light">
              Owned Shares
            </span>
          </div>
          <button class="button is-warning" :disabled="canSellShares.value" @click="toggleModal('sell')">
            Sell Shares
          </button>
        </div>
      </div>
    </div>
    <box>
      <template v-slot:title>Price History
      </template>
      <template v-slot:subtitle>Known price history when prices have been updated</template>
      <table class="table is-fullwidth">
        <thead>
          <th>Date / Time</th>
          <th>Price</th>
          <th>Currency</th>
        </thead>
        <tbody>
          <tr v-for="history in priceHistory" :key="history.timestamp">
            <td>{{ formatDate(history.timestamp) }}</td>
            <td>{{ history.price }}</td>
            <td>{{ history.currency }}</td>
          </tr>
        </tbody>
      </table>
    </box>
    <box>
      <template v-slot:title>Transation History</template>
      <table class="table is-fullwidth" v-if="transactions.length">
        <thead>
          <th>Transaction type</th>
          <th>Shares</th>
          <th>Price</th>
          <th>Currency</th>
          <th>Date</th>
        </thead>
        <tbody>
          <tr v-for="transaction in transactions" :key="transaction.transaction_id">
            <td>{{ determineTransactionType(transaction.transaction_type ) }}</td>
            <td>{{ transaction.total }}</td>
            <td>{{ transaction.amount }}</td>
            <td>{{ transaction.currecny }}</td>
            <td>{{ formatDate(transaction.transaction_at) }}</td>
          </tr>
        </tbody>
      </table>
      <div class="is-flex is-justify-content-center is-italtic" v-else>
        No purchases found for this company :(
      </div>
    </box>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useCompanies } from '../library/companies'
import { useAuth } from '../library/auth'
import { useCurrencies } from '../library/currencies'
import { useRoute } from 'vue-router'
import { toast } from 'bulma-toast'
import { formatDate } from '../library/helpers'
import Box from '../components/Box'
import Modal from '../components/Modal'
export default {
  components: {
    Box,
    Modal
  },
  setup() {
    const {
      getCompany,
      getCompanyPriceHistory,
      purchaseShares,
      sellShares,
      getCompanyTransactionHistory,
      refreshPrices
    } = useCompanies()
    const {
      currencies,
      getCurrencies
    } = useCurrencies()
    const { fetchUserDetails } = useAuth()
    const route = useRoute()
    const company = ref({})
    const transactions = ref([])
    const priceHistory = ref([])
    const showBuyModal = ref(false)
    const showSellModal = ref(false)
    const currencyToBuy = ref('USD')
    const sharesToBuy = ref(0)
    const sharesToSell = ref(0)
    const assignCompany = async (symbol) => {
      const { data } = await getCompany(symbol)
      company.value = data
    } 
    const assignPriceHistory = async (symbol) => {
      const { data } = await getCompanyPriceHistory(symbol)
      priceHistory.value = data
    }
    const assignTransactions = async (symbol) => {
      const { data } = await getCompanyTransactionHistory(symbol)
      transactions.value = data
    }
    const formatColor = (value) => {
      if (value < 0) {
        return 'has-text-danger'
      } else if (value > 0) {
        return 'has-text-success'
      }
      return ''
    }
    const determineTransactionType = (type) => {
      return {
        1: 'Purchase',
        2: 'Sale'
      }[type] || ''
    }
    function toggleModal(type) {
      if (type == 'sell') {
        showSellModal.value = !showSellModal.value
      } else {
        showBuyModal.value = !showBuyModal.value
      }
    }
    const canSellShares = computed(() => company.value.shares_owned > 0)
    onMounted(() => assignCompany(route.params.symbol))
    onMounted(() => assignPriceHistory(route.params.symbol))
    onMounted(() => assignTransactions(route.params.symbol))
    onMounted(getCurrencies)
    const purchase = async () => {
      await purchaseShares(company.value.symbol, currencyToBuy.value, sharesToBuy.value)
      await assignCompany(route.params.symbol)
      await fetchUserDetails()
      showBuyModal.value = false
      toast({
        message: 'Shares purchased!',
        type: 'is-success',
        position: 'top-right'
      })
    }

    const sell = async () => {
      try {
        await sellShares(
          company.value.symbol,
          currencyToBuy.value,
          sharesToSell.value
        )
        await assignCompany(route.params.symbol)
        await fetchUserDetails()
        showSellModal.value = false
        toast({ 
          message: 'Shares sold!',
          type: 'is-success',
          position: 'top-right'
        })
      } catch (e) {
        toast({
          message: e.response.data.detail,
          type: 'is-danger',
          position: 'top-right'
        })
        showSellModal.value = false
      }
    }

    const refreshPricing = async() => {
      try {
        await refreshPrices(route.params.symbol, 'USD')
        await assignPriceHistory()
        toast({
          message: 'Prices updated',
          type: 'is-success',
          position: 'top-right'
        })
      } catch (e) {
        toast({
          message: 'Price update too soon',
          type: 'is-danger',
          position: 'top-right'
        })
      }
    }

    return {
      company,
      transactions,
      canSellShares,
      formatDate,
      priceHistory,
      formatColor,
      showBuyModal,
      showSellModal,
      toggleModal,
      determineTransactionType,
      sharesToBuy,
      sharesToSell,
      purchase,
      sell,
      currencies,
      currencyToBuy,
      refreshPricing
    }
  }  
}
</script>