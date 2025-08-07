import numpy as np
from termcolor import colored, cprint
from random import choice

class Game():
    def __init__(self):
        self.height, self.width = (6, 7)
        self.grid = np.zeros((6, 7))
        self.__actions = np.array([i for i in range(1, self.width+1)])  # yellow move first, yellow - 1, red - 2

    def print_colored_grid(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row, col] == 0: print(colored("■ ", 'white'), end='')
                elif self.grid[row, col] == 1: print(colored("● ", 'yellow'), end='')
                else: print(colored("● ", 'red'), end='')
            print()

    def check_game_status(self):
        if len(self.get_actions()) == 0:
            return -1
        return self.winner_check()
    
    def get_actions(self):
        mask = np.sum(self.grid != 0, axis=0) != self.height
        return self.__actions[mask]
    
    def change_turn(self):
        if np.sum(self.grid != 0) % 2 == 0:
            return 1
        else:
            return 2
        
    def winner_check(self):
        for row in range(self.height):
            for col in range(self.width - 3):
                if self.grid[row, col] != 0 and self.grid[row, col] == self.grid[row, col + 1] == self.grid[row, col + 2] == self.grid[row, col + 3]:
                    return self.grid[row, col]

        for col in range(self.width):
            for row in range(self.height - 3):
                if self.grid[row, col] != 0 and self.grid[row, col] == self.grid[row + 1, col] == self.grid[row + 2, col] == self.grid[row + 3, col]:
                    return self.grid[row, col]

        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if self.grid[row, col] != 0 and self.grid[row, col] == self.grid[row + 1, col + 1] == self.grid[row + 2, col + 2] == self.grid[row + 3, col + 3]:
                    return self.grid[row, col]

        for row in range(self.height - 3):
            for col in range(3, self.width):
                if self.grid[row, col] != 0 and self.grid[row, col] == self.grid[row + 1, col - 1] == self.grid[row + 2, col - 2] == self.grid[row + 3, col - 3]:
                    return self.grid[row, col]

        return 0


    def get_grid(self):
        return self.grid.copy()
    
    def set_grid(self, state):
        self.grid = state.copy()
    
    def make_move(self, action, state=None):
        turn = self.change_turn()
        actions = self.get_actions()
        if len(actions) == 0:
            self.__set_game_status(-1)
        if action in actions:
            col = action - 1
            for i in range(1, self.height+1):
                if self.grid[-i, col] == 0:
                    self.grid[-i, col] = turn
                    break
        else:
            raise "Impossible move!"
            
        
    def play(self):#●■
        while True:
            self.print_colored_grid()
            if self.change_turn() == 1: turn_msg = 'Yellow'
            else: turn_msg = 'Red'
            print(f"{turn_msg} turn!")
            print(f"Possible moves: {self.get_actions()}")
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

def main():
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
    
