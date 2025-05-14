<script setup lang="ts">
import { UButton, UIcon } from '#components'
import type { paths } from '#nuxt-api-party/backend'
import type { PropType } from 'vue'


const props = defineProps({
    original: {
        type: [String,Number,Boolean],
        default: null
    },
    component: {
        type: String as () => 'UInput' | 'UTextarea' | 'USwitch' | 'UIDateTimePicker',
        default: 'UInput'
    },
    componentProps: {
        type: {} as PropType<object>,
        default: {}
    },
    url: {
        type: String as () => keyof paths,
        required:true
    },
    name: {
        type: String,
        required: true
    },
    path: {
        type: {} as PropType<object>,
        default: {}
    },
    query:{
        type: {} as PropType<object>,
        default: {}
    },
    helperButton:{
        type: Boolean,
        default: false
    }
})


const edit = ref(false)
const model = defineModel({default: ''})
const fieldRef = useTemplateRef<HTMLInputElement>('input')
const emit = defineEmits(['edited'])


const submit = async () => {
    if(model.value != props.original){
        try{
            const response = await $backend(props.url, {
                method: "PATCH",
                path: props.path,
                query: props.query,
                body:{
                    [props.name]: model.value
                }
            })
            model.value = response[props.name]
            edit.value = false
            emit('edited', response)
        }catch(error){
            backendError(error)
            model.value = JSON.parse(JSON.stringify(props.original))
            edit.value = false
        }
    }else{
        model.value = JSON.parse(JSON.stringify(props.original))
        edit.value = false
    }
}


watch(edit, () => {
    if(edit.value){
        setTimeout(()=>fieldRef.value?.inputRef?.focus(),0)     
    }
})

const resolvedComponent = computed(()=> {
    switch(props.component){
        case 'UInput':
            return resolveComponent("UInput");
        case 'UTextarea':
            return resolveComponent('UTextarea');
        case 'USwitch':
            return resolveComponent("USwitch");
        case 'UIDateTimePicker':
            return resolveComponent('UIDateTimePicker')
        default:
            return resolveComponent("UInput");
    }

})


</script>

<template>
    <div v-if="!edit" class="group flex flex-row cursor-pointer gap-1 justify-start items-center" >
        <UIcon name="i-heroicons-pencil-square" class="group-hover:flex group-hover:text-primary-500" @click="edit = true"/>
        <slot name="preview" :state="model">
            <p class="text-lg" >{{ model || '---' }}</p>
        </slot>
        
    </div>
    
    <div v-else class="flex flex-row justify-between items-center gap-2">
        <component :is="resolvedComponent" ref="input" v-bind="props.componentProps"  v-model="model" class="w-full" @blur="submit" @keyup.enter="submit" @keyup.esc="submit" />
        <UButton v-if="$props.helperButton" size="sm" leading-icon="i-heroicons-check" @click="submit"/>
    </div>
    
</template>