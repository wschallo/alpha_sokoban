from alpha_sokoban.alpha_sokoban import alpha_sokoban

if __name__ == "__main__":
    path_to_file = "../sample_input_files/sokoban00.txt"

    sokoban = alpha_sokoban(path_to_file)

    print("1) Display board:")
    sokoban.board.display_board()

    print("2) Check for valid moves:")
    print("     Can player move up? {}".format(sokoban.check_if_player_can_make_direction_move("u")))
    print("     Can player move down? {}".format(sokoban.check_if_player_can_make_direction_move("d")))
    print("     Can player move left? {}".format(sokoban.check_if_player_can_make_direction_move("l")))
    print("     Can player move right? {}".format(sokoban.check_if_player_can_make_direction_move("r")))

    print("3) Move down:")
    sokoban.move_player(direction="d")

    print("4) Display updated board:")
    sokoban.board.display_board()