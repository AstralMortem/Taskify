import { FetchError } from "ofetch"


export default function (error: FetchError){
    const toast = useToast()
    let title = "Error"
    let description = "An error occurred"


    if(error.statusCode){
        if(error.statusCode == 422){
            title = `(${error.statusCode}) Validation error`
            console.log(error.data)
            error.data.detail.forEach(e => {
                description += `\n ${e.loc.join('.')}: ${e.msg}`
            })

        }else{
            title = `(${error.statusCode}) ${error.data.title}`
            description = error.data.description
            if(error.data.debug){
                description += `\n <<${error.data.debug}>>`
            }
        }
    }else{
        title = error.name
        description = error.message 
    }
    
    toast.add({
        title,
        description,
        color: 'error',
    })

    console.error(error)


}
