import Hnefetafl_Helpers as hh
import numpy as np
import matplotlib.pyplot as plt
import time


#Conduct 5 experiments, one for each problem size.
#For each problem size, simulate 100 games, in which the baseline AI plays against the tree-based AI.  If the domain is single-player, run 100 games with the baseline and another 100 with the tree-based AI.
#Record the number of nodes processed by the tree-based AI over the course of each game.
#Record the final score for the tree-based and baseline AIs at the end of each game.
#Create two histograms for each problem size: one showing the distribution of node counts, and one showing the distribution of final scores for each AI, across the 100 games.

def test_play(board_size, depth):
    # The attackers' side moves first; the players then take turns.
    players = [2,1]
    player_curr = 2
    times = []

    #play game
    game_over = False
    over = 0
    board = hh.setup_board(hh.size_get(board_size))
    prev_states = np.array(board)
    nodes = 0
    while(not game_over):
        #play game until end
    
        #play a turn
        act = [0,0,0,0]
        start = time.time()
        end = time.time()
        #if simple AI
        if players[player_curr - 1] == 1:
            act = hh.basic_AI(board, player_curr)        
        #if tree-based AI
        elif players[(player_curr - 1)] == 2:
            start = time.time()
            act, new_nodes = hh.tree_AI(board, player_curr, prev_states, depth, players[(player_curr % 2)])
            nodes += new_nodes
            end = time.time()
            times.append((end-start))

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
        #change players
        player_curr = (player_curr % 2) + 1
    return (max(times), nodes, over, (hh.state_score(board, 2)))


for i in range(0,5):
    max_times = []
    node_counts = []
    tree_scores = []
    tree_wins = []
    for j in range(100):
        starter = time.time()
        game_results = test_play(i, 7)
        ender = time.time()
        max_times.append(game_results[0])
        node_counts.append(game_results[1])
        tree_wins.append(game_results[2])
        tree_scores.append(game_results[3])
        print("Game " + str(j) + " time: " + str(ender - starter))
    print("Max time: " + str(max(max_times)))
    figure, axis = plt.subplots(1,2)
    axis[0].hist(node_counts, bins=100, rwidth=0.9)
    axis[0].set_title("Node Counts")
    axis[1].hist(tree_scores, bins=100, rwidth=0.9)
    axis[1].set_title("Tree AI Scores")
    plt.show()
    input()