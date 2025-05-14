<script setup lang="ts">
import { TaskDelete, UIDateTimePicker, UIModalForm, UserAssignSelect, USwitch, UTextarea } from '#components';
import type { components } from '#nuxt-api-party/backend';
import type { PropType } from 'vue';
import { z } from 'zod';


const props = defineProps({
    task: {
        type: {} as PropType<components["schemas"]["CardRead"]>,
        required:true
    },
    board: {
        type: {} as PropType<components["schemas"]["BoardRead"]>,
        required:true
    }
})

defineEmits(['update', 'delete'])

const schema = z.object({
    title: z.string().optional(),
    description: z.string().optional(),
    is_completed: z.boolean().default(false),
    due_date: z.string().nullable().optional(),
    assigned_to_id: z.string().optional()

})


const open = defineModel<boolean>('open',{default: false})

const members = computed(()=> [...props.board.members, props.board.owner])

</script>


<template>
    <UIModalForm
    v-model:open="open" title="Edit Task" url="/api/v1/cards/{card_id}" method="PATCH" :path="{card_id: $props.task.id}" :original-state="$props.task" 
    :schema="schema" 
    :button="{class:'hidden'}" 
    @submit="$emit('update', $event)">
        <template #form="{formState}">
            <UFormField label="Title" name="title">
                <UInput v-model="formState.title" class="w-full"/>
            </UFormField>
            <UFormField label="Description" name="description">
                <UTextarea v-model="formState.description" class="w-full"/>
            </UFormField>
            <UFormField label="Is Completed" name="is_completed">
                <USwitch v-model="formState.is_completed"/>
            </UFormField>
            <UFormField label="Due To" name="due_date">
                <UIDateTimePicker v-model="formState.due_date"/>
            </UFormField>
            <UFormField label="Assing To" name="assign_to_id">
                <UserAssignSelect v-model="formState.assigned_to_id" :members="members"/>
            </UFormField>

        </template>

        <template #footer="{formRef, reset, originalState, formState}">
            <div v-if="useBoardPermission().value == 'full' || useBoardPermission().value == 'edit'" class="flex flex-row justify-between items-center w-full">
                <div class="flex flex-row justify-start items-center gap-3">
                    <UButton label="Save" color="success" :disabled="JSON.stringify(formState) == JSON.stringify(originalState)" @click="formRef?.submit()"/>
                    <UButton label="Clear" color="warning" variant="outline" @click="reset"/>
                </div>
                <TaskDelete v-if="useBoardPermission().value == 'full'" :task="$props.task" @delete="$emit('delete', $event)"/>
            </div>
            <div v-else></div>
        </template>
    </UIModalForm>
</template>