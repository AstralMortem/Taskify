<script setup lang="ts">
defineProps({
  isDark: Boolean
})
</script>

<template>
<div class="flex flex-row gap-4 justify-center items-center text-primary-50">
  <img v-if="$props.isDark" src="/img/logo_primary.svg" alt="logo" >
  <img v-else src="/img/logo.svg" alt="logo">
  <p v-if="!Boolean($props.isDark)" class="text-3xl font-bold">Taskify</p>
</div>
</template>

<style scoped>

</style>