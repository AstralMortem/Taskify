<script setup lang="ts">
import type { paths } from '#nuxt-api-party/backend';
import type { ButtonProps } from '@nuxt/ui';
import type { PropType } from 'vue';


const props = defineProps({
    title: {
        type: String,
        default: 'Delete Item'
    },
    url: {
        type: String as () => keyof paths,
        required: true
    },
    description: {
        type: String,
        default: undefined
    },
    item: {
        type: {} as PropType<object>,
        default: {}
    },
    button: {
        type: {} as PropType<ButtonProps>,
        default: {
            label: 'Delete',
            color: 'error'
        }
    },
    path: {
        type: {} as PropType<object>,
        default: {}
    },
    query: {
        type: {} as PropType<object>,
        default: {}
    }
})

const emit = defineEmits(['delete', 'closed', 'open'])
const open = defineModel<boolean>('open', {default: false})

const sumbit = async () => {
    try{
        const response = await $backend(props.url, {
            method: 'DELETE',
            path: props.path,
            query: props.query
        })

        if(response){
            emit('delete', response)
        }else{
            emit('delete', props.item)
        }

        open.value = false

    }catch(error){
        backendError(error)
    }
}

watch(open, () => {
    if(open.value){
        emit('open')
    }else{
        emit('closed')
    }
})


</script>


<template>

    <UModal v-model:open="open" :title="$props.title" :description="$props.description">
        
        <slot name="label" v-bind="{item: $props.item, title: $props.title}">
            <UButton v-bind="$props.button" />
        </slot>

        <template #body>
            <slot name="body">
                <p v-if="props.description" class="text">{{ props.description }}</p>
            </slot>
        </template>

        <template #footer>
            <div class="flex flex-row justify-start items-center gap-3">
                <UButton label="Delete" color="error" @click="sumbit"/>
                <UButton label="Cancel" color="success" @click="open = false"/>
            </div>
        </template>
    </UModal>
</template>