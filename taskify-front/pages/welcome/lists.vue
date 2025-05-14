<script setup lang="ts">
const {boardLists, createLists, skip} = useWelcome()

definePageMeta({
    layout: 'auth'
})

</script>

<template>
    
    <UIAuthCard title="Create Lists">
        <div class="flex flex-col gap-4">
            <UFormField label="Name the columns">
                <UInput v-model="boardLists[0]" placeholder="like: 'Begin'" class="w-full"/>
            </UFormField>
            <UFormField>
                <UInput v-model="boardLists[1]" placeholder="like: 'In Progress'" class="w-full"/>
            </UFormField>
            <UFormField>
                <UInput v-model="boardLists[2]" placeholder="like: 'End'" class="w-full"/>
            </UFormField>
            <div class="flex flex-col gap-2">
                <UButton label="Continue" block @click="createLists"/>
                <UButton label="Skip" variant="ghost" class="self-end" @click="skip"/>
            </div>
        </div>
        
    </UIAuthCard>

</template>