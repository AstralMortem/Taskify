<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend'
import type { DropdownMenuItem, NavigationMenuItem } from '@nuxt/ui'
import type { PropType } from 'vue'

const props = defineProps({
    label: {
        type: String,
        default: 'My Boards'
    },
    path: {
        type: String,
        default: '/boards/'
    }
})

const boards = defineModel<Array<components["schemas"]["BoardRead"]>>()


const items = computed<NavigationMenuItem[]>(() => {
    return [{
        label: props.label,
        type: 'label',
        slot: "board" as const,
        
        children: boards.value?.map((i) => {
            return {
                label: i.title,
                to: props.path + i.id,
                slot: i.id
            }
        })
    }] 
})

const expandedIdx = ref('0')

defineEmits(['update', 'delete'])

</script>

<template>
    <UNavigationMenu v-model="expandedIdx" :items="items" variant="link" orientation="vertical" :highlight="true" class="data-[orientation=vertical]:w-full"  >
        <template #board-label="{item}">
            <div class="w-full h-full cursor-row-resize"  @click="expandedIdx === '0'? expandedIdx = '99': expandedIdx= '0'">
                <p class="font-bold text-xl">{{ item.label }}</p>
            </div>
        </template>
        <template #board-trailing="{item}">
            <div class="flex felx-row justify-end items-center gap-2">
                <slot name="trailing" :item="item"/>
                <UIcon v-if="expandedIdx == '0'" name="i-heroicons-chevron-up" />
                <UIcon v-else name="i-heroicons-chevron-down"/>
            </div>
        </template>
        <template v-for="board in boards" :key="board.id" #[`${board.id}-trailing`]>
            <BoardActions :board="board" @update="$emit('update', $event)" @delete="$emit('delete', $event)"/>
        </template>
    </UNavigationMenu>
</template>