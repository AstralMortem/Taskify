<script setup lang="ts">
import type { FormSubmitEvent } from '@nuxt/ui'
import { z } from 'zod'

definePageMeta({
    layout: 'auth'
})
const route = useRoute()
const state = ref({
    new_password: undefined,
    new_password_confirm: undefined
})


const submit = async (e: FormSubmitEvent<Schema>) => {
    try{
        await $backend('/api/v1/auth/forgot-password-verify', {
            method: 'POST',
            body: {
                new_password: e.data.new_password,
                token: route.query.token as string
            }
        })
        navigateTo('/auth/login')
    }catch(error){
        backendError(error)
    }
}


const schema = z.object({
    new_password: z.string(),
    new_password_confirm: z.string()
}).superRefine((data,ctx) => {
    if(data.new_password !== data.new_password_confirm){
        ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: 'Passwords didn`t match',
            path: ['new_password_confirm']
        })
    }
})

type Schema = z.output<typeof schema>

</script>

<template>
    <UIAuthCard title="Verify">
    <UForm class="space-y-4" :state="state" :schema="schema" @submit.prevent="submit">
        <UFormField label="Password" name="password">
            <UInput v-model="state.new_password"/>
        </UFormField>
        <UFormField label="Confirm Password" name="password_confirm">
            <UInput v-model="state.new_password_confirm"/>
        </UFormField>
        <UButton label="Submit" type="submit" block/>
    </UForm>
    

</UIAuthCard>
</template>