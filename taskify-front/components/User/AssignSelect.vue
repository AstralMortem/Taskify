<script lang="ts" setup>
import type { components } from '#nuxt-api-party/backend'



defineProps({
    members: {
        type: Array<components["schemas"]["BoardMemeber"]>,
        required: true
    }
})
const selected = defineModel({default:''})


</script>


<template>
    <USelectMenu v-model="selected" :items="$props.members" value-key="id" label-key="email" class="w-full">
        <template #item-leading="{item}">
            <UAvatar :src="item.avatar?useRuntimeConfig().public.AWSDomain + item.avatar: null" :alt="item.full_name || item.username || item.email"/>
        </template>
    </USelectMenu>
</template>