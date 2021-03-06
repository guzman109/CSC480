import numpy as np
from collections import deque
starting_states = {0:[0,1,2,3,4,5,6,7,8], 1: [1,3,4,8,6,2,7,0,5], 2:[2,8,1,0,4,3,7,6,5], 3:[5,6,7,4,0,8,3,2,1]}
# direction_order = {'UDLR': 0, 'DULR': 1}
directions_UDLR = {0:(3,1), 1:(4,0,2), 2:(5,1), 3:(0,6,4), 4:(1,7,3,5), 5:(2,8,4), 6:(3,7), 7:(4,6,8), 8:(5,7)}
directions_Clock = {0:(1,3), 1:(2,4,0), 2:(5,1), 3:(0,4,6), 4:(1,5,7,3), 5:(2,8,4), 6:(3,7), 7:(4,8,6), 8:(5,7)}


class puzzle():
    def __init__(self, difficulty, direction_order='UDLR'):
        # Keep track of edges, each node will have an id number. Root (Start State) is 0.
        self.current_id = 1
        self.difficulty = difficulty
        # For searching strategies.
        self.search_ds = None

        if difficulty < 5:
            # Not a randomized start state
            self.start_state = np.array(starting_states[difficulty])
        else:
            # Randomzied start state
            self.start_state = np.array(starting_states[0])
            np.random.shuffle(self.start_state)
        
        # self.order = direction_order[]
    
    def print_state(self, node_info, id):
        print('State:\n', np.reshape(node_info[id][0],(3,3)))
        print('Blank Index:', node_info[id][1])
        # print('Parent ID:', node_info[id][2])
        print('In deque:', 'Yes' if node_info[id][3] else 'No', 'Expanded:', 'Yes' if node_info[id][4] else 'No')
        print('------------------------------------------------')
    def reset_puzzle(self):
        print('Reseting Puzzle!')
        if self.difficulty < 5:
            # Not a randomized start state
            self.start_state = np.array(starting_states[self.difficulty])
        else:
            # Randomzied start state
            self.start_state = np.shuffle(starting_states[0])

    def move_blank(self, array, i, j):
        array[i], array[j] = array[j], array[i]
        return array
    
    def isGoalState(self, state):
        goal_state = [1,2,3,8,0,4,7,6,5]
        return True if (state == goal_state).all() else False
    def Whatever_First_Search(self, search_alg):
        # Hashmap to keep track of node information (node data_structure). 
        # Each time a node is created, it is added to the dictionary as the key.
        # Key: (int)Node ID 
        # Value: (list)(state, blank_index, parent_id, in_deque, expanded, depth)
        start = self.start_state.tostring()
        node_info = {start:[self.start_state, np.argwhere(self.start_state==0)[0,0], '', False, False]}
        search_struct = deque()
        struct_size = 1
        # Append element to end of deque and set in_deque.
        search_struct.append(start)
        node_info[start][3] = True

        counter = 0
        while struct_size:
            if counter % 1000 == 0:
                print(f'\rIterations: {counter}', end='')

            # Pop element from deque and change in_deque and expanded
            if search_alg == "BFS":
                node_id = search_struct.popleft()
            elif search_alg == "DFS":
                node_id = search_struct.pop()

            struct_size -= 1
            node_info[node_id][3] = False
            node_info[node_id][4] = True

            # Check if state is a goal state
            if self.isGoalState(node_info[node_id][0]):
                print(f'\nGoal Reached, It took {counter} steps in total.')
                return True

            # Get location of blank space and search through possible moves (children)
            blank_idx = node_info[node_id][1]

            for move in directions_Clock[blank_idx]:
                # Create child
                child_state = self.move_blank(node_info[node_id][0].copy(), blank_idx, move)
                child_id = child_state.tostring()
                # Check if node is created. If so check if its in the deque or has been expanded
                if child_id not in node_info:
                    node_info[child_id] = [child_state, move, node_id, True, False]
                    search_struct.append(child_id)
                    struct_size += 1

            counter += 1
        return False
    
    def Iter_Deep(self, depth_limit):
        # Hashmap to keep track of node information (node data_structure). 
        # Each time a node is created, it is added to the dictionary as the key.
        # Key: (int)Node ID 
        # Value: (list)(state, blank_index, parent_id, in_deque, expanded, depth)
        start = self.start_state.tostring()
        node_info = {start:[self.start_state, np.argwhere(self.start_state==0)[0,0], '', False, False, 0]}
        search_struct = deque()
        struct_size = 1
        # Append element to end of deque and set in_deque.
        search_struct.append(start)
        node_info[start][3] = True

        expand_this_layer, expand_next_layer, = 1, 0

        counter, depth = 0,0
        while struct_size:
            if counter % 1000 == 0:
                print(f'\rIterations: {counter}', end='')

            # Pop element from deque and change in_deque and expanded
            node_id = search_struct.pop()

            struct_size -= 1
            node_info[node_id][3] = False
            node_info[node_id][4] = True

            # Check if state is a goal state
            if self.isGoalState(node_info[node_id][0]):
                print(f'\nGoal Reached, It took {counter} steps in total.')
                return True

            # Get location of blank space and search through possible moves (children)
            if depth != depth_limit: 
                blank_idx = node_info[node_id][1]

                for move in directions_Clock[blank_idx]:
                    # Create child
                    child_state = self.move_blank(node_info[node_id][0].copy(), blank_idx, move)
                    child_id = child_state.tostring()
                    # Check if node is created. If so check if its in the deque or has been expanded
                    if child_id not in node_info:
                        node_info[child_id] = [child_state, move, node_id, True, False, depth+1]
                        if node_info[child_id][5] < depth_limit:
                            search_struct.append(child_id)
                            expand_next_layer += 1
                            struct_size += 1

            counter += 1
            expand_this_layer -= 1
            if not expand_this_layer and expand_next_layer:
                expand_this_layer = expand_next_layer
                expand_next_layer = 0
                depth += 1
        return False

    def Iterative_Deepening(self):
        depth_limit = 0
        while not self.Iter_Deep(depth_limit=depth_limit):
            depth_limit += 1
            # print(f'\nCurrent Depth Limit: {depth_limit}')
    def Uniform_Cost_Search(self):
        pass
    def Best_First_Search(self):
        pass
    def A_Star(self, h):
        pass
