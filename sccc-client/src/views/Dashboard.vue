<template>
  <div>
    <h1 class="title">Available Shares</h1>
    <p class="subtitle">Shares are listed with their last price</p>
    <div class="box">
      <h2 class="title-2">Search</h2>
      <div class="control">
        <input class="input" type="text" v-model="searchQuery" 
          placeholder="Fuzzy search of Company" />
      </div>
      <div class="control">
        <label for="">Price</label>
        <input type="text" class="input" v-model="priceQuery">
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
export default {
  setup() {
    const { 
      getCompanies,
      companies 
    } = useCompanies()
    const searchQuery = ref('')
    const priceQuery = ref(0)
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
      if (searchQuery.value.length > 1) {
        const fuse = new Fuse(companies.value, searchOptions)
        return fuse.search(searchQuery.value).map(item => item.item)
      }
      return companies.value
    })
    onMounted(getCompanies)
    return {
      searchQuery,
      priceQuery,
      companies,
      formatDate,
      filteredCompanies
    }
  }
}
</script>