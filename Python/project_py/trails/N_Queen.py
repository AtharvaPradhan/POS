N=4

def theBoardSolver(board,col):
    if col>=N:
        return True
    for i in range(0,N):
        if toPlaceOrNot(board,i,col):
            board[i][col]=1
            if theBoardSolver(board,col+1)==True:
                return True
            board[i][col]=0
    return False

#checks whether any other queen is attacking
def toPlaceOrNot(board,row,col):
    #checks left of the queen 
    for i in range(0,col):     #horizontal check for queen in left
        if board[row][i]==1:
            return False
    
    for i,j in zip(range(row,-1,-1),range(col,-1,-1)): # vertical check
        if board[i][j]==1:
            return False

    for i,j in zip(range(row,N),range(col,0,-1)): # diagnols
        if board[i][j]==1:
            return False
    
    return True

def printBoard(board):
    for i in range(0,N):
        for j in range(0,N):
            print(board[i][j],end=" ")
        print("\n")
        
def main():
    board=[[0 for i in range(N)] for j in range(N)] 
    if theBoardSolver(board,0)==False:
        print("Solution not found")
        return False
    printBoard(board)
    return True
    
main()