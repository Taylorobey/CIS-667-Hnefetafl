import numpy as np
import matplotlib.pyplot as pt
import math
import random

# Hnefetafl Domain API

# Initialize board state
# x should be 7, 9, 11, 13, or 15
def setup_board(x):
    new_board = np.zeros(shape=(1)).astype(int)
    # 7x7, 9x9, 11x11, 13x13, or 15x15 squares
    if (x==7 or x==9 or x==11 or x==13 or x==15):
        #resize board, still contains zeros
        new_board.resize((x, x), refcheck=False)
        center = int(x/2)
        # state for each element in board array:
        # 0 = empty
        # 1 = restricted space
        # 2 = throne space
        # 3 = attacker piece
        # 4 = defender piece
        # 5 = king
        # 6 = king on restricted space
        # 7 = king on throne space

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
        # for larger boards, place extra pieces in triangle formation
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

# print out board
# takes a board state array
def display_board(board_curr):
    side_size = int(math.sqrt(board_curr.size))
    #print coordinates for usability
    if (side_size > 9):
        print(' ', end='')
    print(' ', end=' ')
    for i in range(side_size):
        print(chr(ord('A')+i), end=' ')
    print("")
    #print each row
    for i in range (side_size):
        #print coordinates for usability
        print(str(i+1)+" ", end='')
        if (side_size > 9) and (i < 9):
            print(' ', end='')
        #print each character in the row
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
            if (player_curr==1 and (x>=4)) or (player_curr==2 and x==3):
                #find all possible actions for the piece
                moves = piece_actions(board_curr, player_curr, i, j)
                if (moves):
                    actions.append(moves)
    return actions

# get valid actions for the piece at x, y on board_curr
    # All pieces move any number of vacant squares along a row or a column, just like a rook in chess.
    # Restricted squares may only be occupied by the king. 
    # The central restricted square, if it exists, is called the throne. It is allowed for the king to re-enter the throne.
    # All pieces may pass through restricted squares when they are empty. Restricted squares vary based on board configuration.
def piece_actions(board_curr, player_curr, x, y):
    side_size = int(math.sqrt(board_curr.size))
    #initially empty list of actions
    actions = []

    # check possible actions for piece
    # for each direction, check spaces until encountering a piece or the board edge
    # if space is empty and not restricted, add (a,b,c,d) to list, where (a,b) is current position and (c,d) is possible move
    
    #check up
    i = x - 1
    end = False
    while (i > -1) and end==False:
        #empty space or restricted space if king is current piece
        if (board_curr[i][y]==0) or (((board_curr[x][y])>=5) and (board_curr[i][y]==1 or board_curr[i][y]==2)):
            move = [x,y,i,y]
            actions.append(move)
        #piece in space
        elif(board_curr[i][y]<=7) and (board_curr[i][y]>=3):
            end = True
        i -= 1
    #check down
    i = x + 1
    end = False
    while (i < side_size) and end==False:
        #empty space or restricted space if king is current piece
        if (board_curr[i][y]==0) or (((board_curr[x][y])>=5) and (board_curr[i][y]==1 or board_curr[i][y]==2)):
            move = [x,y,i,y]
            actions.append(move)
        #piece in space
        elif(board_curr[i][y]<=7) and (board_curr[i][y]>=3):
            end = True
        i += 1
    #check right
    j = y + 1
    end = False
    while (j < side_size) and end==False:
        #empty space or restricted space if king is current piece
        if (board_curr[x][j]==0) or (((board_curr[x][y])>=5) and (board_curr[x][j]==1 or board_curr[x][j]==2)):
            move = [x,y,x,j]
            actions.append(move)
        #piece in space
        elif(board_curr[x][j]<=7) and (board_curr[x][j]>=3):
            end = True
        j += 1
    #check left
    j = y - 1
    end = False
    while (j > -1) and end==False:
        #empty space or restricted space if king is current piece
        if (board_curr[x][j]==0) or (((board_curr[x][y])>=5) and (board_curr[x][j]==1 or board_curr[x][j]==2)):
            move = [x,y,x,j]
            actions.append(move)
        #piece in space
        elif(board_curr[x][j]<=7) and (board_curr[x][j]>=3):
            end = True
        j -= 1
    
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

    # check to see if a piece is removed
    # if an enemy piece is cardinally adjacent to destination and there is a space on other side of that piece
    if (c<=side_size -3):
        if is_enemy(board_curr[c][d], board_curr[c+1][d]):
            #check if enemy piece is captured
            if (check_capture(board_curr, (c+1), d, 0)):
                #remove piece from board
                remove_piece(board_curr, (c+1), d)
                return True
    if (d<=side_size -3):
        if is_enemy(board_curr[c][d], board_curr[c][d+1]):
            #check if enemy piece is captured
            if (check_capture(board_curr, c, (d+1), 1)):
                #remove piece from board
                remove_piece(board_curr, c, (d+1))
                return True
    if (c>=2):
        if is_enemy(board_curr[c][d], board_curr[c-1][d]):
            #check if enemy piece is captured
            if (check_capture(board_curr, (c-1), d, 0)):
                #remove piece from board
                remove_piece(board_curr, (c-1), d)
                return True
    if (d>=2):
        if is_enemy(board_curr[c][d], board_curr[c][d-1]):
            #check if enemy piece is captured
            if (check_capture(board_curr, c, (d-1), 1)):
                #remove piece from board
                remove_piece(board_curr, c, (d-1))
                return True
    return False

