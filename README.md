# Sudoku Solver Comparison

## Description
A Python application designed to solve Sudoku puzzles. It offers a comparative analysis between two distinct algorithms: the standard **Backtracking algorithm** and an optimized **Backtracking algorithm with the Minimum Remaining Values (MRV) heuristic**, which is a form of Branch and Bound. The application features a user-friendly Graphical User Interface (GUI) for interactive puzzle input, visualization of the solving process, and detailed performance statistics for each algorithm.

## Features
*   **Sudoku Puzzle Solving:** Efficiently solves standard 9x9 Sudoku puzzles.
*   **Algorithm Selection:** Users can choose between:
    *   **Backtracking:** A classic recursive algorithm for constraint satisfaction problems.
    *   **Backtracking with MRV (Branch and Bound):** An optimized version that prioritizes cells with the fewest valid options, significantly reducing the search space.
*   **Graphical User Interface (GUI):** Built with `tkinter`, providing an intuitive interface for:
    *   Inputting Sudoku puzzles.
    *   Selecting the desired solving algorithm.
    *   **Optional Visualization:** Visually tracks the algorithm's progress as it fills cells and backtracks.
    *   Displaying the solved Sudoku board.
*   **Performance Analysis:** Provides key performance metrics for comparison:
    *   Number of basic operations performed.
    *   Execution time in milliseconds.
*   **"Always on Top" Functionality:** Keeps the application window visible over other applications.
*   **Process Control:** Allows users to stop the solving process at any time.
*   **Clear Options:** Buttons to clear only the solution or clear the entire board.

## Files

### `GUI.py`
This file is the main entry point of the application and handles the graphical user interface.
*   Manages the `tkinter` window, grid input for Sudoku, and all interactive elements.
*   Provides options to select algorithms, toggle visualization, and display results and statistics.
*   Acts as an orchestrator, calling functions from `Solver.py` and `BranchAndBound.py` based on user selection.
*   Includes validation for user input to ensure only valid Sudoku numbers are entered.

### `Solver.py`
Implements the standard Backtracking algorithm for solving Sudoku puzzles.
*   `isSafe(sudoku, row, col, num)`: Checks if a given number can be safely placed in a specific cell according to Sudoku rules.
*   `solveSudoku(sudoku, row, col, ui_callback)`: The core recursive backtracking function that attempts to solve the puzzle. It tries placing numbers from 1 to 9, and if a placement leads to a solution, it returns true; otherwise, it backtracks.
*   `Solver(sudoku, ui_callback)`: Initiates the solving process, measures execution time, and counts basic operations.

### `BranchAndBound.py`
Implements the Backtracking algorithm enhanced with the Minimum Remaining Values (MRV) heuristic, often referred to as Branch and Bound in this context.
*   `get_candidates(sudoku, row, col)`: Determines the set of valid numbers that can be placed in a given cell.
*   `find_mrv_cell(sudoku)`: Identifies the empty cell that has the fewest possible candidate values, which is the core of the MRV heuristic.
*   `solveMRV(sudoku, ui_callback)`: The recursive function that uses the MRV heuristic to guide the search for a solution, making it generally more efficient than plain backtracking.
*   `HeuristicSolver(sudoku, ui_callback)`: Initiates the MRV-based solving process, measures execution time, and counts basic operations.

## How to Run

1.  **Prerequisites:** Ensure you have Python installed on your system. No external libraries beyond `tkinter` (which is usually included with Python) are strictly required, but for a smoother experience, ensure your Python installation is complete.
2.  **Navigate to the Directory:** Open your terminal or command prompt and navigate to the `E:\python\fileuas` directory.
    ```bash
    cd E:\python\fileuas
    ```
3.  **Run the Application:** Execute the `GUI.py` file using Python.
    ```bash
    python GUI.py
    ```
4.  The Sudoku Solver Comparison GUI window will appear, allowing you to input a puzzle and start solving.

## Requirements
*   Python 3.x
*   `tkinter` (typically included with Python installation)
