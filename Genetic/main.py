import numpy as np
from sudoku import Sudoku
import utilities
from genetic import GA
import time

board1 = {
    "(0,2)" : 1, "(0,5)" : 2,
    "(1,2)" : 5, "(1,5)" : 6, "(1,7)" : 3,
    "(2,0)" : 4, "(2,1)" : 6, "(2,5)" : 5,
    "(3,3)" : 1, "(3,5)" : 4, 
    "(4,0)" : 6, "(4,3)" : 8, "(4,6)" : 1, "(4,7)" : 4, "(4,8)" : 3,
    "(5,4)" : 9, "(5,6)" : 5, "(5,8)" : 8,
    "(6,0)" : 8, "(6,4)" : 4, "(6,5)" : 9, "(6,7)" : 5,
    "(7,0)" : 1, "(7,3)" : 3, "(7,4)" : 2,
    "(8,2)" : 9, "(8,6)" : 3
}

board2 = {
    "(0,2)" : 5, "(0,4)" : 1,
    "(1,2)" : 2, "(1,5)" : 4, "(1,7)" : 3,
    "(2,0)" : 1, "(2,2)" : 9, "(2,6)" : 2, "(2,8)" : 6,
    "(3,0)" : 2, "(3,4)" : 3,
    "(4,1)" : 4, "(4,6)" : 7,
    "(5,0)" : 5, "(5,5)" : 7, "(5,8)" : 1,
    "(6,3)" : 6, "(6,5)" : 3,
    "(7,1)" : 6, "(7,3)" : 1,
    "(8,4)" : 7, "(8,7)" : 5
}

board3 = {
    "(0,0)" : 6, "(0,1)" : 7,
    "(1,1)" : 2, "(1,2)" : 5,
    "(2,1)" : 9, "(2,3)" : 5, "(2,4)" : 6, "(2,6)" : 2,
    "(3,0)" : 3, "(3,4)" : 8, "(3,6)" : 9,
    "(4,6)" : 8, "(4,8)" : 1,
    "(5,3)" : 4, "(5,4)" : 7,
    "(6,2)" : 8, "(6,3)" : 6, "(6,7)" : 9,
    "(7,7)" : 1,
    "(8,0)" : 1, "(8,2)" : 6, "(8,4)" : 5, "(8,7)" : 7
}
def print_sudoku(puzzle): 
    for i in range(9): 
        if i % 3 == 0 and i != 0: 
            print("- - - - - - - - - - - ") 
        for j in range(9): 
            if j % 3 == 0 and j != 0: 
                print(" | ", end="") 
            print(puzzle[i][j], end=" ") 
        print() 


if __name__ == '__main__':

    problem = Sudoku(board1)
    print_sudoku(problem.board)

    start = time.time()
    genetic = GA(10000,board1,500,50,4,0.3,0.25,0.25)
    genetic.run()
    end = time.time()
    print("Execution time: ", (end-start)/60)

    # problem = Sudoku(board2)
    # print_sudoku(problem.board)

    # start = time.time()
    # genetic = GA(10000,board2,500,50,4,0.3,0.25,0.25)
    # genetic.run()
    # end = time.time()
    # print("Execution time: ", (end-start)/60)

    # problem = Sudoku(board3)
    # print_sudoku(problem.board)

    # start = time.time()
    # genetic = GA(10000,board3,500,50,4,0.3,0.25,0.25)
    # genetic.run()
    # end = time.time()
    # print("Execution time: ", (end-start)/60)

#ran board one on GA(10000,board2,500,50,4,0.3,0.25,0.25)
#ran board two on GA(10000,board2,500,50,4,0.3,0.25,0.25)