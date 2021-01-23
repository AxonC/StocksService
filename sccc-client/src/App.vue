<template>
  <nav class="navbar" role="navigation">
    <div class="navbar-brand">
      <a class="navbar-item">Stock Management Portal</a>

      <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div id="navbarBasicExample" class="navbar-menu">
      <div class="navbar-start">
        <router-link class="navbar-item" to="/dashboard">
          Dashboard
        </router-link>
        <router-link class="navbar-item" to="/admin">
          Admin
        </router-link>
      </div>
    </div>
  </nav>
  <div class="container is-fullhd has-background-light">
    <section class="section" v-if="user.value">
      <div class="is-justify-content-flex-end is-flex is-flex-direction-column is-align-items-baseline">
        <span class="is-size-2">
          ${{ user.value.balance }}
        </span>
        <span class="is-size-4 is-uppercase is-italic has-text-weight-bold has-text-grey-light">
          Balance
        </span>
      </div>
    </section>
    <section class="section has-background-light" style="height: 100%;">
      <router-view></router-view>
    </section>
  </div>
</template>

<script>
import { useAuth } from './library/auth'
export default {
  name: 'App',
  setup() {
    const { user, isAuthenticated } = useAuth()
    return {
      user,
      isAuthenticated
    }
  }
}
</script>

<style>
#app {
  height: 100%;
  margin: 0; 
  display: flex;
  flex-direction: column;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
