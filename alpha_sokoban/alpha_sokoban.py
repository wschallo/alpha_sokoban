from input_parsing.read_input_files import get_board
from finder import find_player_position_from_board
from constants import MOVES, INVALID_TILE
from board import board
from helpers import check_if_valid_move_direction
from deadlock_detection import deadlock_detector

import numpy as np


class alpha_sokoban:
    def __init__(self, file_path_to_board):
        # Step 1) Load Board:
        self.board = board(get_board(file_name=file_path_to_board))
        self.num_boxes = 0
        vals, counts = np.unique(self.board.integer_matrix, return_counts=True)
        for val, count in zip(vals,counts):
            if val == 2 or val == 5:
                self.num_boxes += counts[val]

        #2) Setup deadlock detector:
        self.deadlock = deadlock_detector(self.board.rows,self.board.cols)
        self.position_of_focus = (0,0)

    def is_there_a_deadlock(self):
        return self.deadlock.check_deadlock(self.board.integer_matrix,self.position_of_focus)

    def get_player_position(self):
        return self.board.get_index_of_player()

    def goal_test(self):
        if len(np.where(self.board.integer_matrix == 5)[0]) == self.num_boxes:
            return True
        else:
            return False

    def get_matrix(self):
        return self.board.integer_matrix

    def get_boxes(self):
        boxes = []
        coord = np.where(self.get_matrix() == 2)
        rows = coord[0]
        cols = coord[1]
        for row,col in zip(rows, cols):
            boxes.append((row, col))
        return boxes

    def get_storage(self):
        storage = []
        coord = np.where(self.get_matrix() == 3)
        rows = coord[0]
        cols = coord[1]
        for row,col in zip(rows, cols):
            storage.append((row, col))

        coord = np.where(self.get_matrix() == 6)
        rows = coord[0]
        cols = coord[1]
        for row,col in zip(rows, cols):
            storage.append((row, col))
        return storage


    def check_if_player_can_make_direction_move(self, direction="U") -> bool:
        # Step 1): Check if direction is valid move:
        if not check_if_valid_move_direction(direction=direction):
            print("Warning: Invalid move encountered: {}".format(direction))
            return False

        # Step 2): Find new index position if move is made:
        delta_index = MOVES[direction]
        player_current_position = self.get_player_position()
        player_position_after_move = (player_current_position[0] + delta_index[0],
                                      player_current_position[1] + delta_index[1])

        #Step 3) Check if can make move:
        ##  Case 1: player is moving to an empty square or a goal state:
        if self.board.is_open_space(player_position_after_move) or self.board.is_storage(player_position_after_move):
            return True
        ##  Case 2: player is trying to push a box (either box or box_on_storage):
        ##      Note: if case #2 occurs, check box is being pushed to empty square or goal
        elif self.board.is_box(player_position_after_move) or self.board.is_box_on_storage(player_position_after_move):
            return self.board.can_box_be_pushed_in_direction(box_position=player_position_after_move, direction=direction)
        else:
            return False


    def move_player(self, direction="U") -> bool:
        if self.check_if_player_can_make_direction_move(direction=direction):
            delta_index = MOVES[direction]
            player_current_position = self.get_player_position()
            player_position_after_move = (player_current_position[0] + delta_index[0],
                                          player_current_position[1] + delta_index[1])
            box_position_after_move = (player_position_after_move[0] + delta_index[0],
                                       player_position_after_move[1] + delta_index[1])


            #Case 1: Player is moving to open space:
            if self.board.is_open_space(player_position_after_move):
                ##  Case 1.a: Player is standing on open space (before move):
                if self.board.is_player(player_current_position):
                    self.board.set(player_current_position, 0) #set current to open_space (0)
                    self.board.set(player_position_after_move, 4)  # set after move to player (4)

                ##  Case 1.b: Player is standing on storage (before move):
                elif self.board.is_player_on_storage(player_current_position):
                    self.board.set(player_current_position, 3) #set current to storage (3)
                    self.board.set(player_position_after_move, 4)  # set after move to player (4)
                ## Case 1.c: Invalid tile (ERROR STATE: do nothing)
                else:
                    print("Warning: invalid current tile player is on at position {}".format(player_current_position))
            #Case 2: Player is moving to stand on storage:
            if self.board.is_storage(player_position_after_move):
                ##  Case 2.a: Player is standing on open space (before move):
                if self.board.is_player(player_current_position):
                    self.board.set(player_current_position, 0) #set current to open_space (0)
                    self.board.set(player_position_after_move, 6)  # set after player_on_storage (6)
                ##  Case 2.b: Player is standing on storage (before move):
                elif self.board.is_player_on_storage(player_current_position):
                    self.board.set(player_current_position, 3) #set current to storage (3)
                    self.board.set(player_position_after_move, 6)  # set after to player_on_storage (6)
                ## Case 2.c: Invalid tile (ERROR STATE: do nothing)
                else:
                    print("Warning: invalid current tile player is on at position {}".format(player_current_position))
            #Case 3: Player is trying to push box:
            if (self.board.is_box(player_position_after_move) or self.board.is_box_on_storage(player_position_after_move)) and \
                    self.board.can_box_be_pushed_in_direction(box_position=player_position_after_move, direction=direction):

                #If a box is able to be pushed, there are three tiles that need to be updated:
                #   | player_current_position | player_position_after_move | box_position_after_move |
                #example: after a move the board will update
                #   inital: |  @  |  $  |  .  |
                #   final: |     |  @  |  *  |

                player_current_position_becomes = INVALID_TILE
                player_position_after_move_becomes = INVALID_TILE
                box_position_after_move_becomes = INVALID_TILE

                ##Determine what player's current position becomes:
                if self.board.is_player(player_current_position):
                    player_current_position_becomes = 0 #set to open_space (0)
                elif self.board.is_player_on_storage(player_current_position):
                    player_current_position_becomes = 3 #set current to storage (3)
                else:
                    print("Warning: invalid current tile player is on at position {}".format(player_current_position))

                ##Determine what player's position after move becomes:
                if self.board.is_box(player_position_after_move):
                    player_position_after_move_becomes = 4 #set to player (4)
                elif self.board.is_box_on_storage(player_position_after_move):
                    player_position_after_move_becomes = 6 # set after player_on_storage (6)
                else:
                    print("Warning: invalid tile on player position after move {}".format(player_current_position))

                ##Determine what box position after move becomes:
                if self.board.is_open_space(box_position_after_move):
                    box_position_after_move_becomes = 2 #set to box (2)
                elif self.board.is_storage(box_position_after_move):
                    box_position_after_move_becomes = 5 #seet to box_on_storage (5)
                else:
                    print("Warning: invalid tile on box position after move {}".format(box_position_after_move))

                if INVALID_TILE not in [player_current_position_becomes, player_position_after_move_becomes, box_position_after_move_becomes]:
                    self.board.set(position=player_current_position, value=player_current_position_becomes)
                    self.board.set(position=player_position_after_move, value=player_position_after_move_becomes)
                    self.board.set(position=box_position_after_move, value=box_position_after_move_becomes)

                    self.position_of_focus = box_position_after_move
                else:
                    print("Warning: Invalid tile type encountered, no move is being made.")


        else:
            print("Error: Unable to make move {}".format(direction))





if __name__ == "__main__":
    path_to_file = '../sample_input_files/sokoban00.txt'

    sokoban = alpha_sokoban(path_to_file)

    sokoban.board.display_board()
    sokoban.move_player(direction="U")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="U")
    sokoban.move_player(direction="R")
    sokoban.move_player(direction="U")
    sokoban.move_player(direction="U")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="D")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="U")
    sokoban.move_player(direction="R")
    sokoban.move_player(direction="R")
    sokoban.move_player(direction="R")
    sokoban.move_player(direction="R")
    sokoban.move_player(direction="D")
    sokoban.move_player(direction="D")
    sokoban.move_player(direction="D")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="R")
    sokoban.move_player(direction="R")
    sokoban.move_player(direction="U")
    sokoban.move_player(direction="U")
    sokoban.move_player(direction="U")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="D")
    sokoban.move_player(direction="D")
    sokoban.move_player(direction="D")
    sokoban.move_player(direction="L")
    sokoban.move_player(direction="D")
    sokoban.move_player(direction="R")

    print("Display updated board:")
    sokoban.board.display_board()
    print(sokoban.get_player_position())
    