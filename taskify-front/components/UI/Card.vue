<script setup lang="ts">

const props = defineProps({
    rounded: {
        type: String as () => '2xl' | '4xl' | 'xl' | 'md' | '10',
        default: '2xl'
    },
    background: {
        type: String,
        default: ''
    },
    withoutPaddings: {
        type: Boolean,
        default: false
    }
})

const roundedClass = computed(() =>{
    switch(props.rounded){
        case '4xl': return 'rounded-4xl';
        case '2xl': return 'rounded-2xl';
        case 'xl': return 'rounded-xl';
        case 'md': return 'rounded-md';
        case '10': return 'rounded-[10px]';
        default: return 'rounded-2xl'
    }
})

const uiClass = computed(()=> {
    if(props.withoutPaddings){
        return {root: 'p-2 sm:p-2 ring-0 ' + roundedClass.value, body: 'p-0 sm:p-0'}
    }else{
        return {root: 'p-4 sm:p-4 ring-0 ' + roundedClass.value, body: 'p-0 sm:p-0'}
    }
})


</script>


<template>
    <UCard :ui="uiClass" :style="{backgroundColor: $props.background}">
        <slot/>
    </UCard>
</template>