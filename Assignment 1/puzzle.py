import numpy as np
from heapq import *
from collections import deque
from scipy.spatial.distance import cdist, cityblock, euclidean

# Start states for each difficulty.
starting_states = {0:[0,1,2,3,4,5,6,7,8], 1: [1,3,4,8,6,2,7,0,5], 2:[2,8,1,0,4,3,7,6,5], 3:[5,6,7,4,0,8,3,2,1]}

# The indicies where the blank can move depending on location. 
directions_UDLR = {0:(3,1), 1:(4,0,2), 2:(5,1), 3:(0,6,4), 4:(1,7,3,5), 5:(2,8,4), 6:(3,7), 7:(4,6,8), 8:(5,7)}
directions_Clock = {0:(1,3), 1:(2,4,0), 2:(5,1), 3:(0,4,6), 4:(1,5,7,3), 5:(2,8,4), 6:(3,7), 7:(4,8,6), 8:(5,7)}
directions_CntrClock = {0:(3,1), 1:(0,4,2), 2:(1,5), 3:(0,6,4), 4:(1,3,7,5), 5:(2,4,8), 6:(3,7), 7:(4,6,8), 8:(5,7)}

goal_state_idx = {0:[1,1], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,2], 5:[2,2], 6:[2,1], 7:[2,0], 8:[1,0]}
goal_state = [1,2,3,8,0,4,7,6,5]


class puzzle():
    def __init__(self, difficulty):
        # Difficulty of the start state.
        self.difficulty = difficulty
        self.start_state = np.array(starting_states[difficulty])
    def moveBlank(self, array, i, j):
        array[i], array[j] = array[j], array[i]
        return array    
    def isGoalState(self, state):
        return True if (state == goal_state).all() else False
    def displayStats(self, id, cost, time, space):
        length = 0
        while id != self.start_state.tostring():
            id = self.nodes[id][2]
            length += 1
        
        print(f'Goal State Reached!')
        print(f'Length:\t{length}.')
        print(f'Cost:\t{cost}.')
        print(f'Time:\t{time}')
        print(f'Space:\t{space}')
        print(self.nodes[id][0].reshape((3,3)))
    """ Heuristic Functions """
    def HeuristicFunc(self, h=1):
        if h == 1:
            return lambda A: np.sum([1 if a!=g and a else 0 for a, g in zip(A, goal_state)])
        elif h == 2:
            return lambda A: np.sum([cityblock([i,j], goal_state_idx[A[i,j]]) if A[i,j] else 0 for i in range(3) for j in range(3)])
        elif h == 3:
            # return lambda A: np.sum([1 if a!=g and a else 0 for a, g in zip(A.flatten(), goal_state)]) + np.sum([cityblock([i,j], goal_state_idx[A[i,j]]) if A[i,j] else 0 for i in range(3) for j in range(3)])
            return lambda A: np.sum([euclidean([i,j], goal_state_idx[A[i,j]]) if A[i,j] else 0 for i in range(3) for j in range(3)])
 
    """ Search Algorithms """
    def SetUp(self, algorithm, search_struct, depth_limit=-1, star=1):
        """
            Input: algorithm: (string) the name of the searching algorithm, 
                    search_struct: (deque or heap) the search data structure to keep track of nodes it is going to visit.
                    star: (int)(optional) For A* Search, this is to use the proper Heuristic Function.
            Output: 
        """
        """ 
            node info is a Hash Map to keep track of node structure
            
            Key: Node ID (string)
            Value: [state, index of blank tile, parent id, in the structure?, expanded?, cost, h, cost+h, depth]
        """
        self.nodes = dict()
        start_id = self.start_state.tostring()

        # Calculate Heuristic if algorithm uses it. Else it just adds the nodes respective information to the dictionary.
        H = self.HeuristicFunc(star) if algorithm in ['Best_First', 'A_Star'] else None
        if algorithm in ['Best_First', 'A_Star']:
            if star == 1:
                h = H(self.start_state)
            else:
                h = H(np.reshape(self.start_state, (3,3)))
            self.nodes[start_id] = [self.start_state, np.argwhere(self.start_state==0)[0,0], '', False, False, 0, h, h, 0]
        else:
            self.nodes[start_id] = [self.start_state, np.argwhere(self.start_state==0)[0,0], '', False, False, 0, 0, 0, 0]


        # Add to the data structure depending on the algorithm.
        if algorithm in ['BFS', 'DFS', 'Iter_Deep']:
            search_struct.append(start_id)
        else:
            search_struct.append((self.nodes[start_id][7], start_id))
            heapify(search_struct)
        self.nodes[start_id][3] = True   # Set in_struct to true
        return self.WhateverSearch(algorithm, search_struct, depth_limit=depth_limit, star=star, H=H)
        
    def WhateverSearch(self, algorithm, search_struct, depth_limit=-1, star=1, H=None):
        num_popped_off = 0
        max_len = len(search_struct)
        # Start the serach.
        while len(search_struct):            
            # Pop the element from the search_struct and expand.
            if algorithm == 'BFS': 
                node_id = search_struct.popleft()
            elif algorithm in ['DFS', 'Iter_Deep']:
                node_id = search_struct.pop()
            else:
                node_id = heappop(search_struct)[1]

            # To keep track of time and space.
            num_popped_off += 1 
            max_len = len(search_struct) if max_len < len(search_struct) else max_len


            # Set in_struct to False and check if it has been expanded.
            self.nodes[node_id][3] = False
            if not self.nodes[node_id][4]:
                self.nodes[node_id][4] = True    # Set expanded to True

                # Check if current node is a goal state
                if self.isGoalState(self.nodes[node_id][0]):
                    self.displayStats(node_id, self.nodes[node_id][5], num_popped_off, max_len)
                    del(self.nodes)
                    return True
                
                depth = self.nodes[node_id][8]
                if depth != depth_limit:
                
                    blank_idx = self.nodes[node_id][1]   # Blank tile index
                    for move in directions_CntrClock[blank_idx]:
                        # Create Child
                        child_state = self.moveBlank(self.nodes[node_id][0].copy(), blank_idx, move)
                        child_id = child_state.tostring()

                        # Calculate cost and heuristic depending on algorithm
                        cost = move + self.nodes[node_id][5]
                        if algorithm in ['BFS', 'DFS', 'Iter_Deep', 'Unif_Cost']:
                            h = 0
                        else:
                            h = H(child_state) if star == 1 else H(np.reshape(child_state, (3,3)))

                        # Add to node to self.nodes dictionary if it hasn't been created.
                        if child_id not in self.nodes:
                            self.nodes[child_id] = [child_state, move, node_id, True, False, cost, h, cost+h, depth+1]
                            # Add the new child
                            if algorithm in ['BFS', 'DFS']:
                                    search_struct.append(child_id)
                            elif algorithm == 'Iter_Deep':
                                if self.nodes[child_id][8] < depth_limit:
                                    search_struct.append(child_id)
                            elif algorithm == 'Best_First':
                                heappush(search_struct, (self.nodes[child_id][6], child_id))
                            else:
                                heappush(search_struct, (self.nodes[child_id][7], child_id))
                        else:
                            # If it has been created then check if the new cost + heuristic value is less than the current one. (Only for A*)
                            if algorithm in ['Unif_Cost', 'A_Star'] and self.nodes[child_id][7] > cost + h:
                                self.nodes[child_id][7] = cost+h
                                self.nodes[child_id][5] = cost
                                # Add the child with updated priority
                                heappush(search_struct, (self.nodes[child_id][7], child_id))
        del(self.nodes)
        return False
    
    def BreadthFirstSearch(self):
        self.SetUp('BFS', deque())
    def DepthFirstSearch(self):
        self.SetUp('DFS', deque())
    def IterativeDeepening(self):
        depth_limit = 0
        while not self.SetUp('Iter_Deep', deque(), depth_limit=depth_limit):
            depth_limit += 1
    def UniformCostSearch(self):
        self.SetUp('Unif_Cost', list())
    def BestFirstSearch(self):
        self.SetUp('Best_First', list())
    def AStar(self, star=1):
        self.SetUp('A_Star', list(), star=star)

        

            


      

