<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';
import { z } from 'zod';

definePageMeta({
    layout: 'auth'
})


const state = ref<components["schemas"]["UserCreate"] >({
    confirmPassword: undefined
})

const schema = z
  .object({
    email: z.string(),
    username: z.string(),
    full_name: z.string().optional(),
    password: z.string().min(6),
    confirmPassword: z.string(),
  })
  .superRefine((data, ctx) => {
    if(data.confirmPassword !== data.password){
        ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: "Passwords do not match",
            path: ["confirmPassword"], // вказуємо, де показати помилку
        })
    }
  })


const authStore = useAuthStore()

const signup = async  () => {

    const payload = JSON.parse(JSON.stringify(state.value))
    delete payload["confirmPassword"]
    await authStore.signup(payload)
}

</script>

<template>
    <UIAuthCard title="SignUp">
        <UForm :state="state" :schema="schema" class="space-y-4" @submit.prevent="signup">
            <UFormField label="Email" name="email">
                <UInput v-model="state.email" placeholder="john@lennon.com" class="w-full"/>
            </UFormField>
            <UFormField label="Username" name="username">
                <UInput v-model="state.username" placeholder="john88" class="w-full"/>
            </UFormField>
            <UFormField label="Full name" name="full_name">
                <UInput v-model="state.full_name" placeholder="John Lennon" class="w-full"/>
            </UFormField>
            <UFormField label="Password" name="password">
                <UInput v-model="state.password" type="password" placeholder="password" class="w-full"/>
            </UFormField>
            <UFormField label="Configrm Password" name="confirmPassword">
                <UInput v-model="state.confirmPassword" type="password" placeholder="password" class="w-full"/>
            </UFormField>
            <div class="flex flex-col gap-2 w-full">
                <UButton label="Sign Up" type="submit" block/>
                <UButton label="Log In" variant="link" block @click="navigateTo('/auth/login')"/>
            </div>
        </UForm>
    </UIAuthCard>
</template>