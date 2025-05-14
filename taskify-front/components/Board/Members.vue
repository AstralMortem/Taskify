<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend'
import { useClipboard } from '@vueuse/core'

const authStore = useAuthStore()
const currentBoard = defineModel<components["schemas"]["BoardRead"]>({default: {}})
const emit = defineEmits(['update'])

const addMember = async (board_id: string, member_id: string) => {
    try{
        const newBoard = await $backend('/api/v1/boards/{board_id}/members/{member_id}', {
            method: 'POST',
            path: {
                board_id: board_id,
                member_id: member_id
            }
        })
        emit('update', newBoard)
        
    }catch(error){
        backendError(error)
    }
}

const removeMemeber = async (board_id: string, member_id: string) => {
    try{
        const newBoard = await $backend('/api/v1/boards/{board_id}/members/{member_id}', {
            method: 'DELETE',
            path: {
                board_id: board_id,
                member_id: member_id
            }
        })
        
        emit('update', newBoard)
    }catch(error){
        backendError(error)
    }
}

const members = computed({
    get(){
        return currentBoard.value?.members || []
    },
    async set(value){
        if(currentBoard.value.owner_id == authStore.user.id){
            const members = currentBoard.value?.members || []
            const added = value.filter(item => !members.includes(item))
            const removed = members.filter(item => !value.includes(item))

            if(added.length){
                await addMember(currentBoard.value.id, added[0].id)
            }else if(removed.length){
                await removeMemeber(currentBoard.value.id, removed[0].id)
            }
        }
        
    }
})

const searchTerm = ref('')


const {data, status} = await useBackendData('/api/v1/users/', {
    query: {
        email: searchTerm
    },
    watch: [searchTerm],
    cache: false,
    transform: (row) => {
        return row.items.filter(i => i.id != authStore.user.id).map(i => {
            return {
                ...i,
            }
        })
    }
})

const isPublicBoard = ref(currentBoard.value.is_public)

const changePublicity = async () => {
    try{
        const response = await $backend('/api/v1/boards/{board_id}/change_public', {
            method: 'PATCH',
            path:{
                board_id: currentBoard.value.id
            },
            body: {
                is_public: isPublicBoard.value
            }
        })
        emit('update', response)
    }catch(error){
        backendError(error)
    }
}


const publicLink = computed(()=> {
    if (import.meta.client) {
        return window.location.origin + `/public/${currentBoard.value.public_hash}`
  }

  const event = useRequestEvent()
  const host = getRequestHeader(event, 'host')
  const protocol = getRequestHeader(event, 'x-forwarded-proto') || 'http'
  return `${protocol}://${host}/public/${currentBoard.value.public_hash}`
})

const {copy} = useClipboard()

const copyLink = async () => {
    copy(publicLink.value)
    useToast().add({
        title: 'Public link copied',
        description: publicLink.value,
        color: 'success'
    })
}

</script>


<template>

    <UModal title="Board members">
        <UAvatarGroup :max="3" size="sm" class="cursor-pointer ">
            <UserPhoto :user="currentBoard.owner"/>
            <UAvatar v-for="member in members" :key="member.id" :alt="member.full_name || member.username || member.email"/>
        </UAvatarGroup>

        <template #body>
            <div class="flex flex-col gap-4">
                <p class="text-xl">Owner</p>
                <div class="flex flex-row justify-start items-center gap-4">
                    <UserPhoto size="2xl" :user="currentBoard.owner"/>
                    <div class="flex flex-col gap-0">
                        <p v-if="currentBoard.owner.full_name" class="font-semibold">{{ currentBoard.owner.full_name }}</p>
                        <p>{{ currentBoard.owner.email }}</p>
                    </div>
                    
                </div>
                <p class="text-xl">Members</p>
                <div v-if="useBoardPermission().value == 'full' || useBoardPermission().value == 'edit'" class="flex flex-col gap-4">
                    <UInputMenu 
                    v-model="members" 
                    v-model:search-term="searchTerm" 
                    label-key="email"
                    :items="data" 
                    :multiple="true" 
                    :filter-fields="['email', 'username', 'full_name']" 
                    :loading="status === 'pending'" >
                        <template #item-leading="{item}">
                            <UAvatar :src="item.avatar?'http://localhost:9000/' + item.avatar: null" :alt="item.full_name || item.username || item.email"/>
                        </template>
                    </UInputMenu>
                </div>
                <p v-if="useBoardPermission().value == 'full' || currentBoard.is_public" class="text-xl">Public Link</p>
                <div class="flex flex-col gap-2 items-start justify-start">
                    <USwitch v-if="useBoardPermission().value == 'full'" v-model="isPublicBoard" label="Make public" @change="changePublicity"/>

                    
                    <div v-if="currentBoard.is_public" class="flex flex-row gap-2 items-center justify-center ring-1 p-2 ring-neutral-400 rounded-lg">
                        <UButton icon="i-heroicons-clipboard" variant="soft" @click="copyLink"/>
                        <p>{{ publicLink }}</p>
                        
                    </div>
                </div>
            </div>
        </template>
    </UModal>
</template>