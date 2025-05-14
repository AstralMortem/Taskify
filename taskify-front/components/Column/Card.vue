<script setup lang="ts">
import { TaskList, UButton } from '#components';
import type { components } from '#nuxt-api-party/backend';
import type { PropType } from 'vue';


const props = defineProps({
    list: {
        type: {} as PropType<components["schemas"]["ListRead"]>,
        required: true
    },
    board: {
        type: {} as PropType<components["schemas"]["BoardRead"]>,
        required: true
    }
})

const editMode = ref(false)
const title = ref(props.list.title)
const titleRef = useTemplateRef('titleRef')
const emit = defineEmits(['update', 'delete'])

const update = async () => {
    if(title.value != props.list.title){
        try{
            const response = await $backend('/api/v1/lists/{list_id}', {
                method: 'PATCH',
                path: {
                    list_id: props.list.id
                },
                body: {
                    title: title.value
                }
            })
            emit('update', response)
            title.value = response.title
        }catch(error){
            backendError(error)
        }  
    }
    editMode.value = false
}

watch(editMode, ()=> {
    title.value = props.list.title
    if(editMode.value){
        setTimeout(() => titleRef.value?.inputRef?.focus(), 0)
    }
})

</script>

<template>
    <UICard class="w-full h-full min-w-[200px]" rounded="2xl" :background="$props.board.background?hexToRGBA($props.board.background, 0.8):'#DBEAFE'">
        <div class="flex flex-col gap-4">
            <div class="flex flex-row justify-between items-center gap-2">
                <p v-if="!editMode" class="font-bold text-base hover:cursor-pointer" :class="[$props.board.background?'hover:text-white':'hover:text-primary-500']" @dblclick="(useBoardPermission().value == 'full' || useBoardPermission().value == 'edit')?editMode = true:editMode = false">{{ title }}</p>
                <UInput v-else ref="titleRef" v-model="title" @blur="update" @keyup.enter="update"/>
                <ColumnDelete v-if="useBoardPermission().value == 'full'" :list="$props.list" @delete="$emit('delete', $event)"/>
            </div>
            <TaskList :list="$props.list" :board="$props.board"/>
        </div>
    </UICard>

</template>