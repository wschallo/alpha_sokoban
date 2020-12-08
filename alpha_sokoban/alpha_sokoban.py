from alpha_sokoban.input_parsing.read_input_files import get_board
from alpha_sokoban.finder import find_player_position_from_board
from alpha_sokoban.constants import MOVES, INVALID_TILE
from alpha_sokoban.board import board
from alpha_sokoban.helpers import check_if_valid_move_direction


class alpha_sokoban:
    def __init__(self, file_path_to_board):
        # Step 1) Load Board:
        self.board = board(get_board(file_name=file_path_to_board))

        # Step 2) Find Player Position:
        self.player_position = self.board.get_index_of_player()

    def check_if_player_can_make_direction_move(self, direction="u") -> bool:
        # Step 1): Check if direction is valid move:
        if not check_if_valid_move_direction(direction=direction):
            print("Warning: Invalid move encountered: {}".format(direction))
            return False

        # Step 2): Find new index position if move is made:
        delta_index = MOVES[direction]
        player_current_position = self.player_position
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


    def move_player(self, direction="u") -> bool:
        if self.check_if_player_can_make_direction_move(direction=direction):
            delta_index = MOVES[direction]
            player_current_position = self.player_position
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
                else:
                    print("Warning: Invalid tile type encountered, no move is being made.")


        else:
            print("Error: Unable to make move {}".format(direction))

