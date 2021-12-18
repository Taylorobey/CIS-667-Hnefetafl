import numpy as np
import matplotlib.pyplot as pt
import math
import random

# Hnefetafl Domain API

# state for each element in board array:
        # 0 = empty
        # 1 = restricted space
        # 2 = throne space
        # 3 = attacker piece
        # 4 = defender piece
        # 5 = king
        # 6 = king on restricted space
        # 7 = king on throne space

# Initialize board state
# x should be 7, 9, 11, 13, or 15
def setup_board(x):
    new_board = np.zeros(shape=(1)).astype(int)
    # 7x7, 9x9, 11x11, 13x13, or 15x15 squares
    if (x==7 or x==9 or x==11 or x==13 or x==15):
        #resize board, still contains zeros
        new_board.resize((x, x), refcheck=False)
        center = int(x/2)

        # center location on board is king on throne
        new_board[center][center] = 7
        #corners are restricted spaces
        new_board[0][0] = 1
        new_board[0][x-1] = 1
        new_board[x-1][0] = 1
        new_board[x-1][x-1] = 1
        #additional restricted spaces for larger boards, adjacent to corners
        if (x==13 or x==15):
            new_board[0][1] = 1
            new_board[1][0] = 1
            new_board[0][x-2] = 1
            new_board[1][x-1] = 1
            new_board[x-2][0] = 1
            new_board[x-1][1] = 1
            new_board[x-2][x-1] = 1
            new_board[x-1][x-2] = 1

        # set up pieces based on board size
        # place equal number of defender and attacker pieces in cardinal directions from king
        for i in range(1, int(center/2)+1):
            #defender
            new_board[center][center+i] = 4
            new_board[center][center-i] = 4
            new_board[center+i][center] = 4
            new_board[center-i][center] = 4

            #attacker
            new_board[center][i-1] = 3
            new_board[center][x-i] = 3
            new_board[i-1][center] = 3
            new_board[x-i][center] = 3
        # additional attacker placement based on board size, as the attacker should have double the number of pieces (not including king)
        # for 7x7 board, place additional attackers into gaps in cardinal directions
        if (x==7):
            new_board[center][1] = 3
            new_board[center][x-2] = 3
            new_board[1][center] = 3
            new_board[x-2][center] = 3
        # for larger boards, place extra pieces in T formation
        else:
            new_board[center+1][0] = 3
            new_board[center-1][0] = 3
            new_board[center+1][x-1] = 3
            new_board[center-1][x-1] = 3
            new_board[0][center+1] = 3
            new_board[0][center-1] = 3
            new_board[x-1][center+1] = 3
            new_board[x-1][center-1] = 3
            #largest boards need an additional 4 attackers
            if (x>11):
                new_board[center+2][0] = 3
                new_board[center-2][0] = 3
                new_board[center+2][x-1] = 3
                new_board[center-2][x-1] = 3

    return new_board

#return character based on content of array location
def icon(x):
    return {
        0: '\u25A1',
        1: 'X',
        2: 'H',
        3: '1',
        4: '0',
        5: 'K',
        6: 'K',
        7: 'K'
        }.get(x, ' ')

#get board size based on user selection
def size_get(x):
        return {
        0: 7,
        1: 9,
        2: 11,
        3: 13,
        4: 15,
        }.get(x, -1)

#get the player for the given piece
def player_get(x):
    if (x == 0) or (x == 1):
        return -1
    if (x == 2):
        return 0
    if (x == 3):
        return 2
    #only get here if x > 3
    return 1

# print out board
# takes a board state array
def display_board(board_curr):
    side_size = int(math.sqrt(board_curr.size))
    #print coordinates for usability
    if (side_size > 9):
        print(' ', end='')
    print(' ', end=' ')
    #print column labels
    for i in range(side_size):
        print(chr(ord('A')+i), end=' ')
    print("")
    # for each row
    for i in range (side_size):
        #spacing to account for larger board numbers
        if (side_size > 9) and (side_size-i < 10):
            print(' ', end='')
        #print row number
        print(str(side_size-i)+" ", end='')

        #print board
        for j in range(side_size):
            #set content to print based on location value
            content = icon(board_curr[i][j])
            #set content to print based on location value
            print(content, end=' ')
        print("")

#get all valid actions for current player
def valid_actions(board_curr, player_curr):
    side_size = int(math.sqrt(board_curr.size))
    # initially empty action list
    actions = []
    # for each space
    for i in range(side_size):
        for j in range(side_size):
            # check state of location
            x = board_curr[i][j]
            # if space contains a piece belonging to current player
            if (player_curr==player_get(x)):
                #find all possible actions for the piece
                moves = piece_actions(board_curr, player_curr, i, j)
                if (moves):
                    actions = actions + moves
    return actions

