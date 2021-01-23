<template>
  <div>
    <modal :close-callback="toggleFormModal" :active="showFormModal">
      <template v-slot:title>Add Company</template>
      <template v-slot:default>
        <div class="control">
          <label for="">Company Symbol</label>
          <input type="text" class="input" v-model="company.symbol" /> 
        </div>
        <div class="control">
          <label for="">Company Name</label>
          <input type="text" class="input" v-model="company.name" />
        </div>
        <div class="control">
          <label for="">Available Shares</label>
          <input type="text" class="input" v-model="company.available_shares" />
        </div>
      </template>
      <template v-slot:footer>
        <button class="button is-success" @click="submit">
          Create Company
        </button>
      </template>
    </modal>
    <modal :close-callback="toggleAvailableSharesModal" :active="showActiveSharesModal">
      <template v-slot:title>Edit Available Shares for: {{ company.symbol }}</template>
      <template v-slot:default>
        <div class="control">
          <label for="">Available Shares</label>
          <input type="text" class="input" v-model="company.available_shares">
        </div>
      </template>
      <template v-slot:footer>
        <button class="button is-success" @click="modify">
          Modify Company
        </button>
      </template>
    </modal>
    <div class="is-flex is-justify-content-end mb-4">
      <button class="button is-primary" @click="toggleFormModal">Create Company</button>
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
        <tr v-for="company in companies" :key="company.symbol">
          <td>{{ company.symbol }}</td>
          <td>{{ company.name }}</td>
          <td>{{ company.available_shares }}</td>
          <td>{{ formatDate(company.last_update) }}</td>
          <td>{{ company.last_price }} ({{ company.currency }})</td>
          <td>
              <button class="button is-info" @click="toggleAvailableSharesModal(company.symbol, company.available_shares)">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import Modal from '../components/Modal'
import { useCompanies } from '../library/companies'
import { toast } from 'bulma-toast'
import { formatDate } from '../library/helpers'
export default {
  components: {
    Modal
  },
  setup() {
    const {
      getCompanies,
      companies,
      createCompany,
      modifyCompany
    } = useCompanies()
    const showFormModal = ref(false)
    const showActiveSharesModal = ref(false)
    const company = ref({
      symbol: '',
      available_shares: 0,
      name: ''
    })
    const toggleFormModal = () => {
      showFormModal.value = !showFormModal.value
    }
    
    const toggleAvailableSharesModal = (symbol, available_shares) => {
      if (symbol) {
        company.value.symbol = symbol
      }
      if (available_shares) {
        company.value.available_shares = available_shares
      }
      showActiveSharesModal.value = !showActiveSharesModal.value
    }

    const submit = async () => {
      await createCompany({
        name: company.value.name,
        symbol: company.value.symbol,
        available_shares: company.value.available_shares
      })
      toast({
        message: 'Company created',
        type: 'is-success',
        position: 'top-right'
      })
      showFormModal.value = false
      resetCompany()
    }

    const resetCompany = () => {
      company.value = {
        symbol: '',
        available_shares: 0,
        name: ''
      }
    }

    const modify = async () => {
      await modifyCompany(company.value.symbol, { available_shares: company.value.available_shares })
      toast({
        message: 'Modified shares',
        type: 'is-success',
        position: 'top-right'
      })
      resetCompany()
      await getCompanies()
      toggleAvailableSharesModal()
    }

    onMounted(getCompanies)

    return {
      companies,
      submit,
      showFormModal,
      showActiveSharesModal,
      toggleFormModal,
      company,
      formatDate,
      toggleAvailableSharesModal,
      modify
    }
  }
}
</script>