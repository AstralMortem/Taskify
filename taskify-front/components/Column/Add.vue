<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend'
import type { PropType } from 'vue'


const props = defineProps({
    board: {
        type: {} as PropType<components["schemas"]["BoardRead"]>,
        required: true
    },
})

const lists = defineModel<Array<components["schemas"]["ListRead"]>>({default:[]})

const emit = defineEmits(['add'])

const addMode = ref(false)
const title = ref('')
const titleRef = useTemplateRef('titleRef')

watch(addMode, ()=>{
    if(addMode.value){
        setTimeout(() => titleRef.value?.inputRef?.focus(), 0)
    }
})


const add = async () => {
    if(title.value){
        try{
        const response = await $backend('/api/v1/lists/board/{board_id}', {
            method: 'POST',
            body:{
              title: title.value,
              position:  lists.value.length
            },
            path: {
                board_id: props.board.id
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
    <div class="w-full">
        <UICard v-if="addMode" rounded="2xl" class="min-w-[200px]" :background="$props.board.background?hexToRGBA($props.board.background, 0.8):'#DBEAFE'">
            <UInput ref="titleRef" v-model="title" placeholder="Set title to your column" @blur="add" @keyup.enter="add"/>
        </UICard>
        <div v-else class="border-2 rounded-2xl h-fit w-max p-4 text-neutral-600 border-dashed hover:bg-white/50 hover:text-black cursor-pointer" @click="addMode = true">
            <p class="font-bold">+ Add Column</p>
        </div>
    </div>
    
</template>