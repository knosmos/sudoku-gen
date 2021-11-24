from PIL import Image, ImageDraw, ImageFont
import gen
import sys
from fpdf import FPDF

FONT = ImageFont.truetype("helvetica.ttf", 50)
CELL = 50 # Pixel size of sudoku cell
BOLD = 3 # Thickness of bold lines
THIN = 1 

def renderBoard(board, understate=[0]*81):
    # create image
    out = Image.new("RGB", (CELL * 9 + 4, CELL * 9 + 4), (255, 255, 255))

    # drawing context
    d = ImageDraw.Draw(out)

    # draw grid
    for col in range(10):
        if col % 3 == 0:
            w = BOLD
        else:
            w = THIN
        d.line([col*CELL + 2, 2, col*CELL + 2, 9*CELL + 2], width=w, fill=(0,0,0))
    for row in range(10):
        if row % 3 == 0:
            w = BOLD
        else:
            w = THIN
        d.line([2, row*CELL + 2, 9*CELL + 2, row*CELL + 2], width=w, fill=(0,0,0))

    # draw board text
    for i in range(81):
        if board[i] != 0: 
            row = i // 9
            col = i % 9
            if understate[i] != 0:
                fill = (200,200,200)
            else:
                fill = (0,0,0)
            d.text((CELL*col + 15, CELL*row + 5), str(board[i]), font=FONT, fill=fill)
    return out

def generateImg(num=1, difficulty=50):
    for i in range(num):
        print(f"generating {i+1} of {num}...")
        board, solution = gen.generate(difficulty)
        renderBoard(board).save(f"tmp/board{i}.png")
        renderBoard(solution, understate=board).save(f"tmp/solution{i}.png")

def generatePDF(sets, difficulty):
    # Writes [sets] pdfs with 2 pages each; 1st contains six puzzles, and 2nd contains solutions
    for k in range(sets):
        print(f"generating set {k+1} of {sets} --------")
        generateImg(num=6, difficulty=difficulty)

        pdf = FPDF('P', 'mm', 'Letter')
        pdf.set_auto_page_break(0)
        pdf.add_page()

        w = 216
        h = 279 - 20
        px = 15
        py = 10

        positions = [
            (0,0),
            (h/3,0),
            (2*h/3,0),
            (0,w/2),
            (h/3,w/2),
            (2*h/3,w/2)
        ]

        pdf.set_font('Arial')
        pdf.text(12,7, f"sudoku - difficulty {int(difficulty/81*100)}%")

        for i in range(6):
            pdf.image(f"tmp/board{i}.png", h=80, x=int(positions[i][1])+px, y=int(positions[i][0])+py)
        
        pdf.add_page()

        for i in range(6):
            pdf.image(f"tmp/solution{i}.png", h=80, x=int(positions[i][1])+px, y=int(positions[i][0])+py)
        pdf.output(f"res/set{k}.pdf","F")

d = 52
s = 3
if len(sys.argv) > 1:
    s = sys.argv[1]
if len(sys.argv) > 2:
    d = sys.argv[2]
generatePDF(s,d)