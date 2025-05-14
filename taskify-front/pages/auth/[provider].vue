<script setup lang="ts">
definePageMeta({
    layout: 'auth'
})
const route = useRoute()
const authStore = useAuthStore()
const boardStore = useBoardStore()


onMounted(async () => {
    await authStore.OAuthLogin(route.params.provider as string as "github", route.query)
    if(authStore.isAuthenticated){
        if(boardStore.boards.length >= 0){
            navigateTo('/boards/' + boardStore.boards[0].id)
        }else{
            navigateTo('/')
        }
    }
})



</script>

<template>
<UIAuthCard>
    <p>Loading...</p>
</UIAuthCard>
</template>