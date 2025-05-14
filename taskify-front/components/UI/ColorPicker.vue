<script setup lang="ts">

const color = defineModel<string | undefined | null>({default: null})
const chip = computed(() => ({ backgroundColor: color.value }))
defineProps({
    previousColor: {
        type: String,
        default: undefined
    }
})

watch(color, ()=>{
  if(color.value === '#FFFFFF'){
    color.value = ''
  }
})

</script>


<template>
    <UPopover>
    <UButton label="Choose color" color="neutral" variant="outline">
      <template #leading>
        <span :style="chip" class="size-3 rounded-full" />
      </template>
    </UButton>

    <template #content>
    <div class="flex flex-col gap-1 p-2">
        <UColorPicker v-model="color" />
        <div class="flex flex-row justify-start gap-2 items-center">
            <UButton label="Clear" size="xs" @click="color = null" />
            <UButton v-if="$props.previousColor" label="Revert" size="xs" variant="outline"  @click="color = $props.previousColor"/>
        </div>
    </div>
    </template>
  </UPopover>
</template>