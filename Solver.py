import time

N = 9
operations_count = 0

def isSafe(sudoku, row, col, num):
    global operations_count
    operations_count += 1
    for i in range(9):
        if sudoku[row][i] == num: return False
    for i in range(9):
        if sudoku[i][col] == num: return False
    sr, sc = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if sudoku[sr + i][sc + j] == num: return False
    return True

def solveSudoku(sudoku, row, col, ui_callback=None):
    if row == N - 1 and col == N: return True
    if col == N:
        row += 1
        col = 0
    if sudoku[row][col] > 0:
        return solveSudoku(sudoku, row, col + 1, ui_callback)
    
    for num in range(1, N + 1):
        if isSafe(sudoku, row, col, num):
            sudoku[row][col] = num
            if ui_callback: ui_callback(row, col, num, "green")
                
            if solveSudoku(sudoku, row, col + 1, ui_callback):
                return True
        
        sudoku[row][col] = 0
        if ui_callback: ui_callback(row, col, "", "red")
            
    return False

def Solver(sudoku, ui_callback=None):
    global operations_count
    operations_count = 0 
    start_time = time.time()
    success = solveSudoku(sudoku, 0, 0, ui_callback)
    exec_time = (time.time() - start_time) * 1000 
    return (sudoku if success else "no"), operations_count, exec_time