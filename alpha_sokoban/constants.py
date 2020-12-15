#mapping of moves to change in index:
MOVES = {'U': (-1,0),
         'D': (1,0),
         'L': (0,-1),
         'R': (0,1)}

#mapping of integers to tile types:
TILE_TYPES = {0: 'open_space',
              1: 'wall',
              2: 'box',
              3: 'storage',
              4: 'player',
              5: 'box_on_storage',
              6: 'player_on_storage'}

INVALID_TILE = -1

#mapping of tiles integers to symbols:
TILE_SYMBOLS = {0: ' ',
                1: '#',
                2: '$',
                3: '.',
                4: '@',
                5: '*',
                6: '+'}

INVALID_TILE_SYMBOL = "!"

#hyper params:
ACTION_COST = 1
TABLE_SIZE = 10

#deadlock detection:
##  Below are the filters:
##  2x2 deadlocks:
DEADLOCK_2_BY_2_0 = [[1,1],[1,2]]
DEADLOCK_2_BY_2_1 = [[1,2],[1,2]]
DEADLOCK_2_BY_2_2 = [[2,2],[1,2]]
DEADLOCK_2_BY_2_3 = [[2,2],[2,2]]

##  3x3 deadlocks: 1 box
DEADLOCK_3_BY_3_0 = [[1,1,0],[1,2,1],[0,0,1]]
DEADLOCK_3_BY_3_1 = [[0,1,0],[1,0,1],[1,2,1]]

##  3x3 deadlocks: 2 boxes
DEADLOCK_3_BY_3_2 = [[1,1,0],[1,0,1],[0,2,2]]
DEADLOCK_3_BY_3_3 = [[1,1,0],[1,0,2],[0,2,1]]
DEADLOCK_3_BY_3_4 = [[0,1,0],[1,0,1],[1,2,2]]
DEADLOCK_3_BY_3_5 = [[0,1,0],[1,0,2],[1,2,1]]
DEADLOCK_3_BY_3_6 = [[0,2,1],[1,2,0],[0,0,0]]

##  3x3 deadlocks: 3 boxes
DEADLOCK_3_BY_3_7 = [[1,1,0],[1,0,2],[0,2,2]]
DEADLOCK_3_BY_3_8 = [[0,1,0],[1,0,2],[1,2,2]]
DEADLOCK_3_BY_3_9 = [[0,1,0],[1,0,1],[2,2,2]]

##  3x3 deadlocks: 4 boxes
DEADLOCK_3_BY_3_10 = [[1,2,0],[1,0,2],[0,2,2]]
DEADLOCK_3_BY_3_11 = [[2,1,0],[1,0,2],[0,2,2]]
DEADLOCK_3_BY_3_12 = [[0,1,0],[1,0,2],[2,2,2]]

##  3x3 deadlocks: 5 boxes
DEADLOCK_3_BY_3_13 = [[2,2,0],[1,0,2],[0,2,2]]
DEADLOCK_3_BY_3_14 = [[1,2,0],[2,0,2],[0,2,2]]
DEADLOCK_3_BY_3_15 = [[0,1,0],[2,0,2],[2,2,2]]

##Deadlock Filter Collection:
DEADLOCK_FILTER_2_BY_2 = [DEADLOCK_2_BY_2_0,DEADLOCK_2_BY_2_1,DEADLOCK_2_BY_2_2,DEADLOCK_2_BY_2_3]

DEADLOCK_FILTER_3_BY_3_1_BOX = [DEADLOCK_3_BY_3_0,DEADLOCK_3_BY_3_1]
DEADLOCK_FILTER_3_BY_3_2_BOX = [DEADLOCK_3_BY_3_2,DEADLOCK_3_BY_3_3,DEADLOCK_3_BY_3_4,DEADLOCK_3_BY_3_5,DEADLOCK_3_BY_3_6]
DEADLOCK_FILTER_3_BY_3_3_BOX = [DEADLOCK_3_BY_3_7,DEADLOCK_3_BY_3_8,DEADLOCK_3_BY_3_9]
DEADLOCK_FILTER_3_BY_3_4_BOX = [DEADLOCK_3_BY_3_10,DEADLOCK_3_BY_3_11,DEADLOCK_3_BY_3_12]
DEADLOCK_FILTER_3_BY_3_5_BOX = [DEADLOCK_3_BY_3_13,DEADLOCK_3_BY_3_14,DEADLOCK_3_BY_3_15]
