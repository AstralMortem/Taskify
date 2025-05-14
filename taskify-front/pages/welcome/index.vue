<script setup lang="ts">
const {init} = useWelcome()

onMounted(()=> init())

</script>

<template>
    <p>Welcome</p>
</template>