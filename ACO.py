"""
Sudoku Wave Function Collapse Solver combinf with an Ant Colony Optimizer- Brian Beach
An AI based Sudoku solver using the Ant COlony Optimization System. 
It will return all generated solutions, execution times, and general statistics through the main function.
A full solution is not guarenteed due to the random nature of the system.
"""
import time
import numpy as np
import random

class Ant:
    #-------- ANT IMPLEMENTATION FUNCTIONS --------#
    def __init__(self, size, base_board):
        self.size = size
        self.base_board = base_board
        self.solution = [[0 for _ in range(size)] for _ in range(size)]

    def generate_solution(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.base_board[i][j] == 0:  # Only fill cells that are empty in the base board
                    possible_values = self.get_possible_values(i, j)
                    if possible_values:
                        self.solution[i][j] = random.choice(possible_values)
                    else:
                        self.solution[i][j] = 0  # If no valid move, leave the cell empty

    def get_possible_values(self, row, col):
        possible_values = set(range(1, 10))
        # Eliminate values based on current board state
        for i in range(9):
            possible_values.discard(self.base_board[row][i])
            possible_values.discard(self.base_board[i][col])

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                possible_values.discard(self.base_board[i][j])

        return list(possible_values)

class AntColonyOptimizer:
    #-------- OPTIMIZER FUNCTIONS --------#
    def __init__(self, puzzle, num_ants, evaporation_rate):
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.puzzle = puzzle
        self.ants = [Ant(9, puzzle) for _ in range(num_ants)]  # Pass the puzzle to each ant
        self.pheromone_levels = np.ones((9, 9, 9))  # 9x9 grid with 9 possible values

    def update_pheromones(self, ant, completion_rate, improvement):
        for i in range(9):
            for j in range(9):
                value = ant.solution[i][j]
                if value != 0:
                    if completion_rate == 100:
                        self.pheromone_levels[i][j][value-1] *= 2  # Major increase for correct solutions
                    elif improvement > 5:
                        self.pheromone_levels[i][j][value-1] *= 1.5  # Minor increase for improvements
                    elif improvement > 0:
                        self.pheromone_levels[i][j][value-1] *= 1.1  # Slight increase for improvements
                    else:
                        self.pheromone_levels[i][j][value-1] *= 0.5  # Halve pheromone for bad solutions

    def evaporate_pheromones(self):
        self.pheromone_levels *= (1 - self.evaporation_rate)

    def solve(self, puzzle):
        best_solution = None
        best_completion_rate = 0

        for iteration in range(1000):  # Iteration Limit
            for ant in self.ants:
                ant.generate_solution()

                solver = SudokuSolver(puzzle, ant.solution)
                solution, completion_rate = solver.solve_with_aco(self.pheromone_levels)

                if completion_rate > best_completion_rate:
                    improvement = completion_rate - best_completion_rate
                    best_solution = solution
                    best_completion_rate = completion_rate
                else:
                    improvement = 0

                self.update_pheromones(ant, completion_rate, improvement)

            self.evaporate_pheromones()

            if best_completion_rate == 100:
                break

        return best_solution, best_completion_rate
    
class SudokuSolver:
    #-------- HELPER FUNCTIONS --------#
    def __init__(self, board):
        self.board = board
        self.size = 9
        self.subgrid_size = 3
        self.possible_values = [[set(range(1, 10)) if board[i][j] == 0 else set() for j in range(self.size)] for i in range(self.size)]

    def load_puzzle(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    self.update_possible_values(i, j, self.board[i][j])

    def update_possible_values(self, row, col, value):
        # Clear the possible values for the cell that just got a number assigned
        self.possible_values[row][col].clear()

        # Update the row and column
        for i in range(self.size):
            self.possible_values[row][i].discard(value)
            self.possible_values[i][col].discard(value)

        # Update the 3x3 subgrid
        start_row, start_col = row - row % self.subgrid_size, col - col % self.subgrid_size
        for i in range(start_row, start_row + self.subgrid_size):
            for j in range(start_col, start_col + self.subgrid_size):
                self.possible_values[i][j].discard(value)


    def is_solved_and_valid(self):
        # Check each row and column
        for i in range(self.size):
            if not self.is_unique(self.board[i]) or not self.is_unique([self.board[j][i] for j in range(self.size)]):
                return False

        # Check each 3x3 subgrid
        for row in range(0, self.size, self.subgrid_size):
            for col in range(0, self.size, self.subgrid_size):
                if not self.is_subgrid_unique(row, col):
                    return False

        return True

    def is_unique(self, sequence):
        return len(sequence) == len(set(sequence)) and all(sequence)

    def is_subgrid_unique(self, start_row, start_col):
        subgrid = []
        for row in range(start_row, start_row + self.subgrid_size):
            for col in range(start_col, start_col + self.subgrid_size):
                subgrid.append(self.board[row][col])
        return self.is_unique(subgrid)
    
    def completion_percentage(self):
        filled_cells = sum(1 for row in self.board for cell in row if cell != 0)
        total_cells = self.size * self.size
        return (filled_cells / total_cells) * 100
    
    def is_solvable(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0 and not self.possible_values[i][j]:
                    return False
        return True

    #-------- WAVE FUNCTION COLLAPSE FUNCTIONS --------#
    def single_assignment(self):
        updated = False
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0 and len(self.possible_values[i][j]) == 1:
                    value = next(iter(self.possible_values[i][j]))
                    self.board[i][j] = value
                    self.update_possible_values(i, j, value)
                    if not self.is_solvable():
                        # Revert the change if it makes the puzzle unsolvable
                        self.board[i][j] = 0
                        self.load_puzzle()
                    else:
                        updated = True
        return updated

    def unique_assignment(self):
        updated = False
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    unique_value = self.find_unique_value(i, j)
                    if unique_value:
                        original_value = self.board[i][j]
                        self.board[i][j] = unique_value
                        self.update_possible_values(i, j, unique_value)
                        if not self.is_solvable():
                            # Revert the change if it makes the puzzle unsolvable
                            self.board[i][j] = original_value
                            self.load_puzzle()
                        else:
                            updated = True
        return updated

    def find_unique_value(self, row, col):
        possible_values = self.possible_values[row][col]
        for value in possible_values:
            if self.is_unique_in_row(row, value) or self.is_unique_in_col(col, value) or self.is_unique_in_subgrid(row, col, value):
                return value
        return None

    def is_unique_in_row(self, row, value):
        for col in range(self.size):
            if value in self.possible_values[row][col] and self.board[row][col] == 0 and (row, col) != (row, col):
                return False
        return True

    def is_unique_in_col(self, col, value):
        for row in range(self.size):
            if value in self.possible_values[row][col] and self.board[row][col] == 0 and (row, col) != (row, col):
                return False
        return True

    def is_unique_in_subgrid(self, row, col, value):
        start_row, start_col = row - row % self.subgrid_size, col - col % self.subgrid_size
        for i in range(start_row, start_row + self.subgrid_size):
            for j in range(start_col, start_col + self.subgrid_size):
                if value in self.possible_values[i][j] and self.board[i][j] == 0 and (i, j) != (row, col):
                    return False
        return True

    def solve(self):
        self.load_puzzle()
        while True:
            updated = self.single_assignment() or self.unique_assignment()
            if not updated:
                break
        return self.board
    

class SudokuSolver(SudokuSolver):  # Extend for the ACO
    def __init__(self, board, ant_solution=None):
        super().__init__(board)
        self.ant_solution = ant_solution

    def solve_with_aco(self, pheromone_levels):
        if self.ant_solution and self.is_valid_partial_solution(self.ant_solution):
            self.board = self.apply_ant_solution(self.ant_solution, pheromone_levels)
        else:
            return None, 0  # Return if the ant solution is not valid

        self.load_puzzle()
        while True:
            updated = self.single_assignment() or self.unique_assignment()
            if not updated:
                break
        completion_rate = self.completion_percentage()
        return self.board, completion_rate

    def apply_ant_solution(self, ant_solution, pheromone_levels):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0 and ant_solution[i][j] != 0:
                    if self.is_valid_number(i, j, ant_solution[i][j]):
                        self.board[i][j] = ant_solution[i][j]
        return self.board
    
    def is_valid_partial_solution(self, solution):
        for i in range(self.size):
            for j in range(self.size):
                if solution[i][j] != 0 and not self.is_valid_number(i, j, solution[i][j]):
                    return False
        return True

    def is_valid_number(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True


#-------- EXAMPLE PUZZLES --------#
sudoku1 = [
    [0, 0, 1, 0, 0, 2, 0, 0, 0],
    [0, 0, 5, 0, 0, 6, 0, 3, 0],
    [4, 6, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 1, 0, 4, 0, 0, 0],
    [6, 0, 0, 8, 0, 0, 1, 4, 3],
    [0, 0, 0, 0, 9, 0, 5, 0, 8],
    [8, 0, 0, 0, 4, 9, 0, 5, 0],
    [1, 0, 0, 3, 2, 0, 0, 0, 0],
    [0, 0, 9, 0, 0, 0, 3, 0, 0]
]

sudoku2 = [
    [0, 0, 5, 0, 1, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 4, 0, 3, 0],
    [1, 0, 9, 0, 0, 0, 2, 0, 6],
    [2, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 4, 0, 0, 0, 0, 7, 0, 0],
    [5, 0, 0, 0, 0, 7, 0, 0, 1],
    [0, 0, 0, 6, 0, 3, 0, 0, 0],
    [0, 6, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 0, 0, 5, 0]
]

sudoku3 = [
    [6, 7, 0, 0, 0, 0, 0, 0, 0],  
    [0, 2, 5, 0, 0, 0, 0, 0, 0],  
    [3, 9, 0, 5, 6, 0, 2, 0, 0],  
    [0, 0, 0, 0, 8, 0, 9, 0, 0],  
    [0, 0, 0, 0, 0, 0, 8, 0, 1],  
    [0, 0, 0, 4, 7, 0, 0, 0, 0],  
    [0, 0, 8, 6, 0, 0, 0, 9, 0],  
    [0, 0, 0, 0, 0, 0, 0, 1, 0],  
    [1, 0, 6, 0, 5, 0, 0, 7, 0],  
]

sudoku4 = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

puzzles = [sudoku1, sudoku2, sudoku3, sudoku4]

#-------- DRIVER FUNCTION --------#
def main():
    avg_time = []
    solved = 0
    total_completion_rates = []
    failed_completion_rates = []

    for puzzle in puzzles: 
        start_time = time.time()
        solver = SudokuSolver(puzzle)
        puzzle = solver.solve()
        solver = AntColonyOptimizer(puzzle, num_ants=10, evaporation_rate=0.1)
        solution, completion_rate = solver.solve(puzzle)
        elapsed_time = time.time() - start_time
        avg_time.append(elapsed_time)
        total_completion_rates.append(completion_rate)
        
        if completion_rate >= 100:
            solved += 1
        else:
            failed_completion_rates.append(completion_rate)

        # Print the solution in a readable format
        for row in solution:
            print(" ".join(map(str, row)))

        print(f"Execution time: {elapsed_time:.6f} seconds")
    
    print(f"Average execution time: {(sum(avg_time) / len(avg_time)):.6f} seconds")
    print(f"Solved: {solved} out of {len(puzzles)}")
    print(f"Average completion rate: {(sum(total_completion_rates) / len(total_completion_rates)):.2f}%")
    print(f"Average failed completion rate: {(sum(failed_completion_rates) / len(failed_completion_rates)):.2f}%")
    

if __name__ == "__main__":
    main()