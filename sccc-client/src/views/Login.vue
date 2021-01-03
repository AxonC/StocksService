<template>
    <div class="container is-max-desktop">
        <h1 class="title">Login</h1>
        <form action="" @submit.prevent="submitForm">
            <div class="field">
                <label for="username" class="label">
                    Username
                </label>
                <div class="control">
                    <input type="text" class="input" v-model="form.username">
                </div>
            </div>
            <div class="field">
                <label for="password" class="label">
                    Password
                </label>
                <div class="control">
                    <input type="password" class="input" v-model="form.password">
                </div>
            </div>
            <button class="button is-primary" type="submit">Login</button>
        </form>
    </div>
</template>

<script>
import { ref } from 'vue'
import { useAuth } from '../library/auth'
export default {
  name: "Login",
  setup() {
    let form = ref({
      username: '',
      password: ''
    })
    const submitForm = async () => {
      const { login } = useAuth()
      login(form.value.username, form.value.password)
    }

    return {
      form,
      submitForm
    }
  }
}
</script>