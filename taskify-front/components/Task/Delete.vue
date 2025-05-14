<script setup lang="ts">
import { UIDeleteModal } from '#components';
import type { components } from '#nuxt-api-party/backend';
import type { PropType } from 'vue';

defineProps({
    task:{
        type: {} as PropType<components["schemas"]["CardRead"]>,
        required:true
    }
})

defineEmits(['delete'])

</script>

<template>
    <UIDeleteModal 
        :title="'Delete ' + $props.task.title" 
        :item="$props.task" 
        url="/api/v1/cards/{card_id}" 
        :path="{card_id:$props.task.id}" 
        :button="{
            color: 'error',
            label: 'Delete'
        }"
        @delete="$emit('delete',$event)">
        <template #body>
            <p class="font-bold text-2xl">Are you shure you want delete <span class="text-error">{{ $props.task.title }}</span> task?</p>
            
        </template>
    </UIDeleteModal>
</template>