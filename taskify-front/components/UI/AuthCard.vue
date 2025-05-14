<script setup lang="ts">

defineProps({
    title: {
        type: String,
        default: ''
    }
})

</script>

<template>
    <UICard class="min-w-[300px]">
        <div class="flex flex-col py-4 gap-8 px-8">
            <div class="flex flex-col gap-5 items-center">
                <img src="/img/logo_primary.svg" class="w-14 h-14">
                <p class="font-bold text-2xl">{{ $props.title }}</p>
            </div>
            <slot/>
        </div>
    </UICard>
</template>