import Hnefetafl_Helpers as hh
import numpy as np
import time

# Hnefetafl Game Interface

# main menu
# get input for board size and player type
players = [0,0]
print("Please choose one of the following:\n0: 7x7 board\n1: 9x9 board\n2: 11x11 board\n3: 13x13 board\n4: 15x15 board")
board_size = int(input())
print("Please choose a mode for player one:\n0: human\n1: simple ai\n2: tree-based ai")
players[0] = int(input())
print("Please choose a mode for player two:\n0: human\n1: simple ai\n2: tree-based ai")
players[1] = int(input())

# The attackers' side moves first; the players then take turns.
player_curr = 2

#play game
game_over = False
over = 0
board = hh.setup_board(hh.size_get(board_size))
print()
print("Initial board:")
print()
hh.display_board(board)
prev_states = np.array(board)
nodes = 0
print()
print("Press Enter to start.")
while(not game_over):
    #play game until end
    
    #play a turn
    act = [0,0,0,0]
    start = time.time()
    end = time.time()
    #if human player, prompt for choice
    if players[player_curr - 1] == 0:
        player_actions = hh.valid_actions(board, player_curr)
        #prompt to select piece
        print("Please choose a piece to move:")
        for i in range(len(player_actions)):
            print(str(i) + ": " + str(player_actions[i][0][0]+1) + chr(ord('A')+player_actions[i][0][1]))
        piece_select = int(input())
        #prompt for move to make
        print("Please choose a space to move to:")
        for i in range(len(player_actions[piece_select])):
            print(str(i) + ": " + str(player_actions[piece_select][i][2]+1) + chr(ord('A')+player_actions[piece_select][i][3]))
        move_select = int(input())
        act = player_actions[piece_select][move_select]

    #if simple AI, choose action 
    elif players[player_curr - 1] == 1:
        #wait for return to be pressed
        input()
        print("Processing...")
        act = hh.basic_AI(board, player_curr)        
        print()
    #if tree-based AI, choose action, choose action
    elif players[(player_curr - 1)] == 2:
        #wait for return to be pressed
        input()
        print("Processing...")
        start = time.time()
        act, nodes = hh.tree_AI(board, player_curr, prev_states, 3, players[(player_curr % 2)])
        end = time.time()
        print()
    #if there are no valid actions, current player loses
    if (act == [-1,-1,-1,-1]):
        over = (player_curr % 2) + 1
        game_over = True
    else:
        #take action
        hh.take_action(board, act)
        #add current state to prev_states list if it matches a relevant previous state, limit to 6 elements
        current_board = np.copy(board)
        if (len(prev_states)>=2):
            if not (np.array_equal(current_board, prev_states[-2])):
                prev_last = prev_states[-1]
                prev_states = np.array([prev_last, ])
        np.append(prev_states, current_board, axis=0)
        #check if game is over
        over = hh.game_over(board, player_curr, prev_states)
        if (over != 0):
            game_over = True
    #display board's current state
    print("Player " + str(player_curr) + "\'s move:")
    print()
    hh.display_board(board)
    print()
    print("Time: " + str(end - start) + "seconds")
    print("Nodes: "+ str(nodes))
    print()
    if (not game_over) and (players[player_curr - 1] != 0):
        print("Press Enter to continue.")
    #change players
    player_curr = (player_curr % 2) + 1
#print board last time
print()
print("Final board:")
print()
hh.display_board(board)
#declare winner
print("The winner is player" + str(over) + "!")
print("Final scores: ")
print("Player 1: " + str(hh.state_score(board, 1)))
print("Player 2: " + str(hh.state_score(board, 2)))
