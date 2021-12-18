import Hnefetafl_Helpers as hh
import AI_Implementation as aii
import CNN_AI_Implementation as cnn
import numpy as np
import matplotlib.pyplot as plt
import time
import copy

MAX_DEPTH = 3
CHILDREN_PER_NODE = 5
WIN_WEIGHT = 3
LEARN_RATE = 2

#Conduct 5 experiments, one for each problem size.
#For each problem size, simulate 100 games, in which the baseline AI plays against the tree-based AI.  If the domain is single-player, run 100 games with the baseline and another 100 with the tree-based AI.
#Make sure the 100 games are not all identical (for example, using different initial states, or playing against a non-deterministic baseline).
#Record the number of nodes processed by the tree-based AI over the course of each game.
#Record the final score for the tree-based and baseline AIs at the end of each game.
#Create two histograms for each problem size: one showing the distribution of node counts, and one showing the distribution of final scores for each AI, across the 100 games.

def test_play(board_size, max_depth, children_per_node, win_weight, learn_rate, main_player, net=None):
    # The attackers' side moves first; the players then take turns.
    players = [main_player,1]
    player_curr = 2

    #play game
    game_over = False
    over = 0
    board = hh.setup_board(hh.size_get(board_size))
    prev_states = np.array(board)
    nodes = 0
    simple_nodes = 0
    while(not game_over):
        #play game until end
    
        #play a turn
        act = [0,0,0,0]
        #if simple AI
        if players[player_curr - 1] == 1:
            act, new_nodes = aii.basic_AI(board, player_curr)
            simple_nodes += new_nodes
        #if tree-based AI
        elif players[(player_curr - 1)] == 2:
            act, new_nodes = aii.tree_AI(board, player_curr, max_depth, children_per_node, win_weight, learn_rate)
            nodes += new_nodes
        #if CNN AI
        elif players[(player_curr - 1)] == 3:
            act, new_nodes = cnn.CNN_choose_action(net, board, player_curr)
            nodes += new_nodes
        #if there are no valid actions, current player loses
        if (act == [-1,-1,-1,-1]):
            over = (player_curr % 2) + 1
            game_over = True
        else:
            #take action
            hh.take_action(board, act)
            #check if game is over
            over = hh.game_over(board, player_curr)
            if (over != 0):
                game_over = True
        #change players
        player_curr = (player_curr % 2) + 1
    return (nodes, simple_nodes, (aii.state_score(board, 1, 1)))

def tree_test():
    tree_nodes = []
    tree_scores = []
    simple_nodes = []
    #board sizes 0-4
    for i in range(5):
        #simulate 100 games
        for j in range(100):
            print(str(i) + ", " + str(j))
            nodes, snodes, score = test_play(i, MAX_DEPTH, CHILDREN_PER_NODE, WIN_WEIGHT, LEARN_RATE, 2)
            tree_nodes.append(nodes)
            simple_nodes.append(snodes)
            tree_scores.append(score)

        simple_scores = copy.deepcopy(tree_scores)
        simple_scores = [x * -1 for x in simple_scores]

        plt.hist([tree_nodes, simple_nodes], color=['blue', 'red'], lw=0, bins=30, label=['Tree AI nodes', 'Simple AI nodes'])
        plt.legend(loc='upper right')
        plt.xlabel('Nodes Visited')
        plt.ylabel('Games')
        plt.show()

        plt.hist([tree_scores, simple_scores], color=['blue', 'red'], lw=0, bins=30, label=['Tree AI scores', 'Simple AI scores'])
        plt.legend(loc='upper right')
        plt.xlabel('Score')
        plt.ylabel('Games')
        plt.show()

        tree_nodes = []
        tree_scores = []
        simple_nodes = []

    return 0

def NN_test():
    #Generating a training and testing dataset, each with at least 500 examples. Each example should be a random game state, encoded as an array of numbers (used as input for the NN), paired with some target output for the NN, such as the utility or heuristic value of the game state.

    #Configure and train the neural network on the training data, and evaluate on the test data, for at least 500 gradient descent weight updates. You should evaluate on the test data every update, but only the training data should be used to calculate the error gradient with respect to the weights. Plot the learning curve showing update iteration on the x-axis and error on the y-axis (one curve for training error, one for test error).
    net = cnn.CNN(11, 4)

    train_curve, test_curve = cnn.train_network(net, 100, 11, 1)

    plt.plot(train_curve, 'b-')
    plt.plot(test_curve, 'r-')
    plt.plot()
    plt.legend(["Train","Test"])
    plt.xlabel('Gradient Updates')
    plt.ylabel('Error')
    plt.show()

    #After training, simulate 100 games using the trained NN incorporated into the tree-based AI. Play it against the baseline AI if your game is two-player. Record and plot the same data as before: number of nodes processed and final scores for each AI. Again, make sure the 100 games are not all identical.
    net_nodes = []
    simple_nodes = []
    net_scores = []
    for i in range(100):
        print(i)
        nodes1, nodes2, final_score = test_play(2, MAX_DEPTH, CHILDREN_PER_NODE, WIN_WEIGHT, LEARN_RATE, 3, net)
        net_nodes.append(nodes1)
        simple_nodes.append(nodes2)
        net_scores.append(final_score)
    simple_scores = copy.deepcopy(net_scores)
    simple_scores = [x * -1 for x in simple_scores]

    plt.hist([net_nodes, simple_nodes], color=['blue', 'red'], lw=0, bins=30, label=['CNN nodes', 'Simple AI nodes'])
    plt.legend(loc='upper right')
    plt.xlabel('Nodes Visited')
    plt.ylabel('Games')
    plt.show()

    plt.hist([net_scores, simple_scores], color=['blue', 'red'], lw=0, bins=30, label=['CNN scores', 'Simple AI scores'])
    plt.legend(loc='upper right')
    plt.xlabel('Score')
    plt.ylabel('Games')
    plt.show()

    return 0

#uncomment to run tests
tree_test()
#NN_test()