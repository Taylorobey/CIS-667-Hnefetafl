import Hnefetafl_Helpers as hh
import AI_Implementation as aii
import numpy as np
import matplotlib.pyplot as plt
import torch as tr
import math
import random

MAX_DEPTH = 3
CHILDREN_PER_NODE = 5
WIN_WEIGHT = 3
LEARN_RATE = 2

#augment data with rotations and reflections, as board states' reflections and rotations are not different in terms of scoring
def augment(dataset):
    augmented = []
    for board, utility in dataset:
        for k in range(1,5):
            rot = np.rot90(board, k)
            augmented.append((rot, utility))
            augmented.append(((rot[:,::-1]), utility))
    return augmented

#generate a random board state
def random_board(moves, size):
    state = hh.setup_board(size)
    player = 2
    for i in range(moves):
        actions = hh.valid_actions(state, player)
        if len(actions) == 0: break
        action = actions[random.randrange(0, len(actions)-1)]
        hh.take_action(state, action)
        player = (player % 2) + 1
    return (state, player)

#generate dataset for training or testing
def dataset(amount, moves, size, player):
    data = []
    for i in range(amount):
        board = random_board(moves, size)
        utility = aii.eval_state(board[0], player, board[1], MAX_DEPTH, CHILDREN_PER_NODE, WIN_WEIGHT, LEARN_RATE, -100)
        #shrink utility of each state, allowing better fine-grain training
        data.append((board[0], (utility[0]/50)))
        print(i)
    return data

#encode states with one-hot encoding
def encode(board):
    # encoding[0,:,:] == 1 where there are "0"s, 0 elsewhere;                   empty
    # encoding[1,:,:] == 1 where there are "1"s or "2"s, 0 elsewhere;           restricted or throne
    # encoding[2,:,:] == 1 where there are "3"s, 0 elsewhere;                   attacker
    # encoding[3,:,:] == 1 where there are "4"s, 0 elsewhere;                   defender
    # encoding[4,:,:] == 1 where there are "5"s, "6"s, or "7"s, 0 elsewhere;    king

    #convert so that encoding doesn't need to recognize multiple values for spaces that are similar score-wise and rule-wise
    x = np.where((board==2), 1, board)
    x = np.where((x==3),2,x)
    x = np.where((x==4),3,x)
    x = np.where((x>=5),4,x)

    #one-hot encoding
    symbols = np.arange(5).reshape(-1,1,1)
    onehot = (symbols == x).astype(np.float32)

    return tr.tensor(onehot)

# Calculates the utility estimate square error for a batch of training examples
def batch_error(net, batch):
    states, utilities = batch
    u = utilities.reshape(-1,1).float()
    y = net(states)
    e = tr.sum((y - u)**2) / utilities.shape[0]
    return e

# network with two fully-connected layers and tanh activation function
# tried with sigmoid function, but tanh gets lower error(by a factor of ~500) and does so faster
class CNN(tr.nn.Module):
    def __init__(self, size, hid_features):
        super(CNN, self).__init__()
        #5 input channels, each an 11x11 2d array
        #use 3x3 filter
        self.to_hidden = tr.nn.Conv2d(5, hid_features, 3)
        #to_hidden results in a 9x9 2d array
        self.to_output = tr.nn.Linear(hid_features*(size-2)**2, 1)
    def forward(self, x):
        h = tr.relu(self.to_hidden(x))
        y = tr.tanh(self.to_output(h.reshape(x.shape[0],-1)))
        return y

# train the network on some generated data
def train_network(net, x, size, player):

    optimizer = tr.optim.SGD(net.parameters(), lr=0.00001, momentum=0.9)

    #example data
    training_examples = augment(dataset(x, 7, size, player))
    testing_examples = augment(dataset(x, 7, size, player))
    # Convert the states and their minimax utilities to tensors
    states, utilities = zip(*training_examples)
    training_batch = tr.stack(tuple(map(encode, states))), tr.tensor(utilities)

    states, utilities = zip(*testing_examples)
    testing_batch = tr.stack(tuple(map(encode, states))), tr.tensor(utilities)

    # Run the gradient descent iterations
    curves = [], []
    for epoch in range(2000):
    
        # zero out the gradients for the next backward pass
        optimizer.zero_grad()

        e = batch_error(net, training_batch)
        e.backward()
        training_error = e.item()

        with tr.no_grad():
            f = batch_error(net, testing_batch)
            testing_error = f.item()

        # take the next optimization step
        optimizer.step()    
        
        # print/save training progress
        if epoch % 100 == 0:
            print("%d: %f, %f" % (epoch, training_error, testing_error))
        curves[0].append(training_error)
        curves[1].append(testing_error)

    return (curves[0], curves[1])

def CNN_eval(net, board):
    with tr.no_grad():
        utility = net(encode(board).unsqueeze(0))
    return utility.item()

def CNN_choose_action(net, board, player):
    actions = hh.valid_actions(board, player)
    children = []
    for i in range(len(actions)):
        board_copy = np.copy(board)
        n = hh.take_action(board_copy, actions[i])
        children.append(n)
    utilities = map(lambda x: CNN_eval(net, x), children)
    return (actions[int(np.argmax(utilities))], len(actions))
