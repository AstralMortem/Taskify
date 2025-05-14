<script setup lang="ts">
const authStore = useAuthStore()
const {user} = storeToRefs(authStore)

</script>


<template>
    <div class="flex flex-row justify-start items-center gap-2 rounded-lg ring-1 ring-default p-2">
        <div v-for="account in user.oauth_accounts" :key="account.id" class="flex flex-row gap-0.5 items-center group" >
            <UPopover>
                <UBadge>
                    <p>{{ account.oauth_name }}</p>
                </UBadge>
                <template #content>
                    <ul class="p-2">
                        <li>Name: {{ account.oauth_name }}</li>
                        <li>Email: {{ account.account_email }}</li>
                        <li>ID: {{ account.account_id }}</li>
                    </ul>
                </template>
            </UPopover>
            
            <UButton leading-icon="i-heroicons-x-mark" size="xs" color="error" class="hidden group-hover:flex" @click="authStore.removeOAuthAccount(account.id)"/>
        </div>
    </div>
</template>