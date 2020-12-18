import heapq
import alpha_sokoban
from constants import MOVES, ACTION_COST, TABLE_SIZE
import sys
import numpy as np
import copy
import time
import os
import signal

NODES_EXP = 0

class TimedOutExc(Exception):
    pass

def deadline(timeout, *args):
    def decorate(f):
        def handler(signum, frame):
            raise TimedOutExc()

        def new_f(*args):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout)
            return f(*args)
            signal.alarm(0)

        new_f.__name__ = f.__name__
        return new_f
    return decorate

class Node:
    def __init__(self, state=None, parent=None, action=None, g=None, h=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = g
        self.heuristic = h

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def get_action(self):
        return self.action

    def get_path_cost(self):
        return self.path_cost

    def get_heuristic(self):
        return self.heuristic

    def get_total_cost(self):
        return self.path_cost + self.heuristic

    def __str__(self):
        return "Node with total cost {}".format(self.get_total_cost())

class TranspositionTable:
    def __init__(self, size_limit):
        self.table = []
        self.size_limit = size_limit
    
    def num_elem(self):
        return len(self.table)

    def add(self, node):
        if self.num_elem() < self.size_limit:
            self.table.append(node)
        else:
            del self.table[0]
            self.table.append(node)

    def in_table(self, node):
        for idx, elem in enumerate(self.table):
            if np.array_equal(elem.get_state().get_matrix(), node.get_state().get_matrix()):
                if node.get_total_cost() < elem.get_total_cost():
                    del self.table[idx]
                    return False
                else:
                    return True
        return False


def manhattan_distance(bx, stg):
    return abs(bx[0] - stg[0]) + abs(bx[1] - stg[1])

def greedy(boxes, storage):
    dis_matrix = [[manhattan_distance(bx, stg) for stg in storage] for bx in boxes] #create weighted matrix
    matched_boxes = []
    matched_stg = []
    match_set = []
    total_distance = 0
    edges = []

    for i, row in enumerate(dis_matrix):
        for j, dist in enumerate(row):
            edges.append((dist, i, j))
    edges.sort()

    while len(edges) != 0:
        dist,box,stg = edges.pop(0)
        if box not in matched_boxes and stg not in matched_stg:
            total_distance += dist
            match_set.append((boxes[box], storage[stg]))
            matched_boxes.append(box)
            matched_stg.append(stg)
    return match_set, total_distance

def Heuristic(state):
    boxes = state.get_boxes()
    storage = state.get_storage()
    _, dist = greedy(boxes, storage)
    return dist

@deadline(3600)
def a_star_search(init_node):
    global NODES_EXP

    count = 1
    frontier = [(init_node.get_total_cost(), count, init_node)]
    heapq.heapify(frontier)
    reached = TranspositionTable(TABLE_SIZE)
    reached.add(init_node)

    while len(frontier) != 0:
        _, _, node = heapq.heappop(frontier)
        NODES_EXP += 1

        child_nodes = expand(node)
        for child in child_nodes:
            state = child.get_state()
            if state.goal_test() == True:
                return child, NODES_EXP
            if reached.in_table(child) == False and state.is_there_a_deadlock() == False:
                reached.add(child)
                count += 1
                heapq.heappush(frontier, (child.get_total_cost(), count, child))
    
    fail = "Search Failed"
    return fail, NODES_EXP
             

def expand(node):
    child_nodes = []
    state = node.get_state()
    for move in MOVES.keys():
        if state.check_if_player_can_make_direction_move(move) == True:
            next_state = copy.deepcopy(state)
            next_state.move_player(move)
            path_cost = node.get_path_cost() + ACTION_COST
            heuristic = Heuristic(next_state)
            child_nodes.append(Node(state=next_state, parent=node, action=move, g=path_cost, h=heuristic))
    return child_nodes


def get_moves(node):
    moves = []
    while(node.get_parent() != None):
        moves.append(node.get_action())
        node = node.get_parent()
    moves.reverse()
    return moves

def listToString(s):  
    str1 = " "  
    return (str1.join(s)) 

if __name__ == "__main__":
    input_dir = '../sokoban_benchmarks/'
    # input_dir = '../Our_Input/'
    f = 'sokoban07b.txt'
    path_to_file = os.path.join(input_dir, f)
    sokoban = alpha_sokoban.alpha_sokoban(path_to_file)
    print(f)
    print("INITIAL STATE")
    print(sokoban.board.display_board(), '\n')
    init_node = Node(state=sokoban, parent=None, action=None, g=0, h=Heuristic(sokoban))
    start_time = time.time()
    try:
        soln_node, nodes_exp = a_star_search(init_node)
        runtime = time.time() - start_time
        if isinstance(soln_node, Node):
            moves = get_moves(soln_node)
            print("SOLUTION")
            print(str(len(moves)) + " " + listToString(moves) + "\n")
            print("RUNTIME")
            print("{:.3f} sec\n".format(runtime))

            for move in moves:
                sokoban.move_player(move)
            print("FINAL STATE")
            print(sokoban.board.display_board(), '\n')
            print("NODES EXPANDED: ", nodes_exp)
            print("REACHED GOAL STATE")
            print(sokoban.goal_test())
    except TimedOutExc:
        print("Timed out")
        print("Nodes expanded: {}".format(NODES_EXP))

    # dir = '../sokoban_benchmarks/'
    # files = os.listdir(dir)
    # files = [f for f in files if 'sokoban' in f]
    # files.sort(key=lambda f: f.split('.')[0].split('n')[1])
    # for f in files:
    #     path_to_file = os.path.join(dir,f)
    #     sokoban = alpha_sokoban.alpha_sokoban(path_to_file)
    #     print(f)
    #     print("INITIAL STATE")
    #     print(sokoban.board.display_board(), '\n')

    #     init_node = Node(state=sokoban, parent=None, action=None, g=0, h=Heuristic(sokoban))
    #     start_time = time.time() 
    #     soln_node = a_star_search(init_node)
    #     runtime = time.time() - start_time
    #     if isinstance(soln_node, Node):
    #         moves = get_moves(soln_node)
    #         print("SOLUTION")
    #         print(str(len(moves)) + " " + listToString(moves) + "\n")
    #         print("RUNTIME")
    #         print("{:.3f} sec\n".format(runtime))

    #         for move in moves:
    #             sokoban.move_player(move)
    #         print("FINAL STATE")
    #         print(sokoban.board.display_board(), '\n')
    #         print("REACHED GOAL STATE")
    #         print(sokoban.goal_test())
