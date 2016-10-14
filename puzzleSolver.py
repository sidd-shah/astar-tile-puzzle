# References Used 
# https://en.wikipedia.org/wiki/Iterative_deepening_A*

import queue as Q
import node
from node import Node
import sys
import math
import time

if __name__ == '__main__':

    frontier_nodes = Q.PriorityQueue()
    
    if len(sys.argv) == 5:
        algorithm = int(sys.argv[1])
        in_file = open(sys.argv[3])
        out_file = open(sys.argv[4], 'w')
    else:
        print('Wrong number of arguments. Usage:\puzzleSover.py <ALGORITHM NUMBER> <N> <INPUT FILE PATH > <OUTPATH>')
        exit()

    input = in_file.read()
    input = input.split('\n')[:-1]
    input_node = []

    for i, row in enumerate(input):
        input_node.append(row.split(','))

    initial_state = Node()
    initial_state.tiles = input_node
    print(initial_state.calculate_empty_pos())
    print(input_node)

    def astar(initial_state, heuristic=1):
        explored_nodes = []
        frontier_nodes.put(initial_state)
        while not frontier_nodes.empty():
            current_node = frontier_nodes.get()
            if current_node.tiles not in explored_nodes:
                explored_nodes.append(current_node.tiles)
                
                current_distance = current_node.distance_from_source_node + current_node.distance_to_goal_node()
                # print(current_distance, len(explored_nodes))
                for action in current_node.find_possible_moves():
                    new_node = Node(current_node, action, heuristic)
                    distance_to_goal_node = new_node.distance_to_goal_node()
                    if distance_to_goal_node == 0 :
                        success_node = new_node
                        frontier_nodes.queue.clear()
                        break
                    else:
                        frontier_nodes.put(new_node)

        return success_node, explored_nodes


 

    def search(node, bound):
        total_cost = node.distance_from_source_node + node.distance_to_goal_node()
        if total_cost > bound:
            return node,total_cost
        if node.distance_to_goal_node() == 0:
            return node,'success'
        min = math.inf
        for action in node.find_possible_moves():
            new_node = Node(node, action)
            result_node,result = search(new_node, bound)
            if result == 'success':
                return result_node,'success'
            if result < min:
                min = result
        return result_node, min

    # Start from the initial state everytime the bound increases
    def iterative_deepening_astar():
        bound = initial_state.distance_to_goal_node()
        while True:
            node,result = search(initial_state, bound)
            if result == 'success':
                return node,'success'
                break
            elif result == math.inf:
                return node,'no optimal solution exists'
                break
            else:
                bound = result

    if algorithm == 1:
        start_time = time.time()
        success_node, explored_nodes = astar(initial_state,1)
        end_time  = time.time()
    else:
        start_time = time.time()
        success_node,result = iterative_deepening_astar()
        end_time = time.time()
    
    out_file.write(",".join(success_node.path_so_far))
    print('Found optimal solution {0}\n{1}\n'.format(success_node.tiles, success_node.path_so_far))
    # print('No of nodes explored {0}\n'.format(len(explored_nodes)))
    print("Execution Time {0}s".format(end_time - start_time))

    # start_time = time.time()
    # success_node, explored_nodes = astar(initial_state,2)
    # end_time  = time.time()
    # out_file.write("{0},{1},{2}\n".format(len(explored_nodes), round((end_time - start_time)*1000, 5), len(success_node.path_so_far)))
    

    in_file.close()
    out_file.close()