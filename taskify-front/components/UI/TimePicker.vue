<script setup lang="ts">

const model = defineModel<string>({default: `${new Date().getHours()}:${new Date().getMinutes()}`})


const firstPart = ref(model.value.split(':')[0])
const secondPart = ref(model.value.split(':')[1])

const hours = Array.from({length: 24}, (_, i) => i.toString().padStart(2, '0'))
const minutes = Array.from({length: 60}, (_, i) => i.toString().padStart(2, '0'))

watch(model, (newValue)=>{
    if(newValue){
        const [hour, minute] = newValue.split(':')
        firstPart.value = hour
        secondPart.value = minute
    }
})


watch(firstPart, (newValue)=>{
    if(newValue){
        model.value = `${newValue}:${secondPart.value}`
    }
})

watch(secondPart, (newValue)=>{
    if(newValue){
        model.value = `${firstPart.value}:${newValue}`
    }
})





</script>


<template>

<UPopover>
    <UButton color="neutral" variant="subtle" icon="i-lucide-timer">
      {{ model || 'Select a date' }}
    </UButton>

    <template #content>
      <div class="flex flex-row gap-2 items-center p-2">
        <USelect v-model="firstPart" :items="hours" />
        <span>:</span>
        <USelect v-model="secondPart" :items="minutes" />
      </div>
    </template>
  </UPopover>

</template>
