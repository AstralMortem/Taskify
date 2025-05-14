<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend'

const boardStore = useJoinedBoardsStore()
const route = useRoute()

const currentBoardModel = computed({
    get(){
        return boardStore.currentBoard
    },
    set(value: components["schemas"]["BoardRead"]){
        const idx = boardStore.boards.findIndex(i => i.id === boardStore.currentBoardId)
        if(idx >=0){
            boardStore.boards[idx] = value
        }
    }
})


onMounted(()=> {
    boardStore.setBoardId(route.params.id as string)
    useBoardPermission().value = 'edit'
})

definePageMeta({
    authRequired: true
})

</script>

<template>
    <BoardCard v-if="currentBoardModel" v-model="currentBoardModel"/>
    <UICard v-else class="w-full min-h-[30vh] flex justify-center items-center">
        <p class="font-bold text-center">Not Allowed</p>
    </UICard>
</template>