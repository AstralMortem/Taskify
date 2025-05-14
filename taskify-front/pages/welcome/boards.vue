<script setup lang="ts">
const {boardTitle, createBoards, skip} = useWelcome()

definePageMeta({
    layout: 'auth'
})

</script>

<template>
    
    <UIAuthCard title="Create Board">
        <div class="flex flex-col gap-4">
            <UFormField label="Enter the board name">
                <UInput v-model="boardTitle" placeholder="like: 'My board'" class="w-full"/>
            </UFormField>
            <div class="flex flex-col gap-2">
                <UButton label="Continue" block @click="createBoards"/>
                <UButton label="Skip" variant="ghost" class="self-end" @click="skip"/>
            </div>
        </div>
        
    </UIAuthCard>

</template>