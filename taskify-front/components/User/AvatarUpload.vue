<script setup lang="ts">
import { UserPhoto } from '#components'

const authStore = useAuthStore()

const preview = ref(JSON.parse(JSON.stringify(authStore.avatar)))
const selectedFile = ref()
const showUploader = ref(false)
const toast = useToast()

const handleFile = (event) => {
    const file = event.target.files[0] as File
    if (file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/gif']
        if(!validTypes.includes(file.type)){
            toast.add({
                title: 'Invalid File type',
                description: `Expect files: ${validTypes.join(',')}`,
                color: 'error' 
            })
            return
        }
        
        selectedFile.value = file
        const reader = new FileReader()
        reader.onload = (e) => {
            preview.value = e.target?.result
        }
        reader.readAsDataURL(file)
    }
}

const uploadFile = async () => {
    if(await authStore.uploadAvatar(selectedFile.value)){
        clear()
    }
    
}

const clear = () => {
    preview.value = ''
    selectedFile.value = undefined
    showUploader.value = false
}


</script>

<template>

    <div class="relative flex flex-row justify-center gap-1 items-center pointer cursor-pointer" @click="showUploader = true">
        
        <UIcon name="i-heroicons-pencil-square"/>
        <UserPhoto :user="authStore.user" size="3xl"/>
    </div>

    <UModal v-model:open="showUploader" title="Update Avatar">
        <template #body>
            <div class="flex flex-row gap-4">
                <UAvatar :src="preview" :alt="authStore.user.full_name || authStore.user.username || authStore.user.email" size="3xl"/>
                <UInput type="file" @change="handleFile"/>
            </div>
        </template>
        <template #footer>
            <div class="flex flex-row gap-2">
                <UButton label="Upload" color="success" @click="uploadFile"/>
                <UButton label="Cancel" color="warning" @click="clear" />
            </div>
        </template>

    </UModal>

</template>