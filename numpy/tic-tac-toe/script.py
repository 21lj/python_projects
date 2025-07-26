import numpy as np 

def createBoard():
    return np.zeros((3, 3), dtype='int') # We'll use 0 = empty, 1 = Player X, 2 = Player O

def printBoard(board):
    chars = {
        0: " ",
        1: "X",
        2: "O"
    }
    print("\nBoard: ")
    for i in board:
        print("|".join(chars[j] for j in i))
        print("-"*5)

# board=createBoard()
# printBoard(board)

def playerMove(board, player):
    while True:
        try:
            move =input(f"Player {player} enter your move as 'row,col' (0-based): ")
            row, col=map(int, move.strip().split(","))
            if board[row, col] != 0:
                print("Spot already taken. Try again!!")
            else:
                board[row, col]=player
                break
        except:
            print("Invalid Input. enter 0, 1, or 2 seprated by ,")

# playerMove(board, 1)
# printBoard(board)

def checkWin(board, player):
    for i in range(3):
        if np.all(board[i, :]==player) or np.all(board[:,i]==player):
            return True
        if np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board))==player):
            return True
        return False
    
def checkDraw(board):
    return not np.any(board==0)

def playGame():
    board=createBoard()
    current_player=1 # the 'X'

    while True:
        printBoard(board)
        playerMove(board, current_player)

        if checkWin(board, current_player):
            printBoard(board)
            print(f"player {current_player} wins!!")
            break
        elif checkDraw(board):
            printBoard(board)
            print("It's a draw!!")
            break

        current_player=2 if current_player==1 else 1

if __name__=="__main__":
    playGame()