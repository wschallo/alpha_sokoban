from alpha_sokoban import alpha_sokoban
import sys
import os.path
from constants import MOVES

def play_sokoban(path_to_file):
    sokoban = alpha_sokoban(path_to_file)

    while True:
        print()
        sokoban.board.display_board()

        if sokoban.goal_test():
            print("Solved!")
            break

        valid_moves = []
        for each_move in MOVES.keys():
            if sokoban.check_if_player_can_make_direction_move(each_move):
                valid_moves.append(each_move)
        print("VALID MOVES: {}".format(" ".join(valid_moves)))
        print("(or type N to reset of Q to quit)")
        get_input = input("Command:")
        the_input = get_input.strip().upper()[0]
        if the_input == "N":
            return True
        elif the_input == "Q":
            return False
        else:
            if the_input in valid_moves:
                sokoban.move_player(the_input)
            elif the_input in MOVES.keys():
                print("Error: {} is not a valid move".format(the_input))
            else:
                print("Error: {} is an unrecognized command.".format(the_input))

    command = input("Would you like to replay this level? Y or N")
    if command.strip().upper()[0] == "Y":
        return True
    else:
        return False


def run_play_sokoban(path_to_file):
    play_again = True

    while play_again:
        play_again = play_sokoban(path_to_file)

if __name__ == "__main__":
    if len(sys.argv) >= 1:
        path_to_file = sys.argv[-1]
        if os.path.isfile(path_to_file):
            run_play_sokoban(path_to_file)



        else:
            print("ERROR: Input file {} could not be found".format(path_to_file))
    else:
        print("ERROR: run_search.py requires as a command line argument a path to a sokoban map file (i.e. sokoban01.txt).")