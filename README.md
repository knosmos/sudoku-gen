# sudoku-gen
I like playing sudoku. I don't like paying for sudoku books. So, I made this: a simple program to generate sudoku puzzle PDFs. Also features QR code solutions.

![image](https://user-images.githubusercontent.com/30610197/149524429-65066143-dc10-44a5-b363-195429376460.png)

## Installation
### Dependencies

- `pillow`
- `fpdf`
- `click`

### Usage
```
py render.py [OPTIONS]

Options:
  -s INTEGER  Number of sets to generate
  -d INTEGER  Number of squares to remove (not guarenteed, as program will stop after a certain threshold)
  -l / -p     Landscape/Portrait mode
  -c          Color mode
  -a          Arrange puzzles with solutions (as opposed to separating them)
  -o / -n     Open/Don't open result pdf in web browser
  --help      Show this message and exit.
```

## Example
[Sample Output](https://github.com/knosmos/sudoku-gen/blob/master/res/res.pdf)
