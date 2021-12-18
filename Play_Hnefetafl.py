import Hnefetafl_Helpers as hh
import AI_Implementation as aii
import CNN_AI_Implementation as cnn
import numpy as np
import math
import time

# Hnefetafl Game Interface

# constants for playing base game
MAX_DEPTH = 3
CHILDREN_PER_NODE = 5
WIN_WEIGHT = 3
LEARN_RATE = 2

# main menu
# get input for board size and player type
players = [0,0]
print("Please choose one of the following:\n0: 7x7 board\n1: 9x9 board\n2: 11x11 board\n3: 13x13 board\n4: 15x15 board")
board_size = int(input())
print("Please choose a mode for player one (defender):\n0: Human\n1: Simple AI\n2: Tree-Based AI\n3: Tree + Neural Network")
players[0] = int(input())
print("Please choose a mode for player two (attacker):\n0: Human\n1: Simple AI\n2: Tree-Based AI\n3: Tree + Neural Network")
players[1] = int(input())

#train CNN if it is chosen
if (players[0] == 3):
    print ("PLease wait while neural network is trained")
    net1 = cnn.CNN(hh.size_get(board_size), 4)
    cnn.train_network(net1, 100, hh.size_get(board_size), 1)
    print()
elif (players[1] == 3):
    print ("PLease wait while neural network is trained")
    net2 = cnn.CNN(hh.size_get(board_size), 4)
    cnn.train_network(net2, 100, hh.size_get(board_size), 2)
    print()
else:
    net1 = None
    net2 = None

# The attackers' side moves first; the players then take turns.
player_curr = 2

#play game
game_over = False
over = 0
nodes = 0
simple_nodes = 0
board = hh.setup_board(hh.size_get(board_size))
#play game until ends
while(not game_over):
    print()
    hh.display_board(board)
    print()
    side_size = int(math.sqrt(board.size))
    act = [0,0,0,0]
    start = time.time()
    end = time.time()
    #play a turn
    #if human player, prompt for choice
    if players[player_curr - 1] == 0:
        player_actions = hh.valid_actions(board, player_curr)
        player_pieces = set()
        #get pieces with valid moves
        for i in player_actions:
            player_pieces.add((i[0], i[1]))
        player_piece = sorted(list(player_pieces), key = lambda x: (x[1], x[0]))
        #prompt to select piece
        print("Please choose a piece to move:")
        selector = 0
        for i in player_piece:
            if (selector%4 == 3):
                a = '\n'
            else:
                a = '\t'
            print(str(selector) + ": " , end='')
            if (len(player_piece)> 9) and (selector < 10):
                print(' ', end='')
            print(chr(ord('A')+i[1]) + str(side_size-i[0]), end=a)
            selector += 1
        piece_select = int(input())
        #prompt for move to make
        player_moves = sorted([x for x in player_actions 
                               if ((x[0]==player_piece[piece_select][0]) and (x[1]==player_piece[piece_select][1]))],
                              key = lambda x: (x[3], x[2]))
        print()
        print("Please choose a space to move to:")
        selector = 0
        for i in player_moves:
            if (selector%4 == 3):
                a = '\n'
            else:
                a = '\t'
            print(str(selector) + ": " , end='')
            if (len(player_piece)> 9) and (selector < 10):
                print(' ', end='')
            print(chr(ord('A')+i[3]) + str(side_size-i[2]), end=a)
            selector += 1
        move_select = int(input())
        act = player_moves[move_select]

    #if simple AI, choose action 
    elif players[player_curr - 1] == 1:
        #wait for return to be pressed
        print("Press Enter to continue.")
        input()
        print("Processing...")
        act, nodes = aii.basic_AI(board, player_curr)
        print()
    #if tree-based AI, choose action, choose action
    elif players[(player_curr - 1)] == 2:
        #wait for return to be pressed
        print("Press Enter to continue.")
        input()
        print("Processing...")
        start = time.time()
        act, nodes = aii.tree_AI(board, player_curr, MAX_DEPTH, CHILDREN_PER_NODE, WIN_WEIGHT, LEARN_RATE)
        end = time.time()
        print()
     #if CNN AI
    elif players[(player_curr - 1)] == 3:
        #wait for return to be pressed
        print("Press Enter to continue.")
        input()
        print("Processing...")
        start = time.time()
        if (player_curr == 1):
            act, nodes = cnn.CNN_choose_action(net1, board, 1)
        elif (player_curr == 2):
            act, nodes = cnn.CNN_choose_action(net2, board, 2)
        end = time.time()
        print()
    #if there are no valid actions, current player loses
    if (act == [-1,-1,-1,-1]):
        over = (player_curr % 2) + 1
        game_over = True
        print("Player " + str(player_curr) + " has no valid actions.")
        print()
    else:
        #take action
        hh.take_action(board, act)
        #check if game is over
        over = hh.game_over(board, player_curr)
        if (over != 0):
            game_over = True
        print()
        print("Player " + str(player_curr) + "\'s move: " + chr(ord('A')+act[1]) + str(side_size-act[0]) + " -> " + 
              chr(ord('A')+act[3]) + str(side_size-act[2]))
        if (not game_over) and (players[player_curr - 1] != 0):
            print("Time: " + str(end - start) + " seconds")
            print("Nodes: "+ str(nodes))
        print()
    #change players
    player_curr = (player_curr % 2) + 1
    nodes = 0
#print board last time
print()
print("Final board:")
print()
hh.display_board(board)
#declare winner
print("The winner is player " + str(over) + "!")
print("Final scores: ")
print("Player 1: " + str(aii.state_score(board, 1, 1)))
print("Player 2: " + str(aii.state_score(board, 2, 1)))
