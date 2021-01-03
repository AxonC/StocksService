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
      </div>
    </div>
  </nav>
  <section class="section has-background-light" style="height: 100%;">
    <router-view></router-view>
  </section>
</template>

<script>
export default {
  name: 'App',
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
