# from rich import print

def valid(board, cell):
    row = cell // 9
    col = cell % 9
    
    # check column
    for i in range(col, 73+col, 9):
        if board[i] == board[cell] and i != cell:
            return False
    #print("passed col")
    # check row
    for i in range(row*9, row*9+9):
        if board[i] == board[cell] and i != cell:
            return False
    #print("passed row")
    # check box
    x = col // 3
    y = row // 3

    for i in range(y*3, y*3 + 3):
        for j in range(x*3, x*3 + 3):
            if board[i*9 + j] == board[cell] and i*9+j != cell:
                return False
    #print("passed box")
    return True

def solve(board):
    '''
    Solves board, a 1d array of len 81 containing sudoku grid (left -> right and
    top -> bottom); 0 represents blank
    Returns list of all solutions
    '''

    '''
    0  1  2  3  4  5  6  7  8
    9  10 11 12 13 14 15 16 17
    18 19 20 21 22 23 24 25 26
    27 28 29 30 31 32 33 34 35
    36 37 38 39 40 41 42 43 44
    45 46 47 48 49 50 51 52 53
    54 55 56 57 58 59 60 61 62
    63 64 65 66 67 68 69 70 71
    72 73 74 75 76 77 78 79 80
    '''

    checks = []
    boxes = [
        [0,1,2, 9,10,11,  18,19,20],
        [3,4,5, 12,13,14, 21,22,23],
        [6,7,8, 15,16,17, 24,25,26],
        
        [27,28,29, 36,37,38, 45,46,47],
        [30,31,32, 39,40,41, 48,49,50],
        [33,34,35, 42,43,44, 51,52,53],
        
        [54,55,56, 63,64,65, 72,73,74],
        [57,58,59, 66,67,68, 75,76,77],
        [60,61,62, 69,70,71, 78,79,80]
    ]
    columns = [list(range(i,73+i,9)) for i in range(9)]
    rows = [list(range(i*9,i*9+9)) for i in range(9)]

    checks = boxes + columns + rows

    currentCell = 0
    solution = [0]*81
    while currentCell != 81:
        if board[currentCell] != 0:
            solution[currentCell] = board[currentCell]
            if valid(solution, currentCell):
                currentCell += 1
            else:
                # backtrack
                currentCell -= 1
                while board[currentCell] != 0:
                    currentCell -= 1
        else:
            solution[currentCell] += 1
            if solution[currentCell] > 9:
                solution[currentCell] = 0
                # backtrack
                currentCell -= 1
                while board[currentCell] != 0:
                    currentCell -= 1
            else:
                '''for check in checks:
                    checklist = [solution[i] for i in check if solution[i] != 0]
                    if len(checklist) != len(set(checklist)):
                        break
                    
                    arr = [0]*10
                    fail = False
                    for i in check:
                        if solution[i] != 0:
                            if arr[solution[i]] == 0:
                                arr[solution[i]] = 1
                            else:
                                fail = True
                    if fail: break'''
                if valid(solution, currentCell):
                    currentCell += 1
        #print(currentCell, solution)
    print("\n".join([str([solution[k] for k in range(i*9,i*9+9)]) for i in range(9)]))

solve([
    5,3,0, 0,7,0, 0,0,0,
    6,0,0, 1,9,5, 0,0,0,
    0,9,8, 0,0,0, 0,6,0,
    
    8,0,0, 0,6,0, 0,0,3,
    4,0,0, 8,0,3, 0,0,1,
    7,0,0, 0,2,0, 0,0,6,

    0,6,0, 0,0,0, 2,8,0,
    0,0,0, 4,1,9, 0,0,5,
    0,0,0, 0,8,0, 0,7,9
])

#print(valid([5, 3, 4, 6, 7, 8, 1, 9, 2, 6, 7, 2, 1, 9, 5, 3, 4, 8, 1, 9, 8, 3, 4, 2, 5, 6, 7, 8, 5, 9, 7, 6, 1, 4, 2, 3, 4, 2, 6, 8, 5, 3, 9, 7, 1, 7, 1, 3, 9, 2, 4, 8, 5, 6, 9, 6, 1, 5, 3, 7, 2, 8, 4, 2, 8, 7, 4, 1, 9, 6, 3, 5, 3, 4, 5, 2, 8, 6, 7, 7, 9], 78))