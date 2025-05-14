<script setup lang="ts">
definePageMeta({
    layout: 'auth'
})
const route = useRoute()
const authStore = useAuthStore()


onMounted(async () => {
    await authStore.OAuthLogin(route.params.provider as string as "github", route.query)
    if(authStore.isAuthenticated){
        navigateTo('/')
    }
})



</script>

<template>
<UIAuthCard>
    <p>Loading...</p>
</UIAuthCard>
</template>