import numpy as np

class DotsAndBoxes:
    def __init__(self, board_size, ply, cpu_first):
        self.board_size = board_size
        self.ply = ply
        self.scores = np.random.randint(low=1, high=6, size=self.board_size)
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
    
    def check_simulated_grid(self, grid):
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
        return grid, score

    def cpu_turn(self):
        alphas = np.zeros(shape=self.ply)
        betas = np.zeros(shape=self.ply)
        
        self.dfs(self.cpu_first, self.grid.copy(), self.ply+1)


    def dfs(self, isMin, simulated_grid, depth, ):
        simulated_grid, score = self.check_simulated_grid(simulated_grid)
        if score:
            if isMin
        if depth:
            next_moves = np.argwhere(simulated_grid == -1)
            for move in next_moves:
                simulated_grid[move] = 1
                self.dfs((not isMin), simulated_grid, depth-1)

