from constants import MOVES

def check_if_valid_move_direction(direction) -> bool:
  '''check if direction is valid move (i.e. up, down, left, right)'''
  return direction in MOVES.keys()
  