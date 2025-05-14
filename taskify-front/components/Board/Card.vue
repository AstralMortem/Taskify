<script setup lang="ts">
import { BoardMembers, ColumnList } from '#components'
import type { components } from '#nuxt-api-party/backend'
import type { PropType } from 'vue'





const board = defineModel<components["schemas"]["BoardRead"]>({default:{}})



</script>


<template>
    <UICard rounded="4xl" class="w-full" :background="board.background?hexToRGBA(board.background, 0.6):''">
        <div class="flex flex-col gap-6 w-full">
            <div class="flex flex-row justify-between items-center border-b-[1px] border-neutral-200 py-4">
                <div class="flex flex-row gap-1 justify-start items-center">
                    <p class="font-bold text-2xl">{{ board.title }}</p>
                    <UPopover v-if="board.description" mode="hover">
                        <UIcon name="i-heroicons-information-circle" class="text-primary cursor-pointer"/>
                        <template #content>
                            <div class="p-2">
                                <p>{{ board.description }}</p>
                            </div>
                        </template>
                    </UPopover>
                </div>
                <BoardMembers v-model="board" @update="board = $event"/>
                
            </div>
            <ColumnList :board="board"/>
        </div>
    </UICard>
</template>