<script setup lang="ts" generic="Z extends z.ZodRawShape, I extends components['schemas']">
import type { components, paths } from '#nuxt-api-party/backend';
import type { ButtonProps, FormSubmitEvent } from '@nuxt/ui';
import type { PropType } from 'vue';
import type z from 'zod';

const props = defineProps({
    url: {
        type: String as () => keyof paths,
        required: true
    },
    method: {
        type: String as () => 'POST' | 'GET' | 'PUT' | 'PATCH' | 'DELETE',
        default: 'POST'
    },
    title:{
        type: String,
        required:true
    },
    description: {
        type: String,
        default: ''
    },
    button: {
        type: {} as PropType<ButtonProps>,
        default: {
            label: 'Open'
        }
    },
    schema: {
        type: {} as PropType<z.ZodObject<Z>>,
        required: true
    },
    query: {
        type: {} as PropType<object>,
        default: {}
    },
    path: {
        type: {} as PropType<object>,
        default: {}
    },
    responseFormatter: {
        type: Function,
        default: (payload: any) => payload
    },
    originalState: {
        type: {} as PropType<object>,
        default: {}
    }

})

type Schema = z.output<typeof props.schema>

const submit = async (event: FormSubmitEvent<Schema>) => {
    try{
        console.log(event.data)
        const response = await $backend(props.url, {
            method: props.method,
            query: props.query,
            path: props.path,
            body: event.data
        })
        console.log(response)

        const parserResponse = props.responseFormatter(response) 
        emit('submit', parserResponse)
        modalOpen.value = false

    }catch(error){
        backendError(error)
        emit('error', error)
    }
}

const reset = () => {
    if(props.originalState){
        formState.value = JSON.parse(JSON.stringify(props.originalState))
    }else{
        formState.value = {}
    }
    emit('reset')

}

const formState = ref<Schema>(props.originalState?JSON.parse(JSON.stringify(props.originalState)):{})
const modalOpen = defineModel<boolean>('open', {default: false})
const formRef = useTemplateRef('form')
const emit = defineEmits(["submit", 'close', 'open', 'reset', 'error'])

watch(modalOpen, ()=>{
    if(!modalOpen.value){
        reset()
        emit('close')
    }else{
        emit('open')
    }
})

const isSubmitDisabled = computed(()=> JSON.stringify(formState.value) == JSON.stringify(props.originalState))

</script>


<template>
    <UModal v-model:open="modalOpen" :title="$props.title" :description="$props.description">
        <slot name="label" v-bind="{formRef, formState, title: $props.title}">
            <UButton v-bind="$props.button" />
        </slot>
        <template #body>
            <slot name="body" v-bind="{formRef, formState}">
                <UForm ref="form" class="space-y-4" :state="formState" :schema="$props.schema" @submit.prevent="submit">
                    <slot name="form" v-bind="{formRef, formState}"/>
                </UForm>
            </slot>
        </template>
        <template #footer>
            <slot name="footer" v-bind="{formRef, formState, submit, reset, originalState: props.originalState}">
                <div class="flex flex-row justify-start items-center gap-3">
                    <UButton v-if="!Object.keys(props.originalState).length" label="Save" color="success" @click="formRef?.submit()"/>
                    <UButton v-else label="Save" color="success" :disabled="isSubmitDisabled" @click="formRef?.submit()"/>
                    <UButton label="Clear" color="warning" variant="outline" @click="reset"/>
                </div>
            </slot>
        </template>
    </UModal>
</template>