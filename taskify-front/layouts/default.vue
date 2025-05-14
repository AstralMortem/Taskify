<script setup lang="ts">
import { NavCard } from '#components';


</script>

<template>
    <div class="w-screen h-screen flex flex-col bg-neutral-100 items-center justify-center">
        <NavTopBar/>
        <div class="h-full w-full flex gap-4 justify-center items-start my-4 max-w-[80vw]">
            <NavCard/>
            <slot/>
        </div>
    </div>
</template>