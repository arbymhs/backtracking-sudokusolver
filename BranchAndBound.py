import time

stop_flag = False
mrv_operations = 0

def get_candidates(sudoku, row, col):
    candidates = set(range(1, 10))
    for i in range(9):
        candidates.discard(sudoku[row][i])
        candidates.discard(sudoku[i][col])
    sr, sc = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            candidates.discard(sudoku[sr + i][sc + j])
    return candidates

def find_mrv_cell(sudoku):
    best_cell, min_c = None, 10
    for r in range(9):
        for c in range(9):
            if sudoku[r][c] == 0:
                num_c = len(get_candidates(sudoku, r, c))
                if num_c == 0: 
                    return (r, c), 0
                if num_c < min_c:
                    min_c, best_cell = num_c, (r, c)
    return best_cell, min_c

def solveMRV(sudoku, ui_callback=None):
    global mrv_operations, stop_flag
    if stop_flag: return False
    
    mrv_operations += 1
    
    cell, num_c = find_mrv_cell(sudoku)
    
    if cell is None: return True
    if num_c == 0: return False
    
    r, c = cell
    for num in get_candidates(sudoku, r, c):
        sudoku[r][c] = num
        
        if ui_callback: 
            ui_callback(r, c, num, "green")
            
        if solveMRV(sudoku, ui_callback): return True
        
        sudoku[r][c] = 0
        if ui_callback: ui_callback(r, c, "", "red")
        
    return False

def HeuristicSolver(sudoku, ui_callback=None):
    global mrv_operations, stop_flag
    mrv_operations = 0
    stop_flag = False
    
    start_time = time.time()
    success = solveMRV(sudoku, ui_callback)
    exec_time = (time.time() - start_time) * 1000
    
    return (sudoku if success else "no"), mrv_operations, exec_time