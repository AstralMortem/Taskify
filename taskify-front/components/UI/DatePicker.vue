<script setup lang="ts">
import { CalendarDate, DateFormatter, getLocalTimeZone } from '@internationalized/date'
import { computed } from 'vue'

const df = new DateFormatter('uk-UA', {
  dateStyle: "short"
})

const model = defineModel<string>({ default: new Date().toISOString().split('T')[0] })

const modelValue = computed({
  get() {
    if(model.value){
      const [year, month, day] = model.value.split('-').map(Number)
      return new CalendarDate(year, month, day)
    }
    return null
  },
  set(value) {
    if(value){
      model.value = value.toString() 
    }
     // CalendarDate automatically formats to "YYYY-MM-DD"
  }
})
</script>

<template>
  <UPopover>
    <UButton color="neutral" variant="subtle" icon="i-lucide-calendar">
      {{ modelValue ? df.format(modelValue.toDate(getLocalTimeZone())) : 'Select a date' }}
    </UButton>

    <template #content>
      <UCalendar v-model="modelValue" class="p-2" />
    </template>
  </UPopover>
</template>
