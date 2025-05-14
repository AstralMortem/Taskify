export const useWelcome = () => {
    const boardStore = useBoardStore()
    
    const boardTitle = useState('boardTitle', ()=> '')
    const boardLists = useState<Array<string>>('boardLists', () => [])
    const listCards = useState<Array<string>>('listCards', () => [])
    const boardID = useState('boardID', () => '')
    const listID = useState('listID', () => '')

    const createBoards = async () => {
        try{
            const response = await $backend('/api/v1/boards/', {
                method: 'POST',
                body: {
                    title: boardTitle.value
                }
            })
            boardID.value = response.id
            await boardStore.fetchBoards()
            navigateTo('/welcome/lists')
        }catch(error){
            backendError(error)
        }
    }

    const createLists = async () => {
        try{
            boardLists.value.map(async (i, idx) => {
                const response = await $backend('/api/v1/lists/board/{board_id}', {
                    method: 'POST',
                    path: {
                        board_id: boardID.value
                    },
                    body: {
                        title: i
                    }
                })
                if(idx == 0){
                    listID.value = response.id
                }
            })
            await boardStore.fetchBoards()
            navigateTo('/welcome/cards')

        }catch(error){
            backendError(error)
        }
    }

    const createCards = async () => {
        try{
            listCards.value.map(async (i, idx) => {
                const response = await $backend('/api/v1/cards/list/{list_id}', {
                    method: 'POST',
                    path: {
                        list_id: listID.value
                    },
                    body: {
                        title: i,
                        description: i,
                        is_completed: false
                    }
                })
            })
            await reset()
            navigateTo('/boards/' + boardID.value)
            
        }catch(error){
            backendError(error)
        }
    }

    const reset = async () => {
        boardTitle.value = ''
        boardLists.value = []
        boardID.value = ''
        listCards.value = []
        listID.value = ''   
        await boardStore.fetchBoards()

    }

    const skip = async () => {
        reset()
        navigateTo('/')
    }

    const init = () => {
        reset()
        navigateTo('/welcome/boards')
    }

    return {init, skip, createBoards, createCards, createLists, boardTitle, boardLists, listCards}
}