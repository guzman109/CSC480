from puzzle import puzzle

import numpy as np
difficulties = {'easy':1, 'medium':2, 'hard':3}




if __name__ == '__main__':
    while True:
        print("Enter difficulty (easy, medium, or hard). (To exit enter 'exit')")
        difficulty = input()
        if difficulty != 'exit':
            print(f'Puzzle Difficulty is set to {difficulty}.')
            p = puzzle(difficulties[difficulty])
            print("Enter search stragegy (BFS, DFS, Iter_Deep, Unif_Cost, Best_First, A*1, A*2 or A*3).")
            algorithm = input()
            if algorithm == 'BFS':
                print('Running BFS')
                p.BreadthFirstSearch()
            elif algorithm == 'DFS':
                print('Running DFS')
                p.DepthFirstSearch()
            elif algorithm == 'Iter_Deep':
                print('Running Iter_Deep')
                p.IterativeDeepening()
            elif algorithm == 'Unif_Cost':
                print('Running Uniform-Cost')
                p.UniformCostSearch()
            elif algorithm == 'Best_First':
                print('Running Best-First')
                p.BestFirstSearch()
            elif algorithm == 'A*1':
                print('Running A*1')
                p.AStar(star=1)
            elif algorithm == 'A*2':
                print('Running A*2')
                p.AStar(star=2)
            elif algorithm == 'A*3':
                print('Running A*3')
                p.AStar(star=3)
            else:
                print('Please Try again.')
            del(p)
        else:
            break