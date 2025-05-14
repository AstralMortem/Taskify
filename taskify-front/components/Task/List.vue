<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';
import type { PropType } from 'vue';
import draggable from 'vuedraggable'
import { useInfiniteScroll } from '@vueuse/core'
import { TaskCard } from '#components';

const props = defineProps({
    board: {
        type: {} as PropType<components["schemas"]["BoardRead"]>,
        required:true
    },
    list: {
        type: {} as PropType<components["schemas"]["ListRead"]>,
        required: true
    }
})

const tasks = ref<Array<components["schemas"]["CardRead"]>>([])
const size = ref(10)
const page = ref(1)
const pages = ref(1)

const route = useRoute()

const fetchTasks = async () => {
    try{
        let response = {} as components['schemas']["Page_CardRead_"]
        if(route.fullPath.includes('/public')){
            response = await $backend('/api/v1/cards/list/{list_id}/public/{board_hash}', {
                path: {
                    list_id: props.list.id,
                    board_hash: route.params.hash as string
                },
                query: {
                    size: size.value,
                    page: page.value
                },
                cache: false,
            })
        }else{
            response = await $backend('/api/v1/cards/list/{list_id}', {
                path: {
                    list_id: props.list.id,
                },
                query: {
                    size: size.value,
                    page: page.value
                },
                cache: false,
            })
        }
        

        tasks.value = [...tasks.value, ...response.items]
        size.value = response.size || 10
        page.value = response.page || 1
        pages.value = response.pages || 1
        page.value += 1

    }catch(error){
        backendError(error)
    }
}

const el = useTemplateRef<HTMLElement>('el')

useInfiniteScroll(el, async() => {
        await fetchTasks()
    },{
        distance: size.value,
        canLoadMore: () => page.value <= pages.value
    })


const reorderTasks = async (list_id: string) => {
    try{
        const response = await $backend('/api/v1/cards/list/{list_id}/reorder', {
            method: 'POST',
            path: {
                list_id: list_id
            },
            body: tasks.value.map(c => c.id)
        })
        
        tasks.value = response.items
        page.value = response.page || 1
        pages.value = response.pages || 1
        size.value = response.size || 10
        page.value += 1

    }catch(error){
        backendError(error)
    }
}

const moveCard = async (card_id: string, old_list_id: string, new_list_id: string, new_position: number) => {
    try{
        await $backend('/api/v1/cards/{card_id}/move', {
            method: 'post',
            path:{
                card_id: card_id
            },
            body: {
                target_list_id: new_list_id,
                position: new_position
            }
        })
        await reorderTasks(new_list_id)
        // await reorderTasks(old_list_id)
    }catch(error){
        backendError(error)
    }
}


const change = async (e) => {
    if(useBoardPermission().value == 'full' || useBoardPermission().value == 'edit'){
        if(e.moved){
            await reorderTasks(props.list.id)
        }else if(e.added){
            await moveCard(e.added.element.id, e.added.element.list_id, props.list.id, e.added.newIndex)
        }
    }
    
}

const updateTask = (newTask: components["schemas"]["CardRead"]) => {
    const idx = tasks.value.findIndex(i => i.id == newTask.id)
    if(idx >= 0){
        tasks.value[idx] = newTask
    }
}

const deleteTask = (oldTask: components["schemas"]["CardRead"]) => {
    tasks.value = tasks.value.filter(i => i.id !== oldTask.id)
}


</script>

<template>
    <div class="overflow-y-auto h-max max-h-[53vh]">
        <draggable ref="el" v-model="tasks" group="cards" item-key="id" class="flex flex-col gap-1 px-1" ghost-class="ghost" @change="change" >
        <template #item="{element}"> 
            <TaskCard :task="element" :board="$props.board" @update="updateTask" @delete="deleteTask"/>
        </template>
        <template #footer>
            <TaskAdd v-if="useBoardPermission().value == 'full' || useBoardPermission().value == 'edit'" :board="$props.board" :list="$props.list" @add="tasks.push($event)"/>
        </template>
    </draggable>
    </div>
    
</template>