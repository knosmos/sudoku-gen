import copy, random

def printBoard(board):
    print("\n".join([str([board[k] for k in range(i*9,i*9+9)]) for i in range(9)]))

def valid(board, cell):
    row = cell // 9
    col = cell % 9
    # check column
    for i in range(col, 73+col, 9):
        if board[i] == board[cell] and i != cell:
            return False
    # check row
    for i in range(row*9, row*9+9):
        if board[i] == board[cell] and i != cell:
            return False
    # check box
    x = col // 3
    y = row // 3
    for i in range(y*3, y*3 + 3):
        for j in range(x*3, x*3 + 3):
            if board[i*9 + j] == board[cell] and i*9+j != cell:
                return False
    return True

def solve(board, findunique = True):
    '''
    Solves board, a 1d array of len 81 containing sudoku grid (left -> right and
    top -> bottom); 0 represents blank
    Returns list of all solutions
    '''

    currentCell = 0
    solutions = []
    solution = copy.deepcopy(board)
    while currentCell >= 0:
        while currentCell != 81:
            if currentCell <= -1:
                break # No more solutions
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
                    if valid(solution, currentCell):
                        currentCell += 1
            #print("\n".join([str([solution[k] for k in range(i*9,i*9+9)]) for i in range(9)])+"\n")
        else:
            #print("\n".join([str([solution[k] for k in range(i*9,i*9+9)]) for i in range(9)]))
            #print()
            solutions.append(copy.deepcopy(solution))
            if findunique and len(solutions) == 1:
                # backtrack
                currentCell -= 1
                while board[currentCell] != 0:
                    currentCell -= 1
            else:
                break
    #print("\n".join([str([solution[k] for k in range(i*9,i*9+9)]) for i in range(9)]))
    return solutions
'''
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
])'''

#solve([1,2,3,4,5,6,7,8,9,4,5,6,7,8,9,1,2,3]+[0]*63)

def removeSquares(n, board):
    while True:
        square = random.randint(0,80)
        while board[square] == 0:
            square = random.randint(0,80)
        b = copy.deepcopy(board)
        b[square] = 0
        if len(solve(b)) >= 2:
            continue
        if n == 0:
            return b
        else:
            return removeSquares(n-1, b)

def generate(difficulty):
    # Fill in starter squares
    board = [0] * 81
    rand = []
    m = list(range(1,10))
    for i in range(3):
        random.shuffle(m)
        rand.append(copy.deepcopy(m))
    print(rand)
    for k in range(3):
        box = []
        c = 0
        for i in range(k*3, k*3 + 3):
            for j in range(k*3, k*3 + 3):
                board[i*9 + j] = rand[k][c]
                c += 1
    '''n = list(set(list(range(1,10)))-set(rand[0][:3]))
    random.shuffle(n)
    for i in range(6):
        board[i+3] = n[i]'''
    #print("scaffold:")
    #print("\n".join([str([board[k] for k in range(i*9,i*9+9)]) for i in range(9)]))
    print("\nfilled:")
    board = solve(board, findunique = False)[0]
    printBoard(board)

    # remove squares one at a time
    print("\ncomplete:")
    final = removeSquares(difficulty, board)
    printBoard(final)
    return final, board # puzzle, solution

generate(50)