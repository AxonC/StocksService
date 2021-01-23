<template>
  <div class="box">
    <h1 class="title">
      <slot name="title"></slot>
    </h1>
    <p class="subtitle">
      <slot name="subtitle"></slot>
    </p>
    <div>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {}
</script>