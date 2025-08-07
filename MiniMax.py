from connect_four import Game
import numpy as np
from termcolor import colored, cprint
import sys

sys.setrecursionlimit(10000)

class Model():
    def __init__(self, MaxPlayer):
        self.MaxPlayer = MaxPlayer
        if MaxPlayer == 1:
            self.MinPlayer = 2
        else:
            self.MinPlayer = 1

    def __make_move(self, state, action):
        new_state = state.copy()
        turn = self.__change_turn(state)
        actions = self.__get_actions(state)
        if action in actions:
            col = action - 1
            for i in range(1, state.shape[0]+1):
                if new_state[-i, col] == 0:
                    new_state[-i, col] = turn
                    break
        return new_state
    
    def __change_turn(self, state):
        if np.sum(state != 0) % 2 == 0:
            return 1
        else:
            return 2
        
    def __winner_check(self, state):
        height = state.shape[0]
        width = state.shape[1]
        for row in range(height):
            for col in range(width - 3):
                if state[row, col] != 0 and state[row, col] == state[row, col + 1] == state[row, col + 2] == state[row, col + 3]:
                    return state[row, col]

        for col in range(width):
            for row in range(height - 3):
                if state[row, col] != 0 and state[row, col] == state[row + 1, col] == state[row + 2, col] == state[row + 3, col]:
                    return state[row, col]

        for row in range(height - 3):
            for col in range(width - 3):
                if state[row, col] != 0 and state[row, col] == state[row + 1, col + 1] == state[row + 2, col + 2] == state[row + 3, col + 3]:
                    return state[row, col]

        for row in range(height - 3):
            for col in range(3, width):
                if state[row, col] != 0 and state[row, col] == state[row + 1, col - 1] == state[row + 2, col - 2] == state[row + 3, col - 3]:
                    return state[row, col]

        return 0
        
    def __get_actions(self, state):
        mask = np.sum(state != 0, axis=0) != state.shape[0]
        return np.array([1, 2, 3, 4, 5, 6, 7])[mask]

    def eval_center(self, state):
        state_center = state[:-2, 2:-2]
        MaxPlayer_center = np.sum(state_center == self.MaxPlayer)
        MinPlayer_center = -np.sum(state_center == self.MinPlayer)

        return MaxPlayer_center + MinPlayer_center
    
    def eval_triple_double(self, hor_state, vert_state):
        hor_triplets = 0
        vert_triplets = 0
        right_diagonal_triplets = 0
        right_diagonal_doubles = 0
        left_diagonal_triplets = 0
        left_diagonal_doubles = 0
        hor_doubles = 0
        vert_doubles = 0

        #horizontal triplets
        for y in range(hor_state.shape[0]):
            for i in range(hor_state.shape[1]-2):
                if hor_state[y, i] == hor_state[y, i+1] == hor_state[y, i+2] and hor_state[y, i] != 0:
                    if i != 0 and i != hor_state.shape[1]-3:
                        if hor_state[y, i-1] == 0 or hor_state[y, i+3] == 0:
                            hor_triplets += 1 if hor_state[y, i] == self.MaxPlayer else -1
                    elif i == 0:
                        if hor_state[y, i+3] == 0:
                            hor_triplets += 1 if hor_state[y, i] == self.MaxPlayer else -1
                    elif i == hor_state.shape[1]-3:
                        if hor_state[y, i-1] == 0:
                            hor_triplets += 1 if hor_state[y, i] == self.MaxPlayer else -1

        #vertical triplets
        for y in range(vert_state.shape[0]):
            for i in range(vert_state.shape[1]-3):
                if vert_state[y, i] == vert_state[y, i+1] == vert_state[y, i+2] != 0 and vert_state[y, i+3] == 0:
                    vert_triplets += 1 if vert_state[y, i] == self.MaxPlayer else -1

        #horizontal doubles
        for y in range(hor_state.shape[0]):
            for i in range(hor_state.shape[1]-1):
                if hor_state[y, i] == hor_state[y, i+1] and hor_state[y, i] != 0:
                    if i != 0 and i != hor_state.shape[1]-2:
                        if (hor_state[y, i-1] == 0 or hor_state[y, i+2] == 0) and (hor_state[y, i-1] != hor_state[y, i] and hor_state[y, i+2] != hor_state[y, i]):
                            hor_doubles += 1 if hor_state[y, i] == self.MaxPlayer else -1
                    elif i == 0:
                        if hor_state[y, i+2] == 0:
                            hor_doubles += 1 if hor_state[y, i] == self.MaxPlayer else -1
                    elif i == hor_state.shape[1]-2:
                        if hor_state[y, i-1] == 0:
                            hor_doubles += 1 if hor_state[y, i] == self.MaxPlayer else -1

        #vertical doubles
        for y in range(vert_state.shape[0]):
            for i in range(vert_state.shape[1]-2):
                if (vert_state[y, i] == vert_state[y, i+1] != 0 and vert_state[y, i+2] == 0):
                    if i == 0:
                        vert_doubles += 1 if vert_state[y, i] == self.MaxPlayer else -1
                    else:
                        if vert_state[y, i-1] != vert_state[y, i]:
                            vert_doubles += 1 if vert_state[y, i] == self.MaxPlayer else -1

        #right-looking diagonal triplets
        for y in range(2, hor_state.shape[0]):
            for x in range(hor_state.shape[1]-2):
                if hor_state[y, x] == hor_state[y-1, x+1] == hor_state[y-2, x+2] and hor_state[y, x] != 0:
                    if 3 <= y <= 4 and 1 <= x <= hor_state.shape[1]-3:
                        try:
                            if hor_state[y+1, x-1] == 0:
                                right_diagonal_triplets += 1 if hor_state[y, x] == self.MaxPlayer else -1
                        except:
                            if hor_state[y-3, x+3] == 0:
                                right_diagonal_triplets += 1 if hor_state[y, x] == self.MaxPlayer else -1
                    elif y < hor_state.shape[0]-1 and x > 0:
                        if hor_state[y+1, x-1] == 0:
                            right_diagonal_triplets += 1 if hor_state[y, x] == self.MaxPlayer else -1
                    elif y > 2 and x < hor_state.shape[1]-3:
                        if hor_state[y-3, x+3] == 0:
                           right_diagonal_triplets += 1 if hor_state[y, x] == self.MaxPlayer else -1

        #right-looking diagonal doubles
        for y in range(1, hor_state.shape[0]):
            for x in range(hor_state.shape[1]-1):
                try:
                    if hor_state[y, x] == hor_state[y-1, x+1] == hor_state[y-2, x+2] != 0 or hor_state[y+1, x-1]:
                        continue
                except: pass
                if hor_state[y, x] == hor_state[y-1, x+1] != 0:
                    if 1 <= x <= hor_state.shape[1]-3 and 2 <= y <= hor_state.shape[0]-2:
                        if hor_state[y+1, x-1] == 0 or hor_state[y-2, x+2] == 0:
                            right_diagonal_doubles += 1 if hor_state[y, x] == self.MaxPlayer else -1
                    elif x <= hor_state.shape[1]-3 and y >= 2:
                        if hor_state[y-2, x+2] == 0:
                            right_diagonal_doubles += 1 if hor_state[y, x] == self.MaxPlayer else -1
                    elif x >= 1 and y <= hor_state.shape[0]-2:
                        if hor_state[y+1, x-1] == 0:
                            right_diagonal_doubles += 1 if hor_state[y, x] == self.MaxPlayer else -1

        #left-looking diagonal triplets
        for y in range(2, hor_state.shape[0]):
            for x in range(2, hor_state.shape[1]):
                if hor_state[y, x] == hor_state[y-1, x-1] == hor_state[y-2, x-2] and hor_state[y, x] != 0:
                    if 3 <= x <= hor_state.shape[1]-2 and 3 <= y <= 4:
                        if hor_state[y+1, x+1] == 0 or hor_state[y-3, x-3] == 0:
                            left_diagonal_triplets += 1 if hor_state[y, x] == self.MaxPlayer else -1
                    elif x >= 3 and 3 <= y <= 5:
                        if hor_state[y-3, x-3] == 0:
                            left_diagonal_triplets += 1 if hor_state[y, x] == self.MaxPlayer else -1
                    elif 2 <= x <= 5 and 2 <= y <= 4:
                        if hor_state[y+1, x+1] == 0:
                            left_diagonal_triplets += 1 if hor_state[y, x] == self.MaxPlayer else -1

        #left-looking diagonal doubles
        for y in range(1, hor_state.shape[0]):
            for x in range(1, hor_state.shape[1]):
                try:
                    if (hor_state[y, x] == hor_state[y-1, x-1] == hor_state[y-2, x-2] and hor_state[y, x] != 0) or hor_state[y+1, x+1] == hor_state[y, x]:
                        continue
                except: pass
                if hor_state[y, x] == hor_state[y-1, x-1] and hor_state[y, x] != 0:
                    if 2 <= x <= hor_state.shape[1]-2 and 2 <= y <= 4:
                        if hor_state[y+1, x+1] == 0 or hor_state[y-2, x-2] == 0:
                            left_diagonal_doubles += 1 if hor_state[y, x] == self.MaxPlayer else -1
                    elif x >= 2 and 2 <= y <= 5:
                        if hor_state[y-2, x-2] == 0:
                            left_diagonal_doubles += 1 if hor_state[y, x] == self.MaxPlayer else -1
                    elif 1 <= x <= 5 and 1 <= y <= 4:
                        if hor_state[y+1, x+1] == 0:
                            left_diagonal_doubles += 1 if hor_state[y, x] == self.MaxPlayer else -1

        return (hor_triplets, hor_doubles,
                vert_triplets, vert_doubles,
                right_diagonal_triplets, right_diagonal_doubles,
                left_diagonal_triplets, left_diagonal_doubles)


    def evaluate(self, state):
        #every row in hor_state represents 1 row)))
        #every row im vert_state represents 1 col and the first element of row in the vert_state is the lowest element in col in the original state and so on
        total_score = 0
        hor_state = state.copy()
        vert_state = np.array([row[::-1] for row in state.transpose()])

        hor_triplets, hor_doubles, vert_triplets, vert_doubles, right_diagonal_triplets, right_diagonal_doubles, left_diagonal_triplets, left_diagonal_doubles = self.eval_triple_double(hor_state, vert_state)
        center_score = self.eval_center(state)

        total_score += 2*vert_doubles + 3.5*vert_triplets
        total_score += 5*hor_triplets + 3*hor_doubles
        total_score += 3*(left_diagonal_triplets + right_diagonal_triplets)
        total_score += 2*(left_diagonal_doubles + right_diagonal_doubles)
        total_score += 0.25*(center_score)



        if self.__winner_check(state) == self.MaxPlayer:
            total_score += 5000
        elif self.__winner_check(state) == self.MinPlayer:
            total_score += -5000
        

        return total_score
    
    def minimax(self, state, depth):
        winner = self.__winner_check(state)
        if winner == self.MaxPlayer:
            return (1000-depth, state)
        elif winner == self.MinPlayer:
            return (-1000+depth, state)

        if depth == 0:
            return (self.evaluate(state), state)
        move_order = self.__change_turn(state)

        if move_order == self.MaxPlayer:
            maxeval = (-float('inf'), None)
            for child, action in self.get_childs(state):
                evaluation = (self.minimax(child, depth-1)[0], action)
                if maxeval[0] <= evaluation[0]:
                    maxeval = evaluation
            return maxeval
        else:
            mineval = (float('inf'), None)
            for child, action in self.get_childs(state):
                evaluation = (self.minimax(child, depth-1)[0], action)
                if mineval[0] > evaluation[0]:
                    mineval = evaluation
            return mineval

    def get_childs(self, state):
        actions = self.__get_actions(state)
        childs = [(self.__make_move(state, action), action) for action in actions]

        return childs

    
class GameFuncs(Game):
    def play(self, model: Model, depth):
        while True:
            self.print_colored_grid()
            if self.change_turn() == 1: turn_msg = 'Yellow'
            else: turn_msg = 'Red'
            print(f"{turn_msg} turn!")
            print(f"Possible moves: {self.get_actions()}")
            if self.change_turn() == model.MaxPlayer:
                move = model.minimax(self.get_grid(), depth)[1]
            else:
                move = int(input())
            self.make_move(move)

            game_status = self.check_game_status()
            if game_status == -1:
                cprint("Draw!", 'black', 'yellow')
                break
            elif game_status in [1, 2]:
                if game_status == 1: cprint(f"Player {int(game_status)} won!", 'yellow')
                else: cprint(f"Player {int(game_status)} won!", 'red')
                break
        self.print_colored_grid()

    def print_colored_state(self, state):
        for row in range(state.shape[0]):
            for col in range(state.shape[1]):
                if state[row, col] == 0: print(colored("■ ", 'white'), end='')
                elif state[row, col] == 1: print(colored("● ", 'yellow'), end='')
                else: print(colored("● ", 'red'), end='')
            print()


    


    
def main():
    model = Model(2)
    game = GameFuncs()
    game.play(model, 5)





if __name__ == "__main__":
    main()