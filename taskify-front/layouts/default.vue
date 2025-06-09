<script setup lang="ts">
import { NavCard } from '#components';


</script>

<template>
    <div class="w-screen h-full min-h-screen flex flex-col bg-neutral-100 items-center justify-start">
        <NavTopBar/>
        <div class="h-full w-full flex flex-col md:flex-row gap-4 justify-start md:justify-center items-start my-4 max-w-[80vw]">
            <NavCard class="w-full md:w-[30%]"/>
            <slot/>
        </div>
    </div>
</template>