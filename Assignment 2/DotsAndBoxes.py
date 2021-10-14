import numpy as np
from collections import deque

class DotsAndBoxes:
    def __init__(self, board_size, ply, cpu_first):
        self.board_size = board_size
        self.ply = ply
        self.scores = np.random.RandomState(1).randint(low=1, high=6, size=self.board_size)
        self.grid = list()
        self.player_score = 0
        self.cpu_score = 0
        self.boxes_complete = 0
        self.cpu_first = cpu_first
    
    def __str__(self):
        return np.array2string(self.scores)

    def __repr__(self):
        return np.array2string(self.scores)

    def check_grid(self, player=False):
        H,W = self.grid.shape
        
        m = 0
        # Look through grid to see if a box was completed in this turn.
        for i in np.arange(H, step=2):
            n = 0
            for j in np.arange(W, step=2):
                # Check each box
                if i+3 <= H and j+3 <= W:
                    if np.sum(self.grid[i:i+3,j:j+3]) == 4:
                        # A box is complete!
                        self.grid[i+1, j+1] = self.scores[m, n]
                        # Update Player or CPU score
                        if player:
                            self.player_score += self.scores[m,n]
                        else:
                            self.cpu_score += self.scores[m,n]
                        
                        #Update number of complete boxes
                        self.boxes_complete += 1
                        return (m, n)
                    n += 1
            m += 1
        return None

    def scoring_function(self, score=0):
        return (self.cpu_score + score) - self.player_score
    def check_node(self, grid):
        H,W = grid.shape
        m = 0
        score = 0
        # Look through grid to see if a box was completed in this turn.
        for i in np.arange(H, step=2):
            n = 0
            for j in np.arange(W, step=2):
                # Check each box
                if i+3 <= H and j+3 <= W:
                    if np.sum(grid[i:i+3,j:j+3]) == 4:
                        # A box is complete!
                        score = self.scores[m,n]
                        grid[i+1, j+1] = self.scores[m, n]
                    n += 1
            m += 1
        return score

    def cpu_turn(self):
        self.alpha_betas = [None] * self.ply
        self.last_top_update = None
        move = tuple(self.set_up_dfs(self.grid.copy(), self.ply, self.cpu_first))
        self.grid[move] = 1
        return move
    
    def set_up_dfs(self, root, depth, is_min):
        next_moves = np.argwhere(root == -1)
        best_move = None
        for move in next_moves:
            child = root.copy()
            child[move] = 1
            score,_ = self.dfs(child, depth-1, not is_min)

            if is_min:
                #AI is Min
                if (self.alpha_betas[depth-1] == None) or (self.alpha_betas[depth-1] > score):
                    self.alpha_betas[depth-1] = score
                    self.last_top_update = depth-1
                    best_move = move
            else:
                # AI is Max
                if (self.alpha_betas[depth-1] == None) or (self.alpha_betas[depth-1] < score):
                    self.alpha_betas[depth-1] = score
                    self.last_top_update = depth-1
                    best_move = move
        return best_move
            
    def update_alpha_betas(self, score, is_min, idx):
        print('IDX', idx)
        # Change the alpha or beta for this node
        prune = False
        if is_min:
            # AI is Min
            if (self.alpha_betas[idx] == None) or (self.alpha_betas[idx] > score):
                self.alpha_betas[idx] = score
                if self.last_top_update == None or self.last_top_update < idx:
                    self.last_top_update = idx
        else:
            # AI is max
            if (self.alpha_betas[idx] == None) or (self.alpha_betas[idx] < score):
                self.alpha_betas[idx] = score
                if self.last_top_update == None or self.last_top_update < idx:
                    self.last_top_update = idx
        
        # Check if we can prune
        if self.last_top_update != idx:
            cpu_role = len(self.alpha_betas)-1
            if (cpu_role % 2) == (self.last_top_update % 2):
                # Both either Min or Max
                if is_min:
                    if self.alpha_betas[self.last_top_update] < self.alpha_betas[idx]:
                        prune = True
                else:
                    if self.alpha_betas[self.last_top_update] > self.alpha_betas[idx]:
                        prune = True
            else:
                # Opposite Roles
                if is_min:
                    if self.alpha_betas[self.last_top_update] > self.alpha_betas[idx]:
                        prune = True
                else:
                    if self.alpha_betas[self.last_top_update] < self.alpha_betas[idx]:
                        prune = True
        return prune
    def dfs(self, node, depth, is_min):
        score = self.check_node(node)
        if score:
            # Leaf Node if completes a box
            return self.scoring_function(score), False
        if depth:
            # Not a leaf node
            next_moves = np.argwhere(node == -1)
            clear_bottom_alph_betas = True
            for move in next_moves:
                # Set up children
                if clear_bottom_alph_betas:
                    self.alpha_betas[depth-1] = None
                    clear_bottom_alph_betas = False
                child = node.copy()
                child[move] = 1
                score, clear_bottom_alph_betas = self.dfs(child, depth-1, not is_min)

                if self.update_alpha_betas(score, is_min, depth-1):
                    # return self.alpha_betas[self.last_top_update], True
                    break
            return self.alpha_betas[depth-1], True 
        else:
            # Leaf Node
            return self.scoring_function(self.check_node(node)), False

