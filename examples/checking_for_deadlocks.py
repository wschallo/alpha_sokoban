import sys
sys.path.insert(1, '../alpha_sokoban')
from alpha_sokoban import alpha_sokoban

"""
Example:
########
#. #   #
#  $   #
#   # ##
## # $.#
#   $  #
#  .# @#
########
"""

if __name__ == "__main__":
    path_to_file = "../sample_input_files/sokoban01.txt"

    sokoban = alpha_sokoban(path_to_file)
    print("Display board:")
    sokoban.board.display_board()

    print("Case 1: No Deadlocks")
    print("Move UP")
    sokoban.move_player("U")
    sokoban.board.display_board()
    print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    print()

    print("Move Left")
    sokoban.move_player("L")
    sokoban.board.display_board()
    print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    print()

    print("Move Left")
    sokoban.move_player("L")
    sokoban.board.display_board()
    print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    print()

    print("Move L")
    sokoban.move_player("L")
    sokoban.board.display_board()
    print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    print()

    print("Move L")
    sokoban.move_player("L")
    sokoban.board.display_board()
    print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    print()

