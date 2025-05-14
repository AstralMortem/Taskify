<script setup lang="ts">
import { storeToRefs, useAuthStore } from '#imports';
import type { components } from '#nuxt-api-party/backend';

const authStore = useAuthStore()
const {user} = storeToRefs(authStore)

const userNavItem = [[{
    label: 'Profile',
    to: '/auth/profile',
    icon: 'i-heroicons-user'
}],[{
    label: 'Log Out',
    icon: 'i-heroicons-arrow-left-start-on-rectangle',
    onSelect: async () => {
        await authStore.logout()
    },
    color: 'error'
}]]


const boardStore = useBoardStore()
const {boards} = storeToRefs(boardStore)

const joinedBoardsStore = useJoinedBoardsStore()

const {boards: joinedBoards} = storeToRefs(joinedBoardsStore)

onMounted(async ()=> {
    boardStore.fetchBoards()
    joinedBoardsStore.fetchBoards()
})





</script>


<template>
    <UICard rounded="4xl">
        <div class="flex flex-col gap-8">
            <UDropdownMenu :items="userNavItem">
                <UserAvatar :user="user"/>
            </UDropdownMenu>
            <div class="flex flex-col gap-2">
                <BoardList v-model="boards" @update="boardStore.updateBoard" @delete="boardStore.deleteBoard">
                    <template #trailing>
                        <BoardAdd @submit="boardStore.addBoard"/>
                    </template>
                </BoardList>
                <BoardList v-model="joinedBoards" label="Joined Boards" path="/boards/member/" @update="joinedBoardsStore.updateBoard" @delete="joinedBoardsStore.deleteBoard" />
            </div>
        </div>
    </UICard>
</template>