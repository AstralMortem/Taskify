import type { components } from "#nuxt-api-party/backend";
import { defineStore } from "pinia";


export const useBoardStore = defineStore('boardStore', {
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

    actions: {
        async fetchBoards(){
            try{
                this.isPending = true
                const response = await $backend('/api/v1/boards/', {
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
        setBoardId(boardId: string){
            this.currentBoardId = boardId
        },
        addBoard(newBoard: components["schemas"]["BoardRead"]){
            this.boards.push(newBoard)
            this.total += 1
            navigateTo('/boards/' + newBoard.id)
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
        async addMember(board_id: string, member_id: string){
            try{
                const newBoard = await $backend('/api/v1/boards/{board_id}/members/{member_id}', {
                    method: 'POST',
                    path: {
                        board_id: board_id,
                        member_id: member_id
                    }
                })
                const idx = this.boards.findIndex(i => i.id == board_id)
                if(idx >= 0){
                    this.boards[idx] = newBoard
                }
            }catch(error){
                backendError(error)
            }
        },
        async removeMemeber(board_id: string, member_id: string){
            try{
                const newBoard = await $backend('/api/v1/boards/{board_id}/members/{member_id}', {
                    method: 'DELETE',
                    path: {
                        board_id: board_id,
                        member_id: member_id
                    }
                })
                
                const idx = this.boards.findIndex(i => i.id == board_id)
                if(idx >= 0){
                    this.boards[idx] = newBoard
                }
            }catch(error){
                backendError(error)
            }
        }
        
    }
})