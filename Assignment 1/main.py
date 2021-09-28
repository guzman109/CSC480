import gui
from puzzle import puzzle

import numpy as np
difficulties = {'none':0, 'easy':1, 'medium':2, 'hard':3, 'random':5}




if __name__ == '__main__':
    difficulty = 'hard'
    p = puzzle(difficulties[difficulty])
    print('BFS')
    p.Breadth_First_Search()
    print('DFS')
    p.Depth_First_Search()
    print('Iter_Deep')
    p.Iterative_Deepening()
    print('Uniform-Cost')
    p.Uniform_Cost_Search()
    print('Best-First')
    p.Best_First_Search()
    print('A*1')
    p.A_Star(star=1)
    print('A*2')
    p.A_Star(star=2)
    print('A*3')
    p.A_Star(star=3)