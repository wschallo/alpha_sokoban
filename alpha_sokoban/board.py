from constants import TILE_SYMBOLS, INVALID_TILE_SYMBOL, INVALID_TILE, MOVES, TILE_TYPES
from finder import find_player_position_from_board
from helpers import check_if_valid_move_direction

class board:
    def __init__(self, board_matrix):
        self.integer_matrix = board_matrix
        self.shape = self.integer_matrix.shape
        (self.rows, self.cols) = self.shape

    def __getitem__(self,key):
        return self.integer_matrix[key]

    def display_board(self):
        for i in range(self.rows):
            to_print = []
            for j in range(self.cols):
                val = self.integer_matrix[i][j]
                if val in TILE_SYMBOLS:
                    to_print.append(TILE_SYMBOLS[val])
                else:
                    to_print.append(INVALID_TILE_SYMBOL)
            output = " ".join(to_print)
            print(output)

    def get_index_of_player(self):
        return find_player_position_from_board(self.integer_matrix)

    def get_tile_from_position(self,position):
        if len(position) == 2:
            return self.integer_matrix[position[0]][position[1]]
        else:
            print("Warning: invalid position index {}".format(position))
            return INVALID_TILE

    def is_open_space(self,position):
        return self.get_tile_from_position(position) == 0

    def is_wall(self,position):
        return self.get_tile_from_position(position) == 1

    def is_box(self, position):
        return self.get_tile_from_position(position) == 2

    def is_storage(self, position):
        return self.get_tile_from_position(position) == 3

    def is_player(self, position):
        return self.get_tile_from_position(position) == 4

    def is_box_on_storage(self, position):
        return self.get_tile_from_position(position) == 5

    def is_player_on_storage(self, position):
        return self.get_tile_from_position(position) == 6

    def can_box_be_pushed_in_direction(self, box_position, direction):
        if check_if_valid_move_direction(direction):
            box_delta = MOVES[direction]
            box_new_position = (box_position[0] + box_delta[0], box_position[1] + box_delta[1])

            return self.is_open_space(box_new_position) or self.is_storage(box_new_position)
        else:
            print("Warning: Invalid move encountered {}".format(direction))
            return False

    def set(self, position, value) -> bool:
        if value in TILE_TYPES.keys():
            if len(position) == 2:
                self.integer_matrix[position[0]][position[1]] = value
                return True
            else:
                print("Warning: invalid position encountered {}".format(position)) #TODO: make this more robust
                return False
        else:
            print("Warning: invalid tile value encountered {}".format(value))
            return False



"""
TILE_TYPES = {0: 'open_space',
              1: 'wall',
              2: 'box',
              3: 'storage',
              4: 'player',
              5: 'box_on_storage',
              6: 'player_on_storage'}
"""

