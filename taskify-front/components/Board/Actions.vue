<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';
import type { DropdownMenuItem } from '@nuxt/ui';
import type { PropType } from 'vue';


const props = defineProps({
    board: {
        type: {} as PropType<components["schemas"]["BoardRead"]>,
        required: true
    }
})

const authStore = useAuthStore()


const actions = ref<DropdownMenuItem[]>([{
    label: 'Edit',
    icon: 'i-heroicons-pencil-square',
    onSelect(e) {
        openEdit.value = true
    },
    color: 'primary',
    class: 'cursor-pointer'
},props.board.owner_id == authStore.user.id?{
    label: 'Delete',
    icon: 'i-heroicons-trash',
    color: 'error',
    onSelect(e) {
        openDelete.value = true
    },
    class: 'cursor-pointer'
}:''])



const openEdit = ref(false)
const openDelete = ref(false)

defineEmits(['update', 'delete'])

</script>


<template>
    <UDropdownMenu :items="actions" >
        <UButton icon="i-heroicons-ellipsis-horizontal" variant="ghost" size="lg"/>
    </UDropdownMenu>
    <BoardEdit  v-model:open="openEdit" :board="$props.board" @submit="$emit('update',$event)"/>
    <BoardDelete v-model:open="openDelete" :board="$props.board" @delete="$emit('delete', $event)"/>
</template>