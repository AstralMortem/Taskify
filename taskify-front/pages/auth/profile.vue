<script setup lang="ts">
import type { FormEvent, FormSubmitEvent } from '@nuxt/ui'
import { z } from 'zod'

definePageMeta({
    authRequired: true
})

const authStore = useAuthStore()
const {user} = storeToRefs(authStore)

const editUrl = "/api/v1/users/me"
const original = ref(JSON.parse(JSON.stringify(user.value)))

const resetPasswordState = ref({
    old_password: undefined,
    new_password: undefined,
    new_password_confirm: undefined
})

const schema = z.object({
    old_password: z.string(),
    new_password: z.string(),
    new_password_confirm: z.string()
}).superRefine((data,ctx) => {
    if(data.new_password !== data.new_password_confirm){
        ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: 'New passwords didn`t match',
            path: ['new_password_confirm']
        })
    }
})


type Schema = z.output<typeof schema>


const resetPassword = async (e: FormSubmitEvent<Schema>) => {
    await authStore.resetPassword(e.data.old_password, e.data.new_password)
    resetPasswordState.value = {
        old_password: undefined,
        new_password: undefined,
        new_password_confirm: undefined
    }
}

const acordionItem = [{
    label: 'Reset Password',
    slot: 'reset' as const
}, {
    label: 'Forgot Password',
    slot: 'forgot' as const
}, {
    label: 'OAuth Accounts',
    slot: 'oauth' as const
}]

</script>


<template>
    <UICard class="w-full h-full overflow-auto max-h-[80vh]">
        <div class="flex flex-col gap-4">
            
            <USeparator label="Profile Info"/>
            <UILabel label="Upload Avatar" class="w-fit">
                <UserAvatarUpload/>
            </UILabel>
            <UILabel label="Full Name">
                <UIEditField v-model="user.full_name" :original="original?.full_name"  :url="editUrl" name="full_name" />
            </UILabel>
            <div class="grid grid-cols-2 gap-4">
                <UILabel label="Email">
                    <UIEditField v-model="user.email" :original="original?.email" :url="editUrl" name="email"/>
                </UILabel>
                <UILabel label="Username">
                    <UIEditField v-model="user.username" :original="original?.username" :url="editUrl" name="username"/>
                </UILabel>
            </div>
            <USeparator label="Security"/>
            <UAccordion :items="acordionItem" :ui="{content: 'data-[state=open]:animate-[accordion-down_200ms_ease-out] data-[state=closed]:animate-[accordion-up_200ms_ease-out] overflow-hidden focus:outline-none p-4'}" >
                <template #reset>
                    <UForm :state="resetPasswordState" class="space-y-4" :schema="schema" @submit.prevent="resetPassword">
                        <UFormField label="Current passord" name="old_password">
                            <UInput v-model="resetPasswordState.old_password" type="password"/>
                        </UFormField>
                        <UFormField label="New password" name="new_password">
                            <UInput v-model="resetPasswordState.new_password" type="password"/>
                        </UFormField>
                        <UFormField label="New password confirm" name="new_passord_confirm">
                            <UInput v-model="resetPasswordState.new_password_confirm" type="password"/>
                        </UFormField>
                        <UButton label="Update" type="submit"/>
                    </UForm>
                </template>
                <template #forgot>
                    <UButton label="Forgot Password" @click="authStore.forgotPassword(authStore.user.email)"/>
                </template>
                <template #oauth>
                    <UserOAuthAccounts/>
                </template>
            </UAccordion>
        </div>
    </UICard>
</template>