<script setup lang="ts">
import { TaskEdit, UICard } from '#components';
import type { components } from '#nuxt-api-party/backend';
import type { PropType } from 'vue';

defineProps({
    task: {
        type: {} as PropType<components["schemas"]["CardRead"]>,
        required: true
    },
    board: {
        type: {} as PropType<components["schemas"]["BoardRead"]>,
        required: true
    }
})

const editMode = ref(false)
defineEmits(['update', 'delete'])

</script>

<template>
    <UICard :without-paddings="true" rounded="10"  class="cursor-pointer" @click="editMode = !editMode">
        <UTooltip :text="$props.task.description">
            <div class="flex flex-row justify-between items-center">
                <div class="flex flex-row gap-1 justify-start items-center">
                    <!-- <UIcon name="i-heroicons-pencil-square" size="1em"/> -->
                    <p class="font-medium text-sm">{{ $props.task.title }}</p>
                </div>
                <UIcon name="i-heroicons-ellipsis-horizontal"/>
            </div>
        </UTooltip>
        
        <TaskEdit v-model:open="editMode" :task="$props.task" :board="$props.board" @update="$emit('update', $event)" @delete="$emit('delete', $event)"/>
    </UICard>
    
</template>