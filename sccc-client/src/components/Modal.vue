<template>
  <div class="modal is-clipped" :class="{'is-active': active }">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <slot name="title">Buy Shares</slot>
      </header>
      <section class="modal-card-body">
        <slot></slot>
      </section>
      <footer class="modal-card-foot">
        <slot name="footer"></slot>
        <button class="modal-close is-large" aria-label="close" @click="closeCallback">
          Close
        </button>
      </footer>
    </div>
   </div>
</template>

<script>
export default {
  props: {
    active: {
      type: Boolean,
      default: false
    },
    closeCallback: Function
  }
}
</script>