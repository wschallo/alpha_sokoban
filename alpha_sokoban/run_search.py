from search import Node, Heuristic, a_star_search, listToString, get_moves
from alpha_sokoban import alpha_sokoban
import sys
import os.path

if __name__ == "__main__":
    if len(sys.argv) >= 1:
        path_to_file = sys.argv[-1]
        if os.path.isfile(path_to_file):
            sokoban = alpha_sokoban(path_to_file)
            init_node = Node(state=sokoban, parent=None, action=None, g=0, h=Heuristic(sokoban))

            soln_node, nodes_exp = a_star_search(init_node)

            if isinstance(soln_node, Node):
                moves = get_moves(soln_node)
                print(str(len(moves)) + " " + listToString(moves))
        else:
            print("ERROR: Input file {} could not be found".format(path_to_file))
    else:
        print("ERROR: run_search.py requires as a command line argument a path to a sokoban map file (i.e. sokoban01.txt).")