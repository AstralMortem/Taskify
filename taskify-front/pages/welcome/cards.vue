<script setup lang="ts">
const {listCards, createCards, skip} = useWelcome()

definePageMeta({
    layout: 'auth'
})

</script>

<template>
    
    <UIAuthCard title="Create Cards">
        <div class="flex flex-col gap-4">
            <UFormField label="Name the columns">
                <UInput v-model="listCards[0]" placeholder="like: 'Task 1'" class="w-full"/>
            </UFormField>
            <UFormField>
                <UInput v-model="listCards[1]" placeholder="like: 'Task 2'" class="w-full"/>
            </UFormField>
            <UFormField>
                <UInput v-model="listCards[2]" placeholder="like: 'Task 3'" class="w-full"/>
            </UFormField>
            <div class="flex flex-col gap-2">
                <UButton label="Continue" block @click="createCards"/>
                <UButton label="Skip" variant="ghost" class="self-end" @click="skip"/>
            </div>
        </div>
        
    </UIAuthCard>

</template>