from os import system

# draw tic-tac-toe board
def draw_board(board):
    # Clear screen before drawing each new board
    system('clear')

    # Draw board, and highlight occupied cells in green
    for i in range(3):
        print('  ' + (('\x1b[0;32;40m%s\x1b[0m' % board[i*3] ) if board[i*3] else str(i*3 + 1)) + '  ' + '|', end = '')
        print('  ' + (('\x1b[0;32;40m%s\x1b[0m' % board[i*3 + 1] ) if board[i*3 + 1] else str(i*3 + 2)) + '  ' + '|', end = '')
        print('  ' + (('\x1b[0;32;40m%s\x1b[0m' % board[i*3 + 2] ) if board[i*3 + 2] else str(i*3 + 3)) + '  ')
        if i != 2:
            print(19 * '-')
    print()

# player chooses whether to play X or O
def x_or_o():
    while True:
        human_player = input('Would you like to play X or O (X goes first)? ').upper()
        if human_player == 'X' or human_player == 'O':
            break
        elif human_player.lower() == 'exit':
            exit(0)
        else:
            print('Please enter a valid option.')
    return human_player

# Get next move from human player
def human_move():
    choice = input('Enter your next move or "exit" to exit game, %s: ' % human_player)

    # exit game if 'exit'
    if choice == 'exit':
        exit(0)

    # confirm integer entered (and assign to variable using zero-based numbering)
    try:
        move = int(choice)-1
    except:
        print('Please enter a valid choice (1-9 or "exit").')
        move = next_move(player)

    # confirm valid integer entered (1-9)
    if not 0 <= move <= 8:
        print('Please enter a valid choice (1-9 or "exit").')
        move = next_move(player)

    # allow player to enter another choice if cell already taken
    if board[move]:
        print('Please choose an available cell.')
        move = next_move(player)

    return move

# Get next move from computer player
def computer_move(board):
    # Initialize best score and move as empty
    best_score, best_move = None, None

    # Get available cells and only check scores for those cells
    moves = [ i for i in range(9) if not board[i] ]

    # Check scores for all available cells
    for move in moves:
        board[move] = computer_player
        last_score = -minimax(board, human_player)
        board[move] = None
        if best_score == None or last_score > best_score:
            best_score = last_score
            best_move = move

    return best_move

def minimax(board, player):
    # Change player to opponent to calculate ultimate game board
    next_player = 'X' if player == 'O' else 'O'

    # If game over in forward-looking state, add score of 1 to that player
    status = check_board(board)
    if status == player:
        return 1
    elif status == next_player:
        return -1

    # Only check available cells
    moves = [ i for i in range(9) if not board[i] ]
    best_score, best_move = None, None
    for move in moves:
        board[move] = player
        last_score = -minimax(board, next_player)
        board[move] = None
        if best_score == None or last_score > best_score:
            best_score = last_score
            best_move = move

    if not best_move:
        return 0

    return best_score

# get move from player
def next_move(player):
    # return choice of human or computer player
    return human_move() if player == human_player else computer_move(board)

# check board to see if game over
def check_board(board):
    # check for winners in all rows
    for i in range(3):
        if board[i*3] == board[i*3 + 1] == board[i*3 + 2] != None:
            return board[i*3]

    # check for winners in all columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != None:
            return board[i]

    # check for winners along diagonals
    if (board[0] == board[4] == board[8] != None) or (board[2] == board[4] == board[6] != None):
        return board[4]

    # check to see if there is a tie (i.e., all cells filled but no winner)
    for i in range(9):
        if not board[i]:
            return False

    return True

if __name__ == '__main__':
    # initialize board and print to screen
    board = [None for i in range(9)]

    draw_board(board)

    # Get choice of X/O from human player
    human_player = x_or_o()
    # Assign other role to computer player
    computer_player = 'X' if human_player == 'O' else 'O'

    # X plays first
    turn = 'X'
    game_over = False

    # continue game while no winner and board not full
    while not game_over:
        # Obtain and play move from current player
        board[next_move(turn)] = turn
        # Re-draw board every move
        draw_board(board)
        # Change turns
        turn = 'O' if turn == 'X' else 'X'
        # Check if game is over
        game_over = check_board(board)

    # if game over, announce result
    if game_over == 'X' or game_over == 'O':
        print('\x1b[1;36;40m%s WINS!\x1b[0m\n' % game_over)
    else:
        print('\x1b[1;36;40mNo winnner - game ends in a tie.\x1b[0m\n')
