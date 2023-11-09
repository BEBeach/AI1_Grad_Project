import time

SIZE = 9
GRID_SIZE = 3

# Helper function to get the block
def get_block_number(row, col):
    return (row // GRID_SIZE) * GRID_SIZE + (col // GRID_SIZE)

# Verifies the assignment
def is_valid_assignment(board, row, col, num):
    block_number = get_block_number(row, col)
    return not any(
        board[row][x] == num or
        board[x][col] == num or
        board[GRID_SIZE * (block_number // GRID_SIZE) + (x % GRID_SIZE)][GRID_SIZE * (block_number % GRID_SIZE) + (x // GRID_SIZE)] == num
        for x in range(SIZE)
    )

# The forward checking implementation
def forward_checking(board, domains, row, col, num):
    for i in range(SIZE):
        if board[row][i] == 0 and num in domains[(row, i)]:
            domains[(row, i)].remove(num)
            if not domains[(row, i)]:
                return False

        if board[i][col] == 0 and num in domains[(i, col)]:
            domains[(i, col)].remove(num)
            if not domains[(i, col)]:
                return False

        box_row = GRID_SIZE * (row // GRID_SIZE) + (i // GRID_SIZE)
        box_col = GRID_SIZE * (col // GRID_SIZE) + (i % GRID_SIZE)
        if board[box_row][box_col] == 0 and num in domains[(box_row, box_col)]:
            domains[(box_row, box_col)].remove(num)
            if not domains[(box_row, box_col)]:
                return False

    return True

# The MRV heuristic is to choose the variable with the smallest domain
# The Degree heuristic is to choose the variable with the most constraints on remaining variables
def select_unassigned_variable(board, domains):
    mrv = float('inf')
    highest_degree = -1
    best_cell = None

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == 0:
                domain_size = len(domains[(row, col)])
                degree = sum(1 for i in range(SIZE) if board[row][i] == 0 or board[i][col] == 0) - 2 # Subtract 2 for the current cell being counted twice

                if domain_size < mrv or (domain_size == mrv and degree > highest_degree):
                    mrv = domain_size
                    highest_degree = degree
                    best_cell = (row, col)

    return best_cell

# The backtracking implementation
def backtrack(board, domains, assignments=[]):
    # If four assignments have been made, print them
    if len(assignments) == 4:
        for assign in assignments:
            print(f"Variable: {assign['var']}, Domain Size: {assign['domain_size']}, Degree: {assign['degree']}, Value Assigned: {assign['value']}")
        # Exit after printing the first 4 assignments
        return True

    unassigned = select_unassigned_variable(board, domains)
    
    # If there is no unassigned variable, we're done
    if not unassigned:
        return True

    row, col = unassigned
    domain_size = len(domains[(row, col)])
    degree = sum(1 for i in range(SIZE) if board[row][i] == 0 or board[i][col] == 0) - 2

    for num in domains[(row, col)]:
        if is_valid_assignment(board, row, col, num):
            board[row][col] = num
            assignments.append({'var': (row, col), 'domain_size': domain_size, 'degree': degree, 'value': num})
            domains_copy = {k: v.copy() for k, v in domains.items()}
            if forward_checking(board, domains_copy, row, col, num):
                if backtrack(board, domains_copy, assignments):
                    return True
            # Undo the current cell for backtracking
            board[row][col] = 0
            assignments.pop()

    return False

# Driver Function
def solve_sudoku(board):
    domains = {(row, col): set(range(1, SIZE + 1)) for row in range(SIZE) for col in range(SIZE) if board[row][col] == 0}
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] != 0:
                if not forward_checking(board, domains, row, col, board[row][col]):
                    return False
    return backtrack(board, domains, assignments=[])


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

sudokuExample = [
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

puzzles = [sudoku1, sudoku2, sudoku3]

for puzzle in puzzles:
    start_time = time.time()
    if solve_sudoku(puzzle):
        print("Solved Sudoku:")
        for row in puzzle:
            print(row)
    else:
        print("No solution found")

    elapsed_time = time.time() - start_time
    if elapsed_time > 3600:
        print("Execution time exceeded 1 hour.")
    else:
        print(f"Execution time: {elapsed_time} seconds")