#get spaces a piece can move in a specific direction
def try_direction(board_curr, player_curr, a, b, x, y):
    #a and b are direction
    #x and y are initial position
        # All pieces move any number of vacant squares along a row or a column, just like a rook in chess.
        # Restricted squares may only be occupied by the king. 
        # The central restricted square, if it exists, is called the throne. It is allowed for the king to re-enter the throne.
        # All pieces may pass through restricted squares when they are empty. Restricted squares vary based on board configuration.
    side_size = int(math.sqrt(board_curr.size))
    actions = []
    end = False

    #check spaces until encountering a piece or the board edge
    #if space is empty and not restricted, add (a,b,c,d) to list, where (a,b) is current position and (c,d) is possible move

    #vertical move
    if (a != 0):
        i = x + a
        while (i > -1) and (i < side_size) and (end==False):
            #empty space (or restricted space if king is current piece)
            if (board_curr[i][y]==0) or (((board_curr[x][y])>=5) and (board_curr[i][y]==1 or board_curr[i][y]==2)):
                move = [x,y,i,y]
                actions.append(move)
            #piece in space
            elif(board_curr[i][y]<=7) and (board_curr[i][y]>=3):
                end = True
            i += a
    #horizontal move
    else:
        j = y + b
        end = False
        while (j > -1) and (j < side_size) and end==False:
            #empty space or restricted space if king is current piece
            if (board_curr[x][j]==0) or (((board_curr[x][y])>=5) and (board_curr[x][j]==1 or board_curr[x][j]==2)):
                move = [x,y,x,j]
                actions.append(move)
            #piece in space
            elif(board_curr[x][j]<=7) and (board_curr[x][j]>=3):
                end = True
            j += b

    #return possible actions for the direction
    return actions

# get valid actions for the piece at x, y on board_curr
def piece_actions(board_curr, player_curr, x, y):
    side_size = int(math.sqrt(board_curr.size))
    #initially empty list of actions
    actions = []

    # check possible actions for piece
    # for each direction, check spaces until encountering a piece or the board edge
    # if space is empty and not restricted, add (a,b,c,d) to list, where (a,b) is current position and (c,d) is possible move
    
    #check each direction
    for i in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_act = try_direction(board_curr, player_curr, i[0], i[1], x, y)
        if (new_act):
            actions = actions + new_act
    
    return actions

# take an action
    #check to see if pieces are removed or game is over
def take_action(board_curr, x):
    side_size = int(math.sqrt(board_curr.size))
    a = x[0]
    b = x[1]
    c = x[2]
    d = x[3]
    # move piece

    if (board_curr[a][b] < 6):
        board_curr[c][d] = board_curr[a][b]
    else:
        board_curr[c][d] += 5

    #remove from old position
    remove_piece(board_curr, a, b)

    #check to see if piece is in a possible capture position
    if ((c<=side_size -3) and (c>=2)) or ((d<=side_size -3) and (d>=2)):
        #get 5x5 grid with (c,d) at the center; fill a row/column with zeroes if not in board
        cap_grid = []
        for i in range(-2, 3):
            cap_row = []
            if (c+i >= 0) and (c+i <= side_size-1):
                for j in range(-2, 3):
                    if (d+j >= 0) and (d+j <= side_size-1):
                        cap_row.append(board_curr[c+i][d+j])
                    else:
                        cap_row.append(0)
            else:
                cap_row = [0,0,0,0,0]
            cap_grid.append(cap_row)
        cap_piece = capture(cap_grid)
        if (cap_piece):
            for x in cap_piece:
                remove_piece(board_curr, c+x[0], d+x[1])
            return True
           
    #return false if no piece is captured
    return False

def capture(cap_grid):
    cap_list = []
    #check capture status for all adjacent pieces
    for i in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        a = cap_grid[2][2]
        b = cap_grid[(2+i[0])][(2+i[1])]
        c = cap_grid[(2+(2*i[0]))][(2+(2*i[1]))]

        # if pieces being checked are allies or restricted spaces, and the piece between them is an enemy
        if ((a==c) or (c==1 or c==2)) and (is_enemy(a, b)):
            #check if piece to be captured is king
            if (b >=5):
                #king needs to be completely surrounded if on or next to throne
                if (i[0]==0):
                    d = cap_grid[1][2+i[1]]
                    e = cap_grid[3][2+i[1]]
                else:
                    d = cap_grid[2+i[0]][1]
                    e = cap_grid[2+i[0]][3]

                if (c==2 or d==2 or e==2 or b==7):
                    #check if surrounded
                    if((c==2 or is_enemy(b,c)) and (d==2 or is_enemy(b,d)) and (e==2 or is_enemy(b,e))):
                        cap_list.append((i[0], i[1]))
                else:
                    cap_list.append((i[0], i[1]))
            else:
                cap_list.append((i[0], i[1]))

    return cap_list

def remove_piece(board_curr, a, b):
    #check if piece was king on throne or restricted space
    if (board_curr[a][b]>=6):
        board_curr[a][b] -= 5
    else:
        board_curr[a][b] = 0
    
def is_enemy(a, b):
    enemy = False
    if (a==3) and (b==4 or b==5):
        enemy = True
    if (a==4 or a==5) and (b==3):
        enemy = True
    return enemy
    
def game_over(board_curr, player_curr):
    side_size = int(math.sqrt(board_curr.size))
    over = 0
    #if game is over, set over to number of winning player

    # king is not on board, player 2 wins
    if not ((5 in board_curr) or (6 in board_curr) or (7 in board_curr)):
        over = 2
    # king is on a board edge, player 1 wins
    if (5 in board_curr[0]) or (5 in board_curr[side_size-1]) or (5 in board_curr[:, 0]) or (5 in board_curr[:, side_size-1]) or (7 in board_curr[0]) or (7 in board_curr[side_size-1]) or (7 in board_curr[:, 0]) or (7 in board_curr[:, side_size-1]):
        over = 1

    return over

