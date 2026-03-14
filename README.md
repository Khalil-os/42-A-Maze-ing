*This project has been created as part of the 42 curriculum by kriad, aredouan*

# A-Maze-ing

## Description

A-Maze-ing is a Python project that generates and displays a random maze based on a configuration file.  
The program reads parameters such as maze size, entry and exit positions, and generation options from the configuration file, then builds a valid maze and displays it.

The maze can optionally be a **perfect maze**, meaning there is exactly one possible path between the entry and exit.

The generated maze is:
- Displayed visually (terminal or graphical window)
- Saved to an output file using a hexadecimal wall representation
- Guaranteed to be valid and coherent

This project also includes a **reusable maze generation module** that can be installed as a Python package.

---

# Instructions

## Requirements

- Python 3.10+
- pip
- virtualenv (recommended)

## Installation

Clone the repository:

```bash
git clone <repo_url>
cd a-maze-ing
```
Install dependencies:
```bash
make install
```
Run the program:
```bash
make run
```
Or directly:
```bash
python3 a_maze_ing.py config.txt
```
Debug mode:
```bash
make debug
```
Code checks:
```bash
make lint
```

## Configuration File

The configuration file defines how the maze should be generated.

Each line follows this format:
```bash
KEY=VALUE
```
Lines beginning with # are comments.

Example:
```bash
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```
Parameters
```bash
Key	            Description

WIDTH	        Width of the maze
HEIGHT	        Height of the maze
ENTRY	        Entry coordinates (x,y)
EXIT	        Exit coordinates (x,y)
OUTPUT_FILE	    Output file name
PERFECT	        Whether the maze must be perfect
```
Optional parameters can be added such as:
```bash
SEED=42
```

## Maze Generation Algorithm
This project uses the Recursive Backtracking algorithm.

Why this algorithm?

It was chosen because:
- It produces perfect mazes
- It is simple and efficient
- It generates visually interesting labyrinths
- It is widely used in procedural generation

The algorithm works by:
- Start from an initial cell
- Mark the cell as visited
- Randomly choose an unvisited neighbor
- Remove the wall between the cells
- Recursively continue the process
- Backtrack when no neighbors remain
- This ensures the maze remains fully connected.

## Reusable Maze Generator Module

The maze generator is implemented as a reusable Python module called:
```bash
mazegen
```
The core class is:
```bash
MazeGenerator
```
Example usage:
```bash
from mazegen.generator import MazeGenerator

generator = MazeGenerator(width=20, height=15, seed=42)
maze = generator.generate()

path = generator.solve()
```
The module allows:
- generating a maze
- accessing maze structure
- computing the shortest path
- controlling generation parameters

The package can be installed via pip from the generated archive:
```bash
mazegen-*.tar.gz
```
## Interactive Controls

During execution, the user can interact with the maze.

Available commands:
```bash
Key	    Action

r	    Regenerate a new maze
s	    Show or hide the shortest path
c	    Change wall color
q	    Quit the program
```

## 42 Pattern

The maze generator reserves specific cells to draw a “42” pattern inside the maze.

If the maze dimensions are too small to contain the pattern, the program prints an error message and continues without it.
## Output File Format

The maze is saved using a hexadecimal representation of walls.

Each cell is encoded using 4 bits:
```bash
Bit	    Direction

0	    North
1	    East
2	    South
3	    West
```
Example:
```bash
A3F1
BC42
...
```

After the maze grid, the file also contains:
- entry coordinates
- exit coordinates
- shortest path (N,E,S,W)

## Team and Project Management

### Roles

- kriad
    - Maze generation algorithm
    - Path solving logic
    - Output file generation
- aredouan
    - Configuration parser
    - Visualization system
    - Packaging module

### Planning

Initial plan:
1. Configuration parser
2. Maze generation
3. Path solver
4. Visualization
5. Packaging reusable module

Evolution:
- Added seed support for reproducibility
- Improved error handling
- Added modular architecture

### What worked well

- Clear separation between modules
- Use of Python typing and docstrings
- Early testing of generation logic

### What could be improved

- More unit tests
- Additional maze algorithms
- Better visualization features

### Tools Used

- Python
- flake8
- mypy
- Git
- Virtualenv
- ChatGPT (used for documentation explanations and algorithm research)

## Resources

Maze generation algorithms:
- https://en.wikipedia.org/wiki/Maze_generation_algorithm
- https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithms

Python packaging:
- https://packaging.python.org

Graph theory and spanning trees:
- https://en.wikipedia.org/wiki/Spanning_tree

### AI usage
AI tools were used to:

- help explain maze algorithms
- assist in writing documentation
- review Python structure

All generated code and explanations were reviewed and understood before integration.

## Bonuses

added animation for the path solving