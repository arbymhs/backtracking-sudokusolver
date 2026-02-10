from tkinter import *
from tkinter import ttk
import Solver
import BranchAndBound
import time

root = Tk()
root.title("Sudoku Solver Comparison - Tugas Akhir")
root.geometry("400x850")

solved_cells = []

def toggle_pin():
    root.attributes("-topmost", pin_var.get())

def stop_process():
    Solver.stop_flag = True
    BranchAndBound.stop_flag = True
    statusLabel.configure(text="PROSES DIHENTIKAN OLEH PENGGUNA", fg="orange")
    btn_stop.pack_forget()

def clear_solution():
    global solved_cells
    for r, c in solved_cells:
        cells[(r, c)].delete(0, END)
        cells[(r, c)].configure(fg="black")
    solved_cells = []
    btn_clear_sol.pack_forget() 
    statusLabel.configure(text="Solusi dihapus. Angka awal dipertahankan.", fg="blue")

def clear_all():
    global solved_cells
    for r in range(1, 10):
        for c in range(1, 10):
            cells[(r, c)].delete(0, END)
            cells[(r, c)].configure(fg="black", bg=("#D0FFFF" if ((r-1)//3+(c-1)//3)%2==0 else "#ffffd0"))
    solved_cells = []
    btn_clear_sol.pack_forget()
    statusLabel.configure(text="", fg="black")

Label(root, text="Analisa Perancangan Algoritma", font=("Arial", 10)).grid(row=0, column=1, columnspan=9)
Label(root, text="SUDOKU SOLVER COMPARISON", font=("Arial", 12, "bold")).grid(row=1, column=1, columnspan=9, pady=5)

upper_frame = Frame(root)
upper_frame.grid(row=2, column=1, columnspan=9, pady=5)

pin_var = BooleanVar()
Checkbutton(upper_frame, text="Always on top", variable=pin_var, command=toggle_pin).pack(side=LEFT, padx=5)

show_process_var = BooleanVar(value=False)
Checkbutton(upper_frame, text="Tampilkan Proses", variable=show_process_var).pack(side=LEFT, padx=5)

algo_var = StringVar(value="Backtracking")
ttk.Combobox(root, textvariable=algo_var, values=["Backtracking", "Backtracking with MRV"], state="readonly").grid(row=14, column=1, columnspan=9, pady=5)

message_frame = Frame(root, height=50)
message_frame.grid(row=16, column=1, columnspan=9, pady=5)
message_frame.grid_propagate(False)
statusLabel = Label(message_frame, text="", font=("Arial", 9, "bold"), wraplength=350)
statusLabel.pack(expand=True)

analysisLabel = Label(root, text="Statistik Performa:\n-", fg="blue", justify="left", font=("Arial", 9, "italic"))
analysisLabel.grid(row=22, column=1, columnspan=9, pady=10)

cells = {}


def visual_update(r, c, v, color):
    if Solver.stop_flag or BranchAndBound.stop_flag:
        return
    cells[(r+1, c+1)].delete(0, END)
    cells[(r+1, c+1)].insert(0, v)
    cells[(r+1, c+1)].configure(fg=color)
    root.update()

def on_key_release(event, row, col):
    val = event.widget.get()
    if len(val) == 1:
        nr, nc = (row, col + 1) if col < 9 else (row + 1, 1)
        if (nr, nc) in cells:
            cells[(nr, nc)].focus_set()

def ValidateNumber(P):
    if P == "": return True
    if P.isdigit() and len(P) == 1 and P != '0':
        return True
    return False

reg = root.register(ValidateNumber)

def draw9x9Grid():
    for r in range(1, 10):
        for c in range(1, 10):
            color = "#D0FFFF" if ((r-1)//3 + (c-1)//3) % 2 == 0 else "#ffffd0"
            e = Entry(root, width=5, bg=color, justify="center", validate="key", 
                      validatecommand=(reg, "%P"), font=("Arial", 10, "bold"), fg="black")
            e.grid(row=r+3, column=c, sticky="nsew", padx=1, pady=1, ipady=5)
            e.bind("<KeyRelease>", lambda ev, r=r, c=c: on_key_release(ev, r, c))
            cells[(r, c)] = e

def isBoardValid(board):
    for r in range(9):
        for c in range(9):
            num = board[r][c]
            if num != 0:
                board[r][c] = 0
                if not Solver.isSafe(board, r, c, num):
                    board[r][c] = num
                    return False, r, c
                board[r][c] = num
    return True, -1, -1

def getValues():
    Solver.stop_flag = False
    BranchAndBound.stop_flag = False
    btn_clear_sol.pack_forget()
    
    board = [[0 if cells[(r,c)].get()=="" else int(cells[(r,c)].get()) for c in range(1,10)] for r in range(1,10)]
    valid, er, ec = isBoardValid(board)
    if not valid:
        statusLabel.configure(text=f"ERROR: Angka sama di B{er+1}, K{ec+1}", fg="red")
        cells[(er+1, ec+1)].configure(bg="#FFCCCC")
        return 
    
    if show_process_var.get():
        btn_stop.pack(side=LEFT, padx=2, after=btn_solve)
    
    updateValues(board)
    btn_stop.pack_forget()

def updateValues(s):
    global solved_cells
    solved_cells = []
    orig = [(r, c) for r in range(1, 10) for c in range(1, 10) if cells[(r, c)].get() != ""]
    sel = algo_var.get()
    callback = visual_update if show_process_var.get() else None
    
    statusLabel.configure(text=f"Menjalankan {sel}...", fg="blue")
    
    if sel == "Backtracking":
        sol, ops, tm = Solver.Solver(s, callback)
    else:
        sol, ops, tm = BranchAndBound.HeuristicSolver(s, callback)
    
    if Solver.stop_flag or BranchAndBound.stop_flag: return

    if sol != "no":
        for r in range(1, 10):
            for c in range(1, 10):
                if (r, c) not in orig:
                    cells[(r, c)].delete(0, END)
                    cells[(r, c)].insert(0, sol[r-1][c-1])
                    cells[(r, c)].configure(fg="green")
                    solved_cells.append((r, c))
        
        statusLabel.configure(text=f"SOLUSI DITEMUKAN ({sel})", fg="green")
        analysisLabel.configure(text=f"Statistik {sel}:\nOperasi Dasar: {ops} kali\nWaktu: {tm:.2f} ms")
        btn_clear_sol.pack(side=LEFT, padx=2, after=btn_solve) 
    else:
        statusLabel.configure(text="TIDAK ADA SOLUSI", fg="red")

draw9x9Grid()
btn_frame = Frame(root)
btn_frame.grid(row=20, column=1, columnspan=9, pady=15)

btn_solve = Button(btn_frame, text="Solve", command=getValues, width=9, bg="#4CAF50", fg="white", font=("Arial", 8, "bold"))
btn_solve.pack(side=LEFT, padx=2)

btn_stop = Button(btn_frame, text="Stop", command=stop_process, width=8, bg="#f44336", fg="white", font=("Arial", 8, "bold"))

btn_clear_sol = Button(btn_frame, text="Clear Sol", command=clear_solution, width=9, bg="#FF9800", fg="white", font=("Arial", 8, "bold"))

btn_clear = Button(btn_frame, text="Clear All", command=clear_all, width=9, font=("Arial", 8, "bold"))
btn_clear.pack(side=LEFT, padx=2)

root.mainloop()