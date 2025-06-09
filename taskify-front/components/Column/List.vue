<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';
import draggable from 'vuedraggable'
import { useInfiniteScroll } from '@vueuse/core'
import type { PropType } from 'vue';

const props = defineProps({
    board: {
        type: {} as PropType<components["schemas"]["BoardRead"]>,
        required: true
    }
})

const route = useRoute()

const lists = ref<Array<components["schemas"]["ListRead"]>>([])
const size = ref(10)
const page = ref(1)
const pages = ref(1)


const fetchLists = async () => {
    try{
        let response = {} as components["schemas"]["Page_ListRead_"]
        if(route.fullPath.includes('/public')){
            response = await $backend('/api/v1/lists/board/public/{board_hash}', {
                path: {
                    board_hash: route.params.hash as string
                },
                query: {
                    size: size.value,
                    page: page.value
                },
                cache: false,
            })
        }else{
            response = await $backend('/api/v1/lists/board/{board_id}', {
                path: {
                    board_id: props.board.id,
                },
                query: {
                    size: size.value,
                    page: page.value
                },
                cache: false,
            })
        }
        

        lists.value = [...lists.value, ...response.items]
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
        await fetchLists()
    },{
        distance: size.value,
        direction: 'right',
        canLoadMore: () => page.value <= pages.value
    })

const updateList = (newList: components['schemas']["ListRead"]) => {
    const idx = lists.value.findIndex(i => i.id == newList.id)
    if(idx >= 0) {
        lists.value[idx] = newList
    }
}

const deleteList = (oldList: components["schemas"]["ListRead"]) => {
    lists.value = lists.value.filter(x => x.id !== oldList.id)
}

const reorderLists = async (newList: Array<components["schemas"]['ListRead']>) => {
    try{
        const response = await $backend('/api/v1/lists/board/{board_id}/reorder', {
            method: 'POST',
            path:{
                board_id: props.board.id
            },
            body: newList.map(i => i.id),
            query: {
                size: size.value,
                page: 1
            }
        })

        lists.value = response.items
        size.value = response.size || 10
        page.value = response.page || 1
        pages.value = response.pages || 1
        page.value += 1
        
    }catch(error){
        backendError(error)
    }

}

const computedLists = computed({
    get(){
        return lists.value
    },
    async set(value){
        if(useBoardPermission().value == 'full' || useBoardPermission().value == 'edit'){
            await reorderLists(value)
        }
    }
})


</script>


<template>
    <div class="overflow-auto w-full md:max-w-[60vw] h-full">
        <draggable ref="el" v-model="computedLists" group="lists" item-key="id" class="flex flex-col md:flex-row gap-4 pb-6" ghost-class="ghost">
            <template #item="{element}">
                <ColumnCard :list="element" :board="$props.board" @update="updateList" @delete="deleteList"/> 
            </template>
            <template #footer>
                <ColumnAdd v-if="useBoardPermission().value == 'full' || useBoardPermission().value == 'edit'" :board="$props.board" :last-position="lists.length" @add="lists.push($event)"/>
            </template>
        </draggable>
        
    </div>
</template>

<style>
.ghost {
  background-color: var(--color-neutral-400);
  opacity: 0.4;
}
</style>