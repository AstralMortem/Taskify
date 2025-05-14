<script setup lang="ts">
const route = useRoute()

const {data, status, error} = await useBackendData('/api/v1/boards/public/{board_hash}', {
    path:{
        board_hash: route.params.hash as string
    }
})

onMounted(()=>{
    useBoardPermission().value = 'read'
})

definePageMeta({
    layout: 'simple'
})

</script>


<template>
    <BoardCard v-model="data" v-if="status === 'success'"/>
    <UICard class="w-full" v-else-if="status === 'pending'">
        <USkeleton class="w-full h-full"/>
    </UICard>    
    <UICard class="w-full items-center flex-col gap-2 justify-center flex text-center" v-else>
        <p class="font-bold text-2xl text-error">{{ error?.data.title }}</p>
        <p class="font-bold text-error">{{ error?.data.description }}</p>
        <UButton to="/" label="Go Home" variant="outline"/>
    </UICard>
</template>