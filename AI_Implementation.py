import Hnefetafl_Helpers as hh
import numpy as np
import matplotlib.pyplot as pt
import math
import random

#Ai implementations

# basic AI
def basic_AI(board_curr, player):
    #choose actions at random
    basic_actions = hh.valid_actions(board_curr, player)
    if(not basic_actions):
        return ([-1,-1,-1,-1], 0)
    elif len(basic_actions) == 1:
        return (basic_actions[0], 1)
    else:
        ind = random.randrange(0, len(basic_actions)-1)
        return (basic_actions[ind], len(basic_actions))

# tree-based AI
def tree_AI(board_curr, player, max_depth, children_per_node, win_weight, learn_rate):

    side_size = int(math.sqrt(board_curr.size))
    #possible actions
    tree_actions = hh.valid_actions(board_curr, player)
    search_count = min(children_per_node, len(tree_actions))
    scores = []
    visits = []
    evals = []
    actions = []
    cap_actions = []
    child_actions = []

    #no valid moves
    if(len(tree_actions)==0):
        return ([-1,-1,-1,-1], 0)
    #valid moves
    else:
        #get score and visited nodes for each possible move from this board state
        #using eval, then pick highest scoring node
        children = []
        captures = []

        #pick random unique children until either all have been picked or search count is reached
        for i in range(search_count):
            board_copy = np.copy(board_curr)
            n = tree_actions.pop(random.randrange(len(tree_actions)))
            m = hh.take_action(board_copy, n)
            if (m):
                captures.append(board_copy)
                cap_actions.append(n)
            else:
                children.append(board_copy)
                child_actions.append(n)
        #captures = np.array([i for i in captures if i.size>0])
        
        #set initial previous best to -100 so that at least one child will be chosen by evaluation (avoiding total pruning)
        #prioritize capturing moves
        if (len(captures) >0):
            actions = cap_actions
            for cap in captures:
                evals.append(eval_state(cap, player, ((player % 2) + 1), max_depth, children_per_node, win_weight, learn_rate, -100))
        else:
            #children = np.array([i for i in children if i.size>0])
            actions = child_actions
            for child in children:
                evals.append(eval_state(child, player, ((player % 2) + 1), max_depth, children_per_node, win_weight, learn_rate, -100))
        if (evals):
                scores, visits = map(list, zip(*evals))
        return (actions[int(np.argmax(scores))], sum(visits))

#score state based on remaining pieces
#winning states get higher score
def state_score(board, player, win_weight):
    #return number of pieces belonging to player, minus pieces belonging to opponent
    score_1 = np.count_nonzero(board==4)
    score_2 = np.count_nonzero(board==3)
    score_return = 0
    if (player==1):
        score_return = (score_1 - score_2)
    else:
        score_return = (score_2 - score_1)
    # if this state is a winning configuration for the current player, multiply score by win_weight
    if (hh.game_over(board, player) != 0):
        if (hh.game_over(board, player) == player):
            score_return = abs(score_return * win_weight)
        else:
            score_return = -abs(score_return * win_weight)
    return score_return

#score evaluation for a given board state
#limited depth expectimax
def eval_state(board_curr, orig_player, player, max_depth, children_per_node, win_weight, learn_rate, prev_best):
    side_size = int(math.sqrt(board_curr.size))
    #learning discount; as eval calls get passed smaller max_depth, scores will become less weighted
    dis = max_depth/learn_rate
    #calculate score of this state
    score = state_score(board_curr, orig_player, win_weight)
    #maximum/minimum possible score for players (does not include king in score count, as it is always assumed to be on board if game has not ended)
    max_score = [(win_weight * 4 * (int(side_size/4))), (win_weight * 8 * (int(side_size/4)))]
    min_score = [(-win_weight * 8 * (int(side_size/4))), (-win_weight * 4 * (int(side_size/4)))]
    #record number of nodes/states visited (start at 1 for this one)
    visited = 1
    #limited depth minimax/expectimax evaluation, value wins highly positive and losses highly negative
    #base case, hit depth limit or game is in game_over state
    if (max_depth == 0) or (hh.game_over(board_curr, player) != 0):
        return (score, visited)
    else:
        #possible actions
        child_actions = hh.valid_actions(board_curr, player)
        if (len(child_actions)>0):
            new_player = (player % 2) + 1

            #track current score for pruning purposes, set initially to worse than worst case for each
            best_score = min_score[player - 1] * 1.5
            worst_score = max_score[player -1] * 1.5

            #for defender, check to see if king can reach edge
            if (player==1):
                king_actions = [(a,b,c,d) for a,b,c,d in child_actions if (board_curr[a][b] > 5)]
                king_nodes = 0
                for k_action in king_actions:
                    king_board = np.copy(board_curr)
                    hh.take_action(king_board, k_action)
                    king_nodes += 1
                    if (hh.game_over(king_board, player))==player:
                        return (state_score(king_board, player, win_weight), (visited + king_nodes))
                visited += king_nodes
           
            
            new_actions = []
            if (len(child_actions) > children_per_node):
                while(len(new_actions) < children_per_node):
                    new_actions.append(child_actions.pop(random.randrange(len(child_actions))))
                child_actions = new_actions

            #if currently the original player, simply check all remaining child nodes
            if (orig_player==player):
                for action in child_actions:
                    new_board = np.copy(board_curr)
                    hh.take_action(new_board, action)
                    new_score, new_visits = eval_state(new_board, orig_player, new_player, (max_depth-1), children_per_node, win_weight, learn_rate, prev_best)
                    visited += new_visits
                    #best possible score update
                    if (new_score > best_score):
                        best_score = new_score
                score += best_score
            #if current player is the opponent, evaluate all children, but check for possible pruning
            #if it is impossible for current node to be better than previous best, stop searching and return -1000
            else:
                #if enemy is simple AI, model probabilistically with all actions being equally probable (expectimax)
                known_sum = 0
                rem_child = len(child_actions)
                for action in child_actions:
                    #check if higher score is possible
                    if (prev_best < ((known_sum + (rem_child * max_score[player-1]))/len(child_actions))):
                        #if it is, evaluate child
                        new_board = np.copy(board_curr)
                        hh.take_action(new_board, action)
                        new_score, new_visits = eval_state(new_board, orig_player, new_player, (max_depth-1), children_per_node, win_weight, learn_rate, prev_best)
                        visited += new_visits
                        known_sum += new_score
                        rem_child -= 1
                    #if not, stop searching and return -1000
                    else:
                        return (-1000, visited)
                #if all children evaluated, calculate score and return
                score += (known_sum/len(child_actions))
                #treat human or tree AI as minimizing player (minimax) ???
    #return final discounted score and visit count
    score *= dis
    return (score, visited)