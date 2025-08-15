from connect_four import Game, GameFuncs
import numpy as np
from termcolor import colored, cprint
import sys
import time

sys.setrecursionlimit(10000)
pruning_counter = 0

class MiniMax():
    def __init__(self, MaxPlayer):
        self.MaxPlayer = MaxPlayer
        if MaxPlayer == 1:
            self.MinPlayer = 2
        else:
            self.MinPlayer = 1

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


        winner = GameFuncs.cls_check_game_status(state)
        if winner == self.MaxPlayer:
            total_score += 5000 - np.sum(state != 0)
        elif winner == self.MinPlayer:
            total_score += -5000 + np.sum(state != 0)


        

        return total_score
    
    def minimax(self, state, depth, include_ab, alpha=-float('inf'), beta=float('inf'), pruning_soft_val=0):
        winner = GameFuncs.cls_check_game_status(state)
        if winner == self.MaxPlayer:
            return (5000 - depth, None)
        elif winner == self.MinPlayer:
            return (-5000 + depth, None)


        if depth == 0:
            return (self.evaluate(state), None)
        move_order = GameFuncs.cls_change_turn(state)

        if move_order == self.MaxPlayer:
            maxeval = (-float('inf'), None)
            for child, action in self.get_childs(state):
                evaluation = (self.minimax(child, depth-1, include_ab, alpha=alpha, beta=beta, pruning_soft_val=pruning_soft_val)[0], action)
                if maxeval[0] <= evaluation[0]:
                    maxeval = evaluation
                alpha = max(alpha, maxeval[0])
                if beta+pruning_soft_val <= alpha and include_ab:
                    break
            return maxeval
        else:
            mineval = (float('inf'), None)
            for child, action in self.get_childs(state):
                evaluation = (self.minimax(child, depth-1, include_ab, alpha=alpha, beta=beta, pruning_soft_val=pruning_soft_val)[0], action)
                if mineval[0] > evaluation[0]:
                    mineval = evaluation
                beta = min(beta, mineval[0])
                if beta+pruning_soft_val <= alpha and include_ab:
                    break
            
            return mineval

    def get_childs(self, state):
        actions = GameFuncs.cls_get_actions(state)
        childs = [(GameFuncs.cls_make_move(state, action), action) for action in actions]

        return childs
    
    def play_with_AI(self, game_cls, depth, prune_soft_val):
        reward, move = None, None
        while True:
            player = game_cls.change_turn()
            game_cls.print_colored_grid()
            turn_msg = "AI" if player == self.MaxPlayer else ("Yellow" if player == 1 else "Red")
            print(colored(f"{turn_msg} turn!", "yellow" if player == 1 else "red"))
            print(f"Possible moves: {game_cls.get_actions()}")
            if game_cls.change_turn() == self.MaxPlayer:
                reward, move = self.minimax(game_cls.get_grid(), depth, True, pruning_soft_val=prune_soft_val)
            else:
                #reward, move = self.minimax(game_cls.get_grid(), depth, False, pruning_soft_val=prune_soft_val)
                
                move = int(input())
            game_cls.make_move(move)
            


            game_status = game_cls.check_game_status()
            if game_status == -1:
                cprint("Draw!", 'black', 'yellow')
                break
            elif game_status in [1, 2]:
                if game_status != self.MaxPlayer:
                    cprint(f"Player {str(int(game_status))} won!", 'yellow' if game_status == 1 else 'red')
                else:
                    cprint(f"AI won!", 'yellow' if game_status == 1 else "red")
                break
        game_cls.print_colored_grid()



    
def main():
    game = Game()
    minimax = MiniMax(2)

    minimax.play_with_AI(game, 5, 5)













if __name__ == "__main__":
    main()
