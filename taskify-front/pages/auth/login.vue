<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';

definePageMeta({
    layout: 'auth'
})

const state = ref<components["schemas"]["LoginCredentials"]>({
    email: '',
    password: ''
})

const route = useRoute()

const authStore = useAuthStore()
const login = async () => {
    await authStore.passwordLogin(state.value)
    if(authStore.isAuthenticated){
        if(route.query.next){
            navigateTo(route.query.next as string)
        }else{
            navigateTo('/')
        }
        
    }
}


</script>

<template>
    <UIAuthCard title="Log In">
        <UForm :state="state" class="space-y-4" @submit.prevent="login">
            <UFormField label="Email/Username" name="username">
                <UInput v-model="state.email" placeholder="john@lennon.com" class="w-full"/>
            </UFormField>
            <UFormField label="Password" name="password">
                <UInput v-model="state.password" type="password" placeholder="password" class="w-full"/>
            </UFormField>
            <div class="flex flex-col gap-2 w-full">
                <UButton label="Log In" type="submit" block/>
                <UButton label="Sign Up" variant="link" block @click="navigateTo('/auth/signup')"/>
            </div>
        </UForm>
        <div class="flex flex-col gap-4">
            <USeparator label="OR"/>
            <UIOAuthButton provider="github" title="GitHub"/>
        </div>
    </UIAuthCard>
</template>