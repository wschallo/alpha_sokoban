import sys
sys.path.insert(1, '../alpha_sokoban')
from alpha_sokoban import alpha_sokoban

'''
########
#  .# .#
# $   @#
# $$## #
#     .#
########
'''

if __name__ == "__main__":
    path_to_file = "../sokoban_benchmarks/sokoban02.txt"

    sokoban = alpha_sokoban(path_to_file)
    print("Display board:")
    sokoban.board.display_board()

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

    print("Move DOWN")
    sokoban.move_player("D")
    sokoban.board.display_board()
    print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    print()

    print("Move Left")
    sokoban.move_player("L")
    sokoban.board.display_board()
    print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    print()

    print("Move UP")
    sokoban.move_player("UP")
    sokoban.board.display_board()
    print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    print()    

    # print("Move R")
    # sokoban.move_player("R")
    # sokoban.board.display_board()
    # print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    # print()

    # print("Move DOWN")
    # sokoban.move_player("D")
    # sokoban.board.display_board()
    # print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    # print()

    # print("Move Left")
    # sokoban.move_player("L")
    # sokoban.board.display_board()
    # print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    # print()

    # print("Move Left")
    # sokoban.move_player("L")
    # sokoban.board.display_board()
    # print("Is there a deadlock? {}".format(sokoban.is_there_a_deadlock()))
    # print()

    

