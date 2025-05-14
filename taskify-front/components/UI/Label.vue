<script setup lang="ts">
defineProps({
    label: {
        type: String,
        default: ''
    }
})
</script>


<template>
    <div class="flex flex-col gap-1">
        <p class="font-semibold">{{ $props.label }}</p>
        <div class="w-full h-full ml-2">
            <slot/>
        </div>
        
    </div>
</template>