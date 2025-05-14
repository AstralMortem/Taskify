<script setup lang="ts">
definePageMeta({
    layout: 'auth'
})

const email = ref('')

const authStore = useAuthStore()

const submit = async () => {
    try{
        await authStore.forgotPassword(email.value)
        navigateTo('/auth/login')
    }catch(error){
        console.log(error)
    }
    
    
}

</script>


<template>
<UIAuthCard title="Forgot Password">
    <UForm class="space-y-4" @submit.prevent="submit">
        <UFormField label="Email" required>
            <UInput v-model="email"/>
        </UFormField>
        <UButton label="Submit" type="submit" block/>
    </UForm>
    

</UIAuthCard>
</template>