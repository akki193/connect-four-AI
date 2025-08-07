# connect-four-AI
an AI for connect four game, implemented Minimax algorithm

FUTURE IDEAS AND MAIN INFORMATION
Connect four was recreated fully with python where gameboard represented with 2 dim numpy grid
In corresponding file for Minimax algorithm was made evaluate() function that calculate const value of the game position and the Minimax algorithm by itself, maybe in the future i will implement alpha beta in Minimax and uses this to train Qlearning model

COLOR OF THE PLAYER
To play against AI run MiniMax.py, to change the color of player open the file and change parameter of the model(model = Model(2)) to 1 if you want to move first, or keep it on 2 if you want to move second.

DEPTH
To change the depth of the algorithm change the second parameter of the GameFuncs.play() to desired depth(Warning! if depth more than 5 the model can think realy long time)
