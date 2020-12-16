import numpy as np

def get_board(file_name):
    """returns a matrix representation of the board where
    0 -> open space
    1 -> wall
    2 -> box
    3 -> storage
    4 -> player
    5 -> box on storage location
    6 -> player on storage location

    Parameters
    __________
    file_name : str
        path to file
    """
    with open(file_name, 'r') as f:
        f_contents = f.readlines()
        f_contents = [line.replace("\n", "").split(" ") for line in f_contents]

        board_dim = f_contents[0]
        width = int(board_dim[0])
        height = int(board_dim[1])
        board = np.zeros((height, width), dtype=np.uint8)

        wall_loc = f_contents[1]
        num_walls = int(wall_loc[0])
        for i in range(1, num_walls * 2 + 1, 2):
            row = int(wall_loc[i]) - 1
            col = int(wall_loc[i + 1]) - 1
            board[row, col] = 1

        storage_loc = f_contents[3]
        num_storage = int(storage_loc[0])
        for i in range(1, num_storage * 2 + 1, 2):
            row = int(storage_loc[i]) - 1
            col = int(storage_loc[i + 1]) - 1
            board[row, col] = 3

        box_loc = f_contents[2]
        num_boxes = int(box_loc[0])
        for i in range(1, num_boxes * 2 + 1, 2):
            row = int(box_loc[i]) - 1
            col = int(box_loc[i + 1]) - 1
            if board[row, col] == 3:
                board[row, col] = 5
            else:
                board[row, col] = 2

        player_loc = f_contents[4]
        row = int(player_loc[0]) - 1
        col = int(player_loc[1]) - 1
        if board[row,col] == 3:
            board[row, col] = 6
        else:
            board[row, col] = 4

        return board

if __name__ == "__main__":
    path_to_input = "../sample_input_files.sokoban00.txt"
    print(get_board(path_to_input))
