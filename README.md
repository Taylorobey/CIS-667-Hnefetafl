# CIS-667-Hnefetafl

This project uses Matplotlib and Numpy:

https://numpy.org/doc/stable/index.html

https://matplotlib.org/

Hnefetafl_Helpers.py must be loaded before either the interactive or test programs

For the interactive program, run Play_Hnefetafl.py
The program will prompt for the board size and types of players
Empty spaces are the empty box character, restricted spaces are 'X', attackers are '1', defenders are '0', the king is 'K', and the throne is 'H'

For the tests, run Hnefetafl_Tests.py
The time for test completion grows a lot as board size increases, so if you want to run these yourself I'll point out easy changes that can influence completion time so that the larger ones can go faster (I'll probably end up changing these to paramaters for the test to try different configurations) :
Hnefetafl_Tests.py line 71 determines the number of tests
Hnefetafl_Tests.py line 73, the second parameter determines the default depth of the AI's search
Hnefetafl_Helpers.py line 431, mca determines the maximum number of actions chosen to be evaluated at each state
Hnefetafl_Helpers.py line 432, ft determines the depth at which the AI will choose to fully evaluate all children of a node
