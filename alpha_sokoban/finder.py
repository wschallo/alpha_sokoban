import numpy as np

def find_player_position_from_board(board):
  result = np.where(board == 4)
  if len(result[0]) == 0:
      result = np.where(board == 6)
  listOfCoordinates= list(zip(result[0], result[1]))
  return listOfCoordinates[0]