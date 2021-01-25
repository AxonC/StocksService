<template>
  <div>
    <div>
      <h1 class="title">My Portfolio</h1>
      <table class="table is-fullwidth">
        <thead>
          <tr>
            <th>Company</th>
            <th>Shares Owned</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="owned in portfolio" :key="owned.company_symbol">
            <td>{{ owned.company_symbol }}</td>
            <td>{{ owned.shares_owned }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="mt-4">
      <h1 class="title">Available Shares</h1>
      <p class="subtitle">Shares are listed with their last price</p>
    </div>
    <div class="box">
      <h2 class="title-2">Search</h2>
      <div class="control">
        <input class="input" type="text" v-model="searchQuery" 
          placeholder="Fuzzy search of Company" />
      </div>
      <div class="control">
        <label for="">Price Low</label>
        <input type="text" class="input" v-model="priceQuery.low">
      </div>
      <div class="control">
        <label for="">Price High</label>
        <input type="text" class="input" v-model="priceQuery.high">
      </div>
      <div class="mt-3 has-text-right">
        <button class="button is-info" @click="resetSearch">Reset Search</button>
      </div>
    </div>
    <table class="table is-fullwidth">
      <thead>
        <tr>
          <th>Company Symbol</th>
          <th>Company Name</th>
          <th>Available Shares</th>
          <th>Last Updated</th>
          <th>Latest Price</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="company in filteredCompanies" :key="company.symbol">
          <td>{{ company.symbol }}</td>
          <td>{{ company.name }}</td>
          <td>{{ company.available_shares }}</td>
          <td>{{ formatDate(company.last_update) }}</td>
          <td>{{ company.last_price }} ({{ company.currency }})</td>
          <td>
            <router-link :to="{ name: 'Company', params: { symbol: company.symbol }}">
              View
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useCompanies } from '../library/companies'
import { format } from 'date-fns'
import { enGB } from 'date-fns/locale' 
import Fuse from 'fuse.js'
import { useAuth } from '../library/auth'
export default {
  setup() {
    const { 
      getCompanies,
      companies 
    } = useCompanies()
    const { user } = useAuth()
    const searchQuery = ref('')
    const priceQuery = ref({
      low: 0,
      high: 0
    })
    const formatDate = (date) => {
      return format(new Date(date), 'Pp', { locale: enGB })
    }
    const searchOptions = {
      keys: [
        'symbol',
        'name'
      ]
    }
    const filteredCompanies = computed(() => {
      let localCompanies = [...companies.value]
      if (priceQuery.value.low > 0) {
        localCompanies = localCompanies.filter(({ last_price }) => last_price > parseInt(priceQuery.value.low))
      }
      if (priceQuery.value.high > 0) {
        localCompanies = localCompanies.filter(({ last_price }) => last_price < parseInt(priceQuery.value.high))
      }
      if (searchQuery.value.length > 1) {
        const fuse = new Fuse(localCompanies, searchOptions)
        localCompanies = fuse.search(searchQuery.value).map(item => item.item)
      }
      return localCompanies
    })
    const resetSearch = () => {
      priceQuery.value = {low: 0, high: 0}
      searchQuery.value = ''
    }
    onMounted(getCompanies)
    onMounted(() => console.log(user.value))
    return {
      searchQuery,
      priceQuery,
      companies,
      formatDate,
      filteredCompanies,
      resetSearch,
      portfolio: computed(() => user.value.portfolio)
    }
  }
}
</script>