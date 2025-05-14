<script setup lang="ts">

</script>

<template>
  <div class="w-screen h-full min-h-screen  overflow-x-clip fixed bg-neutral-100 overflow-y-scroll">
    <img src="/img/left_banner.svg" alt="left-banner" class="absolute top-[20%] -left-[12%]">
    <img src="/img/right_banner.svg" alt="right-banner" class="absolute top-[20%] -right-[12%]">
    <div class="w-full h-full flex flex-col">
      <NavTopBar/>
      <div class="w-full h-full flex flex-row justify-center items-start  mt-8 ">
        <slot/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>