<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';
import type { PropType } from 'vue';


defineProps({
    board: {
        type: {} as PropType<components['schemas']["BoardRead"]>,
        required: true
    }
})

const open = defineModel<boolean>('open', {default: false})
defineEmits(['delete'])



</script>


<template>
    <UIDeleteModal v-model:open="open" :item="$props.board" :title="'Delete ' + board.title" url="/api/v1/boards/{board_id}" :path="{board_id: $props.board.id}" :button="{class: 'hidden'}" @delete="$emit('delete', $event)">
        <template #body>
            <p class="font-bold text-2xl">Are you shure you want delete <span class="text-error">{{ board.title }}</span> board?</p>
        </template>
    </UIDeleteModal>
</template>