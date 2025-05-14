<script setup lang="ts">
import { UserPhoto } from '#components';
import type { components } from '#nuxt-api-party/backend';
import type { PropType } from 'vue';


defineProps({
    user: {
        type: {} as PropType<components["schemas"]["UserRead"]>,
        required: true
    }
})



</script>


<template>
    <div class="flex flex-row justify-start items-center gap-3">
        <!-- <UAvatar :src="user.avatar" :alt="$props.user.full_name || $props.user.username" size="3xl"/> -->
        <UserPhoto :user="user" size="3xl"/>
        <div class="flex flex-col gap-0 items-start justify-start">
            <p class="font-semibold">{{ $props.user.full_name || $props.user.username }}</p>
            <p class="text-neutral-400">{{ $props.user.email }}</p>
        </div>
    </div>
</template>