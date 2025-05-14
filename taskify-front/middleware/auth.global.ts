export default defineNuxtRouteMiddleware(async (to, from) => {

    const authStore = useAuthStore()
    const cookie = useCookie("taskify_auth")



    if(!authStore.isAuthenticated && cookie.value){
        try{
            await authStore.fetchMe()
        }catch(error){
            return navigateTo('/auth/login')
        }
    }

    if(to.meta.authRequired && !authStore.isAuthenticated){
        return navigateTo('/auth/login')
    }

    
})
