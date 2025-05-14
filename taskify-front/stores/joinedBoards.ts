import type { components } from "#nuxt-api-party/backend";

export const useJoinedBoardsStore = defineStore('joinedBoards', {
    state: () => ({
        currentBoardId: "",
        boards: [] as Array<components["schemas"]["BoardRead"]>,
        isPending: false,
        page: 1,
        total: 0,
        pages: 0,
        size: 10
    }),
    getters: {
        currentBoard: (state) => state.boards.find(i => i.id === state.currentBoardId)
    },

    
    actions:{
        async fetchBoards(){
            try{
                this.isPending = true
                const response = await $backend('/api/v1/boards/membered/all', {
                    method: 'GET',
                    query: {
                        size: this.size,
                        page: this.page 
                    }
                })
                this.isPending = false
                this.boards = [...this.boards, ...response.items]
                this.page = response.page || 1
                this.pages = response.pages || 0
                this.total = response.total || 0

                this.page += 1 

            }catch(error){
                backendError(error)
            }
        },

        setBoardId(board_id:string){
            this.currentBoardId = board_id
        },
        updateBoard(newBoard: components["schemas"]["BoardRead"]){
            const idx = this.boards.findIndex(b => b.id === newBoard.id)
            if(idx >= 0){
                this.boards[idx] = newBoard
            }
        },
        deleteBoard(oldBoard: components["schemas"]["BoardRead"]){
            this.boards = this.boards.filter(b => b.id !== oldBoard.id)
            if(this.boards.length > 0){
                const board = this.boards[0]
                this.setBoardId(board.id)
                navigateTo('/boards/' + board.id)
            }else{
                this.setBoardId("")
                navigateTo('/')
            }
        },
    }
})