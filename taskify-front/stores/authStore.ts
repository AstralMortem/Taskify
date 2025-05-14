import type { components } from "#nuxt-api-party/backend";
import { defineStore } from "pinia";


export const useAuthStore = defineStore("authStore", {
    state: () => ({
        user: {} as components["schemas"]["UserRead"],
        isPending: false
    }),
    actions: {
        async passwordLogin(credentials: components["schemas"]["LoginCredentials"]){
            try{
                this.isPending = true
                await $backend('/api/v1/auth/login', {
                    method: 'POST',
                    body: credentials
                })
                this.isPending = false
                const cookie = useCookie('taskify_auth')
                if(cookie.value){
                    await this.fetchMe()
                }else{
                    navigateTo('/auth/login')
                }
            }catch(error){
                backendError(error)
            }
        },
        async fetchMe(){
            // eslint-disable-next-line no-useless-catch
            try{
                this.isPending = true
                this.user = await $backend('/api/v1/users/me')
                this.isPending = false
            }catch(error){
                throw error
            }
        },
        async logout(){
            try{
                await $backend('/api/v1/auth/logout', {
                    method: 'POST'
                })
                navigateTo('/auth/login')
                this.user = {} as components["schemas"]["UserRead"]
            }catch(error){
                backendError(error)
            }
        },
        async signup(payload: components["schemas"]["UserCreate"]){
            try{
                await $backend('/api/v1/auth/signup', {
                    method: 'POST',
                    body: payload
                })
                navigateTo('/auth/login?next=/welcome')
            }catch(error){
                backendError(error)
            }
        },
        async getOAuthURL(provider: "github"){
            try{
                const response = await $backend(`/api/v1/oauth/${provider}/login`)
                navigateTo(response.authorization_url, {
                    external: true
                })
                
            }catch(error){
                backendError(error)
            }
        },
        async OAuthLogin(provider: "github", query: object){
            try{
                await $backend(`/api/v1/oauth/${provider}/callback`, {
                    query: query
                })
                const cookie = useCookie('taskify_auth')
                if(cookie.value){
                    await this.fetchMe()
                }else{
                    navigateTo('/auth/login')
                }
            }catch(error){
                backendError(error)
            }
        },
        async removeOAuthAccount(oauth_id: string){
            try{
                await $backend('/api/v1/oauth/{oauth_id}', {
                    method: 'DELETE',
                    path:{
                        oauth_id: oauth_id
                    }
                })
                this.user.oauth_accounts = this.user.oauth_accounts.filter(i => i.id !== oauth_id)
            }catch(error){
                backendError(error)
            }
        },
        async resetPassword(old_password: string, new_password: string){
            try{
                const user = await $backend('/api/v1/auth/reset-password', {
                    method: 'POST',
                    body:{
                        old_password,
                        new_password
                    }
                })
                this.user = user
            }catch(error){
                backendError(error)
            }
        },
        async forgotPassword(email: string){
            try{
                await $backend('/api/v1/auth/forgot-password', {
                    method: 'POST',
                    body: {
                        email: email
                    }
                })

                useToast().add({
                    title: 'Message Send',
                    description: 'Reset link was send on ' + email,
                    color: 'success'
                })
            }catch(error){
                backendError(error)
                throw error
            }
        },
        async uploadAvatar(file: Blob){
            const form = new FormData()
            form.append('file', file)
            try{
                this.user = await $backend('/api/v1/files/avatars', {
                    method: 'PUT',
                    body: form
                })
                return true
            }catch(error){
                backendError(error)
                return false
            }
        }
    },
    getters: {
        isAuthenticated: (state) => Boolean(Object.keys(state.user).length),
        avatar: (state) => state.user.avatar? 'http://localhost:9000/' + state.user.avatar : null
    }
})