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

## Dependencies

- pillow
- fpdf
- click

## Example
### Puzzle
![image](https://user-images.githubusercontent.com/30610197/143623081-00de0f2e-7744-453f-b21e-a252b5268570.png)


### Solution
![image](https://user-images.githubusercontent.com/30610197/143623101-a6794cde-82c5-4c4d-ae62-091f659d570d.png)