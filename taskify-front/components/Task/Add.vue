<script setup lang="ts">
import { UButton } from '#components';
import type { components } from '#nuxt-api-party/backend';
import type { Prop, PropType } from 'vue';


const props = defineProps({
    board: {
        type: {} as PropType<components["schemas"]["BoardRead"]>,
        required: true
    },
    list: {
        type: {} as PropType<components["schemas"]["ListRead"]>,
        required: true
    }
})

const cards = defineModel<Array<components["schemas"]["CardRead"]>>({default: []})
const title = ref('')
const titleRef = useTemplateRef('titleRef')
const addMode = ref(false)

const emit = defineEmits(['add'])

watch(addMode, ()=>{
    if(addMode.value){
        setTimeout(() => titleRef.value?.inputRef?.focus(), 0)
    }
})

const add = async () => {
    if(title.value){
        try{
        const response = await $backend('/api/v1/cards/list/{list_id}', {
            method: 'POST',
            body:{
              title: title.value,
              position:  cards.value.length,
              description: '',
              is_completed: false
            },
            path: {
                list_id: props.list.id
            }
        })

        emit('add', response)

        }catch(error){
            backendError(error)
        }
    }
    addMode.value = false
    title.value = ''
}


</script>


<template>
    <div class="w-full mt-3">
        <UICard v-if="addMode" :without-paddings="true" rounded="10" :background="'#FFFFFF'">
            <UInput ref="titleRef" v-model="title" placeholder="Set title to your column" @blur="add" @keyup.enter="add"/>
        </UICard>
        <UButton v-else label="Add Card" variant="outline" :color="$props.board.background?'neutral':'primary'" block @click="addMode = true"/>
    </div>
</template>