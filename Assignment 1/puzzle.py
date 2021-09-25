import numpy as np
starting_states = {0:[0,1,2,3,4,5,6,7,8], 1: [1,3,4,8,6,2,7,0,5], 2:[2,8,1,0,4,3,7,6,5], 3:[5,6,7,4,0,8,3,2,1]}
directions = {0:(3,1), 1:(4,0,2), 2:(5,1), 3:(0,6,4), 4:(1,7,3,5), 5:(2,8,4), 6:(3,7), 7:(4,6,8), 8:(5,7)}


class puzzle():
    def __init__(self, difficulty):
        # Keep track of edges, each node will have an id number. Root (Start State) is 0.
        self.edges = {0:[]}
        self.current_id = 1

        # For searching strategies.
        self.deque = list()

        if difficulty < 5:
            # Not a randomized start state
            start_state = np.array(starting_states[difficulty])
        else:
            # Randomzied start state
            start_state = np.shuffle(starting_states[0])
        # Hashmap to keep track of node information (node data_structure). 
        # Each time a node is created, it is added to the dictionary as the key.
        # Key: (int)Node ID 
        # Value: (list)(state, deque_index, blank_index, action, depth, parent_id, expanded) 
        self.node_info = {0:[start_state, -1, np.argwhere(start_state==0)[0,0], -1, 0, -1, 0]}
    
    def print_state(self,idx):
        print('State:', np.reshape(self.node_info[idx][0],(3,3)))
        print('Deque Index:', self.node_info[idx][1])
        print('Blank Index:', self.node_info[idx][2])
        print('Action:', self.node_info[idx][3])
        print('Depth:', self.node_info[idx][4])
        print('Parent ID:', self.node_info[idx][5])
        print('Expanded:', 'Yes' if self.node_info[idx][6] else 'No')


    def swap(array, i, j):
        array[i], array[j] = array[j], array[i]
        return array
    def Breadth_First_Search(self):
        pass
    def Depth_First_Search(self):
        pass
    def Iterative_Deepening(self):
        pass
    def Uniform_Cost_Search(self):
        pass
    def Best_First_Search(self):
        pass
    def A_Star(self, h):
        pass
