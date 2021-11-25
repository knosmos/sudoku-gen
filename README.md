# sudoku-gen

A simple program to generate sudoku puzzle PDFs.

```
Usage: render.py [OPTIONS]

Options:
  -s INTEGER  Number of sets to generate
  -d INTEGER  Number of squares to remove (not guarenteed, as program will stop after a certain threshold)
  -l / -p     Landscape/Portrait mode
  -c          Color mode
  --help      Show this message and exit.
```

## Example
### Puzzle
![image](https://user-images.githubusercontent.com/30610197/143372845-4acfa2d6-7d4b-48de-9240-723af6e241e6.png)

### Solution
![image](https://user-images.githubusercontent.com/30610197/143372875-ffc9d377-f1c1-42e3-92e4-61a0a1afa825.png)

## Dependencies

- pillow
- fpdf
- click