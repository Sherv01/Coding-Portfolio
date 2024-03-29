"""
Author(s): Shervin Darmanki Farahani, Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Nov. 16, 2023
"""

def is_empty(board):
    for row in board:
        for cell in row:
            if cell != " ":
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    y_start, x_start = y_end - d_y * (length - 1), x_end - d_x * (length - 1)
    start_bound = y_start - d_y < 0 or x_start - d_x < 0 or board[y_start - d_y][x_start - d_x] != " " #this is either true or false, true if the prev cell is either full or the edge
    end_bound = y_end + d_y >= len(board) or x_end + d_x >= len(board[0]) or board[y_end + d_y][x_end + d_x] != " " #same with this, except for the next cell insted of the prev cell
    if start_bound and end_bound:
        return "CLOSED"
    elif start_bound or end_bound:
        return "SEMIOPEN"
    else:
        return "OPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    #dealing with edge cases
    if y_start == 0 and x_start == 0:
        if board[y_start][x_start] == col:
            y_start = -1
            x_start = -1
    elif y_start == 0 and board[y_start][x_start] == col:
        y_start = -1
    elif x_start == 0 and board[y_start][x_start] == col:
        if length != 2:
            x_start = -1
    #the actual code
    open_seq_count, semi_open_seq_count = 0, 0
    for i in range(1, length + 1):
        ycoord, xcoord = y_start + d_y * i, x_start + d_x * i
        if 0 <= ycoord < len(board) and 0 <= xcoord < len(board[0]): #checks if the coordinates are even on the board
            if board[ycoord][xcoord] == col: #checks if the square is the same color
                if i == length:
                    #check if the next square in the sequence is of the same color and on board
                    y_next, x_next = y_start + d_y * (length + 1), x_start + d_x * (length + 1)
                    if 0 <= y_next < len(board) and 0 <= x_next < len(board[0]) and board[y_next][x_next] == col:
                        break
                    #check if the previous square in the sequence is of the same color and on board
                    y_prev, x_prev = y_start, x_start
                    if 0 <= y_prev < len(board) and 0 <= x_prev < len(board[0]) and board[y_prev][x_prev] == col:
                        break
                    #check if the sequence is open or semi-open
                    seq_type = is_bounded(board, y_start + d_y * (length), x_start + d_x * (length), length, d_y, d_x)
                    if seq_type == "OPEN":
                        open_seq_count += 1
                    elif seq_type == "SEMIOPEN":
                        semi_open_seq_count += 1
            else:
                #if the square is not of the same color, break
                break
        else:
            #if the coordinates are out of the board, break
            break
    return open_seq_count, semi_open_seq_count



def detect_rows(board, col, length):
    total_open_seq_count, total_semi_open_seq_count = 0, 0
    for y_start in range(-1, len(board)): #use -1 here because since detect row starts detecting the next square, we want to be able to check 0 as well
        for x_start in range(-1, len(board[0])):
            for d_y, d_x in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                open_seq_count, semi_open_seq_count = detect_row(board, col, y_start, x_start, length, d_y, d_x)
                total_open_seq_count += open_seq_count
                total_semi_open_seq_count += semi_open_seq_count
    return total_open_seq_count, total_semi_open_seq_count

def search_max(board):
    max_score = -10000000000
    move_y, move_x = -1, -1
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                board[y][x] = "b"
                current_score = score(board)
                if current_score > max_score:
                    max_score = current_score
                    move_y, move_x = y, x
                board[y][x] = " "
    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    for y_start in range(-1, len(board)):
            for x_start in range(-1, len(board[0])):
                for d_y, d_x in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                    sequence = []
                    for k in range(5):
                        if 0 <= y_start + k * d_y < len(board) and 0 <= x_start + k * d_x < len(board[0]):
                            sequence.append(board[y_start + k * d_y][x_start + k * d_x])
                    if len(sequence) == 5 and sequence.count("w") == 5 and is_bounded(board, y_start + 4 * d_y, x_start + 4 * d_x, 5, d_y, d_x) == "CLOSED":
                        return "White won"
                    elif len(sequence) == 5 and sequence.count("b") == 5 and is_bounded(board, y_start + 4 * d_y, x_start + 4 * d_x, 5, d_y, d_x) == "CLOSED":
                        return "Black won"
    white_open_seq_count, white_semi_open_seq_count = detect_rows(board, "w", 5)
    if white_open_seq_count > 0 or white_semi_open_seq_count > 0:
        return "White won"
    black_open_seq_count, black_semi_open_seq_count = detect_rows(board, "b", 5)
    if black_open_seq_count > 0 or black_semi_open_seq_count > 0:
        return "Black won"
    for row in board:
        if " " in row:
            return "Continue playing"
    return "Draw"




def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':
    easy_testset_for_main_functions()
    some_tests()
    # play_gomoku(8)
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 0, 1, 3, "w")  # Horizontal sequence at the top border
    print_board(board)
    print(detect_row(board, "w", 0, -1, 3, 0, 1))  # Expected output: (0, 1)

    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 0, 1, 2, "w")  # Horizontal sequence at the top border
    put_seq_on_board(board, 1, 0, 0, 1, 2, "w")  # Another horizontal sequence
    print_board(board)
    print(detect_rows(board, "w", 2))  # Expected output: (0, 6)

    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 0, 1, 5, "b")  # Horizontal sequence of 5 black stones at the top border
    print_board(board)
    #print(is_win(board))  # Expected output: 'Black won'



