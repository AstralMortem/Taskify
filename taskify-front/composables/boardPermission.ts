
export const useBoardPermission = () =>{
    return useState<'full' | 'edit' | 'read'>('boardPermission', () => 'full')
}