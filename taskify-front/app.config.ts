export default defineAppConfig({
    ui: {
        colors: {
            primary: 'blue',
            neutral: 'zinc'
        },
        button: {
            slots:{
                base: 'hover:cursor-pointer'
            }
        }
    }
})