<script setup lang="ts">
import { UAvatar } from '#components';
import type { components } from '#nuxt-api-party/backend';
import type { PropType } from 'vue';


defineProps({
    user: {
        type: {} as PropType<components["schemas"]["UserRead"]>,
        required:true
    }
})

</script>

<template>
    <UAvatar :src="useRuntimeConfig().public.AWSDomain + user.avatar" :alt="$props.user.full_name || $props.user.username"/>
</template>