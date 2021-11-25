from PIL import Image, ImageDraw, ImageFont
import gen
from fpdf import FPDF
import click

FONT = ImageFont.truetype("helvetica.ttf", 100)
CELL = 100 # Pixel size of sudoku cell
BOLD = 6 # Thickness of bold lines
THIN = 2 

def renderBoard(board, highlight=[1]*81):
    # create image
    out = Image.new("RGB", (CELL * 9 + 8, CELL * 9 + 8), (255, 255, 255))

    # drawing context
    d = ImageDraw.Draw(out)

    # draw grid
    for col in range(10):
        if col % 3 == 0:
            w = BOLD
        else:
            w = THIN
        d.line([col*CELL + 4, 4, col*CELL + 4, 9*CELL + 4], width=w, fill=(0,0,0))
    for row in range(10):
        if row % 3 == 0:
            w = BOLD
        else:
            w = THIN
        d.line([2, row*CELL + 4, 9*CELL + 4, row*CELL + 4], width=w, fill=(0,0,0))

    # draw board text
    for i in range(81):
        if board[i] != 0: 
            row = i // 9
            col = i % 9
            if highlight[i] != 0:
                fill = (0,0,0)
            else:
                fill = (200,200,200)
            d.text((CELL*col + 30, CELL*row + 10), str(board[i]), font=FONT, fill=fill)
    return out

def generateImg(num=1, difficulty=50, set=1):
    for i in range(num):
        print(f"generating {i+1} of {num}...")
        board, solution = gen.generate(difficulty)
        renderBoard(board).save(f"tmp/board{set}_{i}.png")
        renderBoard(solution, highlight=board).save(f"tmp/solution{set}_{i}.png")

def generatePDF(sets, difficulty, landscape_mode):
    # Writes [sets] sets with 2 pages each; 1st contains six puzzles, and 2nd contains solutions

    if landscape_mode:
        pdf = FPDF('L', 'mm', 'Letter')
        h = 216
        w = 279 - 20
    else:
        pdf = FPDF('P', 'mm', 'Letter')
        w = 216
        h = 279 - 20        
    
    pdf.set_auto_page_break(0)
    
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

    if landscape_mode:
        positions = [
            (0,0),
            (0,w/3),
            (0,2*w/3),
            (h/2,0),
            (h/2,w/3),
            (h/2,2*w/3)
        ]

    for k in range(sets):
        print(f"\033[96mgenerating set {k+1} of {sets} --------\033[0m")
        generateImg(num=6, difficulty=difficulty, set=k)

        pdf.add_page()

        for i in range(6):
            pdf.image(f"tmp/board{k}_{i}.png", h=80, x=int(positions[i][1])+px, y=int(positions[i][0])+py)
        
        pdf.add_page()

        for i in range(6):
            pdf.image(f"tmp/solution{k}_{i}.png", h=80, x=int(positions[i][1])+px, y=int(positions[i][0])+py)
    
    pdf.output("res/res.pdf","F")
    print("Generation complete - file stored in /res")

@click.command()
@click.option('-s', default=3, help='Number of sets to generate')
@click.option('-d', default=40, help='Difficulty of puzzles')
@click.option('-l/-p', default=False, help="Landscape/Portrait mode")

def run(s, d, l):
    generatePDF(s,d,l)
run()