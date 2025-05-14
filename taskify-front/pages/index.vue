<script setup lang="ts">
definePageMeta({
    authRequired: true
})

const boardStore = useBoardStore()
const {boards} = storeToRefs(boardStore)

const joinedBoardStore = useJoinedBoardsStore()
const {boards: joinedBoards} = storeToRefs(joinedBoardStore)

</script>

<template>
    <UICard rounded="4xl" class="w-full">
        <div class="flex flex-col gap-4">
            <div class="flex flex-col gap-4">
                <p class="font-bold text-2xl">My Boards</p>
                <USeparator/>
                <div v-if="boards.length" class="grid lg:grid-cols-4 md:grid-cols-3 gap-4">
                    <ULink v-for="board in boards" :key="board.id" :to="'/boards/' + board.id" class="cursor-pointer group text-center">
                        <UICard class="w-full bg-primary-50 group-hover:bg-primary-100" rounded="2xl" >
                            <p class="font-bold text-lg">{{ board.title }}</p>
                        </UICard>
                    </ULink>
                </div>
                <div v-else class="flex justify-center items-start pt-20">
                    <BoardAdd label="Add Board" @submit="boardStore.addBoard"/>
                </div>
            </div>

            

            <div class="flex flex-col gap-4">
                <p class="font-bold text-2xl">Joined Boards</p>
                <USeparator/>
                <div class="grid lg:grid-cols-4 md:grid-cols-3 gap-4">
                    <ULink v-for="board in joinedBoards" :key="board.id" :to="'/boards/member/' + board.id" class="cursor-pointer group text-center">
                        <UICard class="w-full bg-primary-50 group-hover:bg-primary-100" rounded="2xl">
                            <p class="font-bold text-lg">{{ board.title }}</p>
                        </UICard>
                    </ULink>
                </div>
            </div>
            
        </div>
    </UICard>
</template>