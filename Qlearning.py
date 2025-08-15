import pandas as pd
from connect_four import Game, GameFuncs
from MiniMax import MiniMax
import numpy as np
from random import choice
from termcolor import cprint, colored
import random
import xxhash




class Qlearning():
    def __init__(self, MaxPlayer, L=1, y=1, start_e=0.5, end_e=0.1):
        index = pd.MultiIndex.from_tuples([], names=['state', 'action'])
        self.Qtable = pd.DataFrame(columns=['Qvalue'], index=index)

        self.learning_rate = L
        self.epsilon = start_e
        self.end_epsilon = end_e
        self.initial_value = 0
        self.discount_factor = y

        self.MaxEstimator = MiniMax(MaxPlayer)
        self.MinEstimator = MiniMax(1 if MaxPlayer == 2 else 2)
        self.MaxPlayer = MaxPlayer
        self.MinPLayer = 1 if MaxPlayer == 2 else 2



    def convert_state(self, state):
        str_state = ''.join([str(state[row, col]) for row in range(state.shape[0])
                                                   for col in range(state.shape[1])])
        bytes_state = str_state.encode('utf-8')
        hash_state = xxhash.xxh64(bytes_state).intdigest()

        return hash_state



    def Q(self, state, action):
        hash_state = self.convert_state(state)

        if (hash_state, action) not in self.Qtable.index:
            self.Qtable.loc[(hash_state, action), 'Qvalue'] = self.initial_value
        else:
            self.update_Qvalue(state, action)

    def get_Qvalue(self, state, action):
        hash_state = self.convert_state(state)
        if (hash_state, action) not in self.Qtable.index:
            return self.initial_value
        else:
            return self.Qtable.loc[(hash_state, action), 'Qvalue']

    def update_Qvalue(self, state, action):
        hash_state = self.convert_state(state)
        Qvalue = self.get_Qvalue(state, action)
        reward = self.estimate_reward(state, action)
        state_prime = GameFuncs.cls_make_move(state, action)
        best_prime_move = self.estimate_best_move(state_prime, pruning_soft_val=5, depth=5)
        if GameFuncs.cls_check_game_status(state_prime) == 0:
            Qvalue_prime = self.get_Qvalue(state_prime, best_prime_move)
        else:
            Qvalue_prime = 0



        new_Qvalue = Qvalue + self.learning_rate*(reward + self.discount_factor*Qvalue_prime - Qvalue)
        self.Qtable.loc[(hash_state, action), 'Qvalue'] = new_Qvalue



    def estimate_reward(self, state, action):
        state_prime = GameFuncs.cls_make_move(state, action)
        reward = self.MaxEstimator.evaluate(state_prime)

        return reward
    
    def estimate_best_move(self, state, depth=5, include_ab=True, pruning_soft_val=0):
        _, action = self.MaxEstimator.minimax(state, depth, include_ab, pruning_soft_val=pruning_soft_val)
        return action


    
    def make_decision(self, state):
        actions = GameFuncs.cls_get_actions(state)

        if self.epsilon < 0.01:
            weighted_choice = 'exploitation'
        else:
            weighted_choice = np.random.choice(['exploitation', 'exploration'], p=[1-self.epsilon, self.epsilon])
        hash_state = self.convert_state(state)
        print(f"This move {"was" if (hash_state) in self.Qtable.index else "wasnt"} in memory")
        if (hash_state) not in self.Qtable.index or weighted_choice == 'exploration': 
            action = choice(actions)
            return action
        elif weighted_choice == 'exploitation': 
            action = self.Qtable.loc[hash_state].idxmax().to_list()[0]
            return action   


    
    def learn(self, epochs: int, game_cls: Game, print_states=False):
        epsilon_decreasing_val = (self.epsilon - self.end_epsilon) / epochs
        for epoch in range(epochs):
            print(self.epsilon)
            self.epsilon -= epsilon_decreasing_val
            print("Epoch:", epoch)
            while True:
                state = game_cls.get_grid()
                action = self.make_decision(state)

                self.Q(state, action)
                game_cls.make_move(action)
                if print_states:
                    game_cls.print_colored_grid()
                if game_cls.check_game_status() != 0:
                    break
            game_cls.reset_grid()
    
    def save_Qtable(self, filename):
        self.Qtable.to_pickle(filename)

    def load_Qtable_from_pkl(self, filename):
        self.Qtable = pd.read_pickle(filename)

    def delete_pkl(self, filename):
        open(filename, "w").close()

    def play_with_AI(self, game_cls):
        while True:
            state = game_cls.get_grid()
            player = game_cls.change_turn()
            game_cls.print_colored_grid()
            turn_msg = "AI" if player == self.MaxPlayer else ("Yellow" if player == 1 else "Red")
            print(colored(f"{turn_msg} turn!", "yellow" if player == 1 else "red"))
            print(f"Possible moves: {game_cls.get_actions()}")
            if player == self.MaxPlayer:
                move = self.make_decision(state)
            else:                
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

    def update_Qtable(self, filename, epochs, print_states=False):
        self.load_Qtable_from_pkl(filename)
        self.learn(epochs, Game(), print_states=print_states)
        self.delete_pkl(filename)
        self.save_Qtable(filename)




    

        
def main():
    model = Qlearning(1, L=0.01, y=0.8, start_e=0.9, end_e=0.1)
    filename = "/Users/denis/Desktop/connect_four/Qtable.pkl"
    model.update_Qtable(filename, 50, print_states=True)

#3599 items, 56K memory capacity
#4547 items, 69K memory capacity
#6439 items, 96K memory capacity
#10688 items, 157K memory capacity

#DONT RUN ON HIGH AMOUNT OF EPOCHS


    


        
if __name__ == "__main__":
    main()

    






