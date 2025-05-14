<script setup lang="ts">
import { UIDeleteModal } from '#components';
import type { components } from '#nuxt-api-party/backend';
import type { PropType } from 'vue';

defineProps({
    list:{
        type: {} as PropType<components["schemas"]["ListRead"]>,
        required:true
    }
})

defineEmits(['delete'])

</script>

<template>
    <UIDeleteModal 
        :title="'Delete ' + $props.list.title" 
        :item="$props.list" 
        url="/api/v1/lists/{list_id}" 
        :path="{list_id:$props.list.id}" 
        :button="{
            icon: 'i-heroicons-trash',
            color: 'neutral',
            variant: 'link',
            ui: {
                leadingIcon: 'font-bold text-lg'
            }
        }"
        @delete="$emit('delete',$event)">
        <template #body>
            <p class="font-bold text-2xl">Are you shure you want delete <span class="text-error">{{ $props.list.title }}</span> column?</p>
            
        </template>
    </UIDeleteModal>
</template>