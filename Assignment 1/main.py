import gui
from puzzle import puzzle

import numpy as np
difficulties = {'none':0, 'easy':1, 'medium':2, 'hard':3, 'random':5}




if __name__ == '__main__':
    difficulty = 'easy'
    p = puzzle(difficulties[difficulty])
    p.print_state(0)