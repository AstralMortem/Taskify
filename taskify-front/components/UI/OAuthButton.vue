<script setup lang="ts">
defineProps({
    provider: {
        type: String as () => "github",
        required: true
    },
    title: {
        type: String,
        default: ''
    }
})

const authStore = useAuthStore()


</script>

<template>
    <UButton :label="$props.title || $props.provider" size="xl" variant="outline" :leading-icon="`mdi:${$props.provider.toLowerCase()}`" @click="authStore.getOAuthURL($props.provider)" :ui="{leadingIcon: 'text-2xl'}"/>
</template>