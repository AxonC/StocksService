<template>
  <div>
    <table class="table">
      <thead>
        <tr>
          <th>Company Symbol</th>
          <th>Company Name</th>
          <th>Available Shares</th>
          <th>Last Updated</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="company in companies" :key="company.symbol">
          <th>{{ company.symbol }}</th>
          <th>{{ company.name }}</th>
          <th>{{ company.available_shares }}</th>
          <th>{{ company.last_update }}</th>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useCompanies } from '../library/companies'
export default {
  setup() {
    const { 
      getCompanies,
      companies 
    } = useCompanies()
    onMounted(getCompanies)
    return {
      companies
    }
  }
}
</script>