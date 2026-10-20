def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return row[0]
    for column in range (3):
        if board[0][column] == board[1][column] == board[2][column] != "":
            return board[0][column]
        
    if board [0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board [0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]
    
    return None








