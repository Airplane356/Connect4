import random 
import time
import copy

def loading_animation(duration):
    """
    Description: This function prints a trailing dot animation
    Parameters: Duration
    Returns: none
    """
    num_dots = 0
    while num_dots < 6:
        print("." * num_dots, end="\r")  # Print dots without newline
        num_dots += 1  # Increment number of dots (cycle from 0 to 5)
        time.sleep(duration)   

def halloffame():
    #Checks if hall of fame file exists, then displays all users in the hall of fame
    try:
        counter = 1
        file = open("HallofFame.txt", 'r')
        print("~ HALL OF FAME ~")
        for line in file:
            print(f"{counter}:", line.strip())
            counter += 1  
        file.close()
    except FileNotFoundError:
        print("No human has ever beat me.. mwah-ha-ha-ha!")
        return False

def halloffame_add(fileexist):
     #Appends name to the hall of fame, creating a file if none exists
    name = str(input("What is your name?: "))
    if fileexist == False:
        fileW = open("HallofFame.txt", 'w')
    else:
        fileW = open("HallofFame.txt", 'a')

    fileW.write(name)
    fileW.write('\n')

    print("You have been added to the hall of fame!")
    fileW.close()

def drop_piece(board, row, col, piece):
    """
    Description: this function plays the players piece
    Parameters: board, row, col, player
    Returns: board
    """
    board[row][col] = piece
    return board
    
def get_next_open_row(board, col):
    """
    Description: this function returns the next available row
    Parametesr: board, col
    Returns: next open row 
    """
    for r in range(6):
        if board[r][col] == ' ':
            return r

def print_board(board):
    """
    Description: Prints out the connect 4 board using nested for loops
    Parameters: Connect 4 board
    Returns: None
    """
    for x in reversed(range(6)):
        print("|| ", end = '')
        for y in range(7):
            print(board[x][y], end = ' || ')
        print()
        print("-"*37)

def winning_move(board, piece):
    """
    Description: this function checks for a winning position in all directions
    Parametesr: board, player
    Returns: True if win, False elsewise
    """
    # Check horizontal locations
    for c in range(4):
        for r in range(6):
            if (board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece):
                return True

    # Check vertical locations
    for c in range(7):
        for r in range(3):
            if (board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece):
                return True

    # Check positively sloped diagonals
    for c in range(4):
        for r in range(3):
            if (board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece):
                return True

    # Check negatively sloped diagonals
    for c in range(4):
        for r in range(3, 6):
            if (board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece):
                return True

    return False

def evaluate_window(window, piece):
    """
    Description: this function evaluates the score of each snippet based on how many clumps of 1, 2, 3, and 4 there are. 
    Parameters: window snipper, player
    Returns: score of the window
    """
    score = 0
    opponent_piece = 'X' if piece == 'O' else 'O'

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(' ') == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(' ') == 2:
        score += 2
    if window.count(opponent_piece) == 3 and window.count(' ') == 1:
        score -= 4

    return score

def score_position(board, piece):
    """
    Description: this function gets snippets of each possible rows of 4 in all directions and evaluates it
    Parameters: board, piece(player)
    Returns: score of the window
    """
    score = 0

    # Score center column
    center_array = [board[i][3] for i in range(6)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(6):
        for c in range(4):
            window = board[r][c:c + 4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(7):
        for r in range(3):
            window = [board[i][c] for i in range(r, r + 4)]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(3):
        for c in range(4):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(3):
        for c in range(4):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    """
    Description: minimax algorithm to determine best move 
    Parameters: board, depth, alpha, beta, maximizing_player(true if computer is maximizer, false elsewise)
    Returns: none/column, value
    """

    valid_locations = [col for col in range(7) if board[5][col] == ' ']

    if depth == 0 or winning_move(board, 'X') or winning_move(board, 'O'):
        if winning_move(board, 'O'):
            return (None, 100000000000000)
        elif winning_move(board, 'X'):
            return (None, -10000000000000)
        else:
            return (None, 0)

    if maximizing_player:
        value = float('-inf')
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, row, col, 'O')
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = float('inf')
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, row, col, 'X')
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_user_choice():
    """
    Description: prompts the user if they wanna go first
    Parametser: none
    Returns: none
    """
    while True:
        user_choice = input("Would you like to go first? (y/n): ").lower()
        if user_choice == "y":
            return True
        elif user_choice == "n":
            return False
        else:
            print("Invalid choice. Please enter 'y' for yes or 'n' for no.")

def get_user_column():
    """
    Description: prompts user to choose col
    Parameters: none
    Returns: none
    """
    while True:
        try:
            col = int(input("Player X, make your selection (1-7): ")) - 1
            if col in range(7):
                return col
            else:
                print("Invalid column. Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_ai_column(board, depth):
    col, _ = minimax(board, depth, float('-inf'), float('inf'), True)
    return col

def main():
    """mainline logic"""
    fileexist = halloffame()
    user_turn = get_user_choice()
    board = [[' ' for _ in range(7)] for _ in range(6)]
    print_board(board)
    
    game_over = False

    while not game_over:
        if user_turn:
            col = get_user_column()
            player = 'X'
        else:
            col = get_ai_column(board, 4)
            player = 'O'

        if board[5][col] == ' ':
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, player)
            if winning_move(board, player):
                print_board(board)
                print(f"Player {player} wins!")
                if player == 'X':
                    halloffame_add(fileexist)
                game_over = True
        else:
            print("Invalid move, please try again.")
            continue

        print("\n")
        print_board(board)

        if all(' ' not in row for row in board):
            print("It's a tie!")
            game_over = True

        user_turn = not user_turn

main()
