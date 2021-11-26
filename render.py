from PIL import Image, ImageDraw, ImageFont
import gen
from fpdf import FPDF
import click
import time, os, sys, math
import webbrowser

FONT = ImageFont.truetype("helvetica.ttf", 100)
CELL = 100 # Pixel size of sudoku cell
BOLD = 6 # Thickness of bold lines
THIN = 2

def progressBar(width,i,n,item):
    sys.stdout.write(f"\r|{'#'*math.ceil(i/n*width)}{'.'*math.floor(width-i/n*width)}|\033[96m {item} {i} of {n}\033[0m\r")
    sys.stdout.flush()

def renderBoard(board, highlight=[1]*81, highlight_color=(0,0,0)):
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
                fill = highlight_color
            d.text((CELL*col + 30, CELL*row + 10), str(board[i]), font=FONT, fill=fill)
    return out

def generateImg(num=1, difficulty=50, set=1, highlight_color=(0,0,0)):
    for i in range(num):
        # print(f"puzzle {i+1} of {num}...")
        progressBar(15,i+1,num,"puzzle")
        board, solution = gen.generate(difficulty)
        renderBoard(board).save(f"tmp/board{set}_{i}.png")
        renderBoard(solution, highlight=board, highlight_color=highlight_color).save(f"tmp/solution{set}_{i}.png")

def generatePDF(sets, difficulty, landscape_mode, color_mode, collate):
    # Writes [sets] sets with 2 pages each; 1st contains six puzzles, and 2nd contains solutions

    if landscape_mode:
        pdf = FPDF('L', 'mm', 'Letter')
        h = 216
        w = 279 - 20
    else:
        pdf = FPDF('P', 'mm', 'Letter')
        w = 216
        h = 279 - 20

    if color_mode:
        highlight_color = (83, 183, 237)
        info_color = (6, 119, 194)
    else:
        highlight_color = (200, 200, 200)
        info_color = (100, 100, 100)
    
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

    pdf.set_font("Arial", "", 20)

    sys.stdout.write("\n")
    sys.stdout.flush()
    for k in range(sets):
        sys.stdout.write("\x1b[1A")
        sys.stdout.flush()
        progressBar(15,k+1,sets,"set")
        sys.stdout.write("\n")
        sys.stdout.flush()
        generateImg(num=6, difficulty=difficulty, set=k, highlight_color=highlight_color)
        
        pdf.add_page()
        for i in range(6):
            pdf.image(f"tmp/board{k}_{i}.png", h=80, x=int(positions[i][1])+px, y=int(positions[i][0])+py)
        if landscape_mode:
            pdf.set_text_color(0,0,0)
            pdf.text(15, int(h/2), "sudoku-gen")
            pdf.set_text_color(info_color[0],info_color[1],info_color[2])
            pdf.text(100, int(h/2), f"set {k+1} of {sets}   /   created {time.strftime('%Y-%m-%d %H:%M')}")
        if collate:
            pdf.add_page()
            for i in range(6):
                pdf.image(f"tmp/solution{k}_{i}.png", h=80, x=int(positions[i][1])+px, y=int(positions[i][0])+py)
            if landscape_mode:
                pdf.set_text_color(0,0,0)
                pdf.text(15, int(h/2), "sudoku-gen")
                pdf.set_text_color(info_color[0],info_color[1],info_color[2])
                pdf.text(100, int(h/2), f"set {k+1} of {sets}   /   created {time.strftime('%Y-%m-%d %H:%M')}   /   solution")
    if not collate:
        for k in range(sets):
            pdf.add_page()
            for i in range(6):
                pdf.image(f"tmp/solution{k}_{i}.png", h=80, x=int(positions[i][1])+px, y=int(positions[i][0])+py)
            if landscape_mode:
                pdf.set_text_color(0,0,0)
                pdf.text(15, int(h/2), "sudoku-gen")
                pdf.set_text_color(info_color[0],info_color[1],info_color[2])
                pdf.text(100, int(h/2), f"set {k+1} of {sets}   /   created {time.strftime('%Y-%m-%d %H:%M')}   /   solution")
    
    print()
    print("Writing pdf...")
    pdf.output("res/res.pdf","F")
    print("Generation complete - file stored in /res")

@click.command()
@click.option('-s', default=3, help='Number of sets to generate')
@click.option('-d', default=40, help='Difficulty of puzzles')
@click.option('-l/-p', default=True, help="Landscape/Portrait mode")
@click.option('-c', is_flag=True, default=False, help='Color mode')
@click.option('-a', is_flag=True, default=False, help='Arrange puzzles with solutions (as opposed to separating them)')
@click.option("-o/-n", default=True, help="Open/Don't open result pdf in web browser")

def run(s, d, l, c, a, o):
    # Make folders if necessary
    try:
        os.mkdir("tmp")
        print("\033[93mcreated /tmp/ directory\033[0m")
    except FileExistsError:
        pass
    try:
        os.mkdir("res")
        print("\033[93mcreated /res/ directory\033[0m")
    except FileExistsError:
        pass

    # Generate PDFs
    generatePDF(s,d,l,c,a)
    if o:
        print("Opening result pdf in browser...")
        webbrowser.open(os.path.dirname(os.path.abspath(__file__))+"/res/res.pdf")

if __name__ == "__main__":
    run()