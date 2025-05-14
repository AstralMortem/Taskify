<script setup lang="ts">
import { UFormField } from '#components';
import z from 'zod'


defineProps({
    label: {
        type: String,
        default: ''
    }
})

const schema = z.object({
    title: z.string(),
    description: z.string().optional(),
    background: z.string().optional()
})

defineEmits(['submit'])

</script>

<template>
    <UIModalForm 
    title="Add Board"
    url="/api/v1/boards/"
    :schema="schema"
    :button="{
        label: $props.label,
        leadingIcon: 'i-heroicons-plus'
    }"

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