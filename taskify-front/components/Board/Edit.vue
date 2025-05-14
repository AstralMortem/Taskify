<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';
import type { ButtonProps } from '@nuxt/ui';
import type { PropType } from 'vue';
import { z } from 'zod';

const openModal = defineModel({default: false})

defineProps({
    board: {
        type: {} as PropType<components["schemas"]["BoardRead"]>,
        required: true
    }
})

const schema = z.object({
    title: z.string().optional(),
    description: z.string().optional(),
    background: z.string().optional()
})

defineEmits(['submit'])

</script>

<template>
    <UIModalForm 
    v-model:open="openModal" 
    title="Edit Board" 
    url="/api/v1/boards/{board_id}" 
    method="PATCH" 
    :button="{
       class: 'hidden'
    }"
    :path="{board_id:$props.board.id}" 
    :schema="schema" 
    :original-state="$props.board"
    @submit="$emit('submit', $event)"
    >
        <template #form="{formState}">
            <UFormField label="Title" name="title">
                <UInput v-model="formState.title" placeholder="like 'My Board'" class="w-full"/>
            </UFormField>
            <UFormField label="Description" name="description">
                <UTextarea v-model="formState.description" placeholder="like: 'This is my board'" class="w-full"/>
            </UFormField>
            <UFormField label="Background Color" name="background">
                <UIColorPicker v-model="formState.background"/>
            </UFormField>
        </template> 
    </UIModalForm>
</template>