def check_capture(board_curr, a, b, c):
    side_size = int(math.sqrt(board_curr.size))
    center = int(side_size/2)
    #piece to check is king on or next to throne, must be surrounded
    if ((a<=center+1 and a>=center-1 and b==center) or (b<=center+1 and b>=center-1 and a==center)):
        if (board_curr[a][b]>=5):
            #surrounded by enemies or throne on all sides
            if (board_curr[a+1][b]==2 or is_enemy(board_curr[a][b], board_curr[a+1][b])) and (board_curr[a-1][b]==2 or is_enemy(board_curr[a][b], board_curr[a-1][b])) and (board_curr[a][b+1]==2 or is_enemy(board_curr[a][b], board_curr[a][b+1])) and (board_curr[a][b-1]==2 or is_enemy(board_curr[a][b], board_curr[a][b-1])):
                return True  
    #otherwise, check if piece is between two enemy pieces or enemy and restricted space
    #aggressor is adjacent along a
    if (c==0):
        #check for edges of board
        if (a > 0) and (a < (side_size - 1)):
            if ((board_curr[a-1][b]==1) or (board_curr[a-1][b]==2 and board_curr[a][b]==3) or (is_enemy(board_curr[a-1][b], board_curr[a][b]))) and ((board_curr[a+1][b]==1) or (board_curr[a+1][b]==2 and board_curr[a][b]==3) or (is_enemy(board_curr[a+1][b], board_curr[a][b]))):
                return True
    #aggressor is adjacent along b
    if (c==1):
        #check for edges of board
        if (b > 0) and (b < (side_size - 1)):
            if ((board_curr[a][b-1]==1) or (board_curr[a][b-1]==2 and board_curr[a][b]==3) or (is_enemy(board_curr[a][b-1], board_curr[a][b]))) and ((board_curr[a][b+1]==1) or (board_curr[a][b+1]==2 and board_curr[a][b]==3) or (is_enemy(board_curr[a][b+1], board_curr[a][b]))):
                return True

    #no captures
    return False

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
    
def game_over(board_curr, player_curr, prev_states):
    side_size = int(math.sqrt(board_curr.size))
    over = 0
    #if game is over, set over to number of winning player

    # king is not on board, player 2 wins
    if not ((5 in board_curr) or (6 in board_curr) or (7 in board_curr)):
        over = 2
    # king is on a board edge, player 1 wins
    if (5 in board_curr[0]) or (5 in board_curr[side_size-1]) or (5 in board_curr[:, 0]) or (5 in board_curr[:, side_size-1]) or (7 in board_curr[0]) or (7 in board_curr[side_size-1]) or (7 in board_curr[:, 0]) or (7 in board_curr[:, side_size-1]):
        over = 1
    # if the board state is repeated three times, the player who last moved loses (to avoid stalemates)
    if (len(prev_states)==6):
        over = (player_curr % 2) + 1

    #unsure how to implment, may not be necessary as this is a variant rule
    # attackers surround all defenders, no gaps in cardinal directions, player 1 wins
    return over

# basic AI
def basic_AI(board_curr, player):
    #choose actions evenly at random
    basic_actions = sum(valid_actions(board_curr, player), [])
    if(not basic_actions):
        return [-1,-1,-1,-1]
    else:
        ind = random.randrange(0, len(basic_actions)-1)
        return basic_actions[ind]

# tree-based AI
def tree_AI(board_curr, player, prev_states, depth, enemytype):
    side_size = int(math.sqrt(board_curr.size))
    #possible actions
    tree_actions = sum(valid_actions(board_curr, player), [])
    scores = []
    visits = []

    if(len(tree_actions)==0):
        return ([-1,-1,-1,-1], 0)
    else:
        #get score and visited nodes for each possible move using eval, then pick highest scoring node
        children = np.empty((len(tree_actions), side_size, side_size))
        captures = []
        for i in range(len(tree_actions)):
            board_copy = np.copy(board_curr)
            if (take_action(board_copy, tree_actions[i])):
                captures.append(i)
            children[i] = board_copy
        #set initial previous best to -1000 so that at least one child will be chosen by evaluation
        evals = []
        #prioritize capturing moves
        if (captures):
            for i in range(len(tree_actions)):
                if (captures.count(i)):
                    prev = np.copy(prev_states)
                    if (len(prev)>=2):
                        if not (np.array_equal(children[i], prev[-2])):
                            prev_last = prev[-1]
                            prev = np.array([prev_last, ])
                    np.append(prev, np.copy(children[i]), axis=0)
                    evals.append(eval_state(children[i], player, ((player % 2) + 1), prev, depth, -1000, enemytype))
                else:
                    evals.append((-1000, 0))
        else:
            for child in children:
                prev = np.copy(prev_states)
                if (len(prev)>=2):
                    if not (np.array_equal(child, prev[-2])):
                        prev_last = prev[-1]
                        prev = np.array([prev_last, ])
                    np.append(prev, np.copy(child), axis=0)
                evals.append(eval_state(child, player, ((player % 2) + 1), prev, depth, -1000, enemytype))
        if (evals):
                scores, visits = map(list, zip(*evals))
        return (tree_actions[np.argmax(scores)], sum(visits))

def state_score(board, player):
    #return number of pieces belonging to player, minus pieces belonging to opponent
    score_1 = np.count_nonzero(board==4)
    score_2 = np.count_nonzero(board==3)
    if (player==1):
        return (score_1 - score_2)
    else:
        return (score_2 - score_1)

def eval_state(board_curr, orig_player, player, prev_states, depth, prev_best, enemytype):
    side_size = int(math.sqrt(board_curr.size))
    #learning discount
    dis = 1/(4**(4-depth))
    #track score for this state. score based on diffrence in remaining pieces
    #include score of this state
    score = state_score(board_curr, orig_player)
    #maximum/minimum possible score for players (does not include king in score count, as it is always assumed to be on board if game has not ended)
    max_score = [(4 * (int(side_size/4))), (8 * (int(side_size/4)))]
    min_score = [(-8 * (int(side_size/4))), (-4 * (int(side_size/4)))]
    #record number of nodes/states visited
    visited = 1
    #limited depth minimax/expectimax evaluation, value wins highly positive and losses highly negative
    #keep relatively close to max score in order to increase ability to prune
    game = game_over(board_curr, player, prev_states)
    if game == orig_player:
        score = max_score[orig_player - 1] * 1.25
    elif game > 0:
        score = min_score[orig_player - 1] * 1.25
    else:
        #base case
        if (depth==0):
            return (score, visited)
        #possible actions
        child_actions = sum(valid_actions(board_curr, player), [])
        if (len(child_actions)>0):
            #check to see if king can reach edge
            if (player==1):
                king_actions = [(a,b,c,d) for a,b,c,d in child_actions if (board_curr[a][b] > 5)]
                king_nodes = 0
                for k_action in king_actions:
                    king_board = np.copy(board_curr)
                    take_action(king_board, k_action)
                    king_nodes += 1
                    if (game_over(king_board, player, prev_states))==player:
                        return ((max_score[1] * 1.5), (visited + king_nodes))
                visited += king_nodes
            #hybrid limited depth tree/monte-carlo search
            else:
                new_player = (player % 2) + 1
                mca = 7 #number of actions chosen to search
                ft = 2 #depth at which a full tree search is performed

                #track current score for pruning purposes, set initially to worse than worst case for each
                best_score = min_score[player - 1] * 1.5
                worst_score = max_score[player -1] * 1.5

                if (depth > ft):
                    #reduce possible actions to check
                    new_actions = []
                    if (len(child_actions) > mca):
                        while(len(new_actions) < mca):
                            new_actions.append(child_actions.pop(random.randrange(len(child_actions))))
                        child_actions = new_actions

                #if currently the original player, check all remaining child nodes
                if (orig_player==player):
                    #add king's actions to be checked for player 1
                    if (player==1):
                        child_actions = child_actions
                    #check possible nodes
                    for action in child_actions:
                        new_board = np.copy(board_curr)
                        take_action(new_board, action)
                        #add child to prev_states 
                        prev = np.copy(prev_states)
                        if (len(prev)>=2):
                            if not (np.array_equal(board_curr, prev[-2])):
                                prev_last = prev[-1]
                                prev = np.array([prev_last, ])
                        np.append(prev, new_board, axis=0)
                        new_score, new_visits = eval_state(new_board, orig_player, new_player, np.copy(prev_states), (depth-1), best_score, enemytype)
                        visited += new_visits
                        #best possible score update
                        if (new_score > best_score):
                            best_score = new_score
                    score += best_score
                #if current player is the opponent, evaluate all children, but check for possible pruning
                #if it is impossible for current node to be better than previous best, stop searching and return -1000
                else:
                    #if enemy is simple AI, model probabilistically with all actions being equally probable (expectimax)
                    if (enemytype==1):
                        known_sum = 0
                        rem_child = len(child_actions)
                        for action in child_actions:
                            #check if higher score is possible
                            if (prev_best < ((known_sum + (rem_child * max_score[player-1]))/len(child_actions))):
                                #if it is, evaluate child
                                new_board = np.copy(board_curr)
                                take_action(new_board, action)
                                #add child to prev_states 
                                prev = np.copy(prev_states)
                                if (len(prev)>=2):
                                    if not (np.array_equal(board_curr, prev[-2])):
                                        prev_last = prev[-1]
                                        prev = np.array([prev_last, ])
                                np.append(prev, new_board, axis=0)
                                new_score, new_visits = eval_state(new_board, orig_player, new_player, np.copy(prev_states), (depth-1), best_score, enemytype)
                                visited += new_visits
                                known_sum += new_score
                                rem_child -= 1
                            #if not, stop searching and return -1000
                            else:
                                return (-1000, visited)
                        #if all children evaluated, calculate score and return
                        score += (known_sum/len(child_actions))
                        return (score, visited)
                    #treat human or tree AI as minimizing player (minimax)
                    else:
                        #check possible nodes
                        for action in child_actions:
                            new_board = np.copy(board_curr)
                            take_action(new_board, action)
                            #add child to prev_states 
                            prev = np.copy(prev_states)
                            if (len(prev)>=2):
                                if not (np.array_equal(board_curr, prev[-2])):
                                    prev_last = prev[-1]
                                    prev = np.array([prev_last, ])
                            np.append(prev, new_board, axis=0)
                            new_score, new_visits = eval_state(new_board, orig_player, new_player, np.copy(prev_states), (depth-1), best_score, enemytype)
                            visited += new_visits
                            #if node has lower score, better for current player
                            if (new_score < worst_score):
                                worst_score = new_score
                            #if it is impossible for current node to be better than previous best, stop searching and return -1000
                            if (worst_score < prev_best):
                                return (-1000, visited)
                        score += worst_score
    #return final discounted score and visit count
    score *= dis
    return (score, visited)
