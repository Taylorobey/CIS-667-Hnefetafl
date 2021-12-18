# CIS-667-Hnefetafl

## Existing Code

This project uses the following libraries:

[numpy](https://numpy.org/doc/stable/index.html)

[matplotlib](https://matplotlib.org/)

[pytorch](https://pytorch.org/)

## Running Project

For any running environment in which the order of files matters, follow this order:

Hnefetafl_Helpers.py -> AI_Implementation.py -> CNN_AI_Implementation.py -> Hnefetafl_Tests.py/Play_Hnefetafl.py

### Interactive Domain

For the interactive program, run Play_Hnefetafl.py

The program will prompt for the board size and types of players. Player 1 is the defender, and player 2 is the attacker.

Empty spaces are the empty box character, restricted spaces are 'X', attackers are '1', defenders are '0', the king is 'K', and the throne is 'H'.

If a human is playing, the interface will prompt them to choose a piece to move, then a location to move the piece to.

The rules of play are as follows:

* The attacker (player 2) goes first. Players alternate turns. A player may move one piece on their turn
* Pieces can move any number of spaces in a cardinal direction. Pieces cannot move through other pieces, and pieces other than the King cannot end a move on a restricted space
* If a piece ends its move such that an enemy is adjacent to it, and the space opposite that enemy is either an ally or a restricted space, the enemy is captured and removed from the board.
* The king has one special case; if he is on or next to the throne, he must be surrounded on all 4 sides to be captured. (The throne counts as a restricted space)
* If the King is captured, the attackers win. If the King reaches the edge of the board, the defenders win.

### Running Tests

For the tests, run Hnefetafl_Tests.py.

The tests are encapsulated in functions, so the last lines calling them can be commented out if you wish to run one of the two types of test.

The time for test completion grows a lot as board size increases, so if you want to run these yourself I'll point out easy changes that can influence completion time so that the larger ones can go faster:

Hnefetafl_Helpers.py lines 9-12;    
determines the default variables used for the depth of search, number of children searched at each depth, win weight, and learn rate

Hnefetafl_Tests.py line 65;         
determines the number of tests for each board size for tree_test()

Hnefetafl_Tests.py line 111;        
determines the number of tests for NN_test()
