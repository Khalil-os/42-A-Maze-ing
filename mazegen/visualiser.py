from typing import Dict, Tuple, Any
import os
from .generator import MazeGenerator
import time

north: int = 1
east: int = 2
south: int = 4
west: int = 8

Dx = {north: 0, south: 0, east: 1, west: -1}
Dy = {north: -1, south: 1, east: 0, west: 0}


Opposite: Dict[int, int] = {north: south,
                            south: north,
                            east: west,
                            west: east
                            }


class MazeVisualizer():
    """Handles visualization and interaction with the generated maze."""

    class Style:
        """ANSI styles, colors, and characters used for rendering."""
        RESET = "\033[0m"
        BOLD = "\033[1m"
        # Colors
        white = "\033[97m"    # Walls
        entry = "\033[95m"  # Entry
        red = "\033[91m"      # Exit
        gray = "\033[94m"     # 42 Pattern
        green = "\033[92m"    # Path Solution

        # Characters
        block = "██"
        space = "  "

    def __init__(self, width: int, height: int, entry: Tuple[int, int],
                 exite: Tuple[int, int], perfect: bool = True,
                 seed: int | None = None) -> None:
        """Initialize the visualizer and generate the maze."""
        self.width = width
        self.height = height
        self.perfect = perfect
        self.seed = seed
        self.maze = MazeGenerator(width, height, perfect, seed)
        self.maze.run(0, 0)
        self.show_path = False
        self.entry = entry if entry else (0, 0)
        self.exite = exite if exite else (width - 1, height - 1)
        self.wall_colors = [
            "\033[97m",  # White (Default)
            "\033[93m",  # Yellow
            "\033[96m",  # Cyan
            "\033[33m",  # Orange/Brown
            "\033[35m"   # Magenta
        ]
        self.color_idx = 0

    def render(self) -> None:
        """Render the maze grid in the terminal."""
        print("\033[H", end="")
        map_h: int = self.height * 2 + 1
        map_w: int = self.width * 2 + 1
        current_wall_color = self.wall_colors[self.color_idx]
        colored_wall = current_wall_color + self.Style.block + self.Style.RESET

        v_grid = [[colored_wall for _ in range(map_w)]
                  for _ in range(map_h)]
        should_draw_path = self.show_path and self.maze.solution_cells

        for y in range(self.height):
            for x in range(self.width):
                vx = x * 2 + 1
                vy = y * 2 + 1
                is_path = (should_draw_path and (x, y) in
                           self.maze.solution_cells)

                if self.maze.grid[y][x] != 15:
                    if is_path:
                        v_grid[vy][vx] = (self.Style.green + self.Style.block +
                                          self.Style.RESET)
                    else:
                        v_grid[vy][vx] = self.Style.space

                else:
                    v_grid[vy][vx] = (self.Style.red +
                                      self.Style.block + self.Style.RESET)

                if not (self.maze.grid[y][x] & south):
                    neighboor_in_path = (should_draw_path and
                                         ((x, y+1) in self.maze.solution_cells)
                                         )

                    if is_path and neighboor_in_path:
                        v_grid[vy + 1][vx] = (self.Style.green +
                                              self.Style.block +
                                              self.Style.RESET)
                    else:
                        v_grid[vy + 1][vx] = self.Style.space

                if not (self.maze.grid[y][x] & east):
                    neighboor_in_path = (should_draw_path and
                                         ((x+1, y) in self.maze.solution_cells)
                                         )
                    if is_path and neighboor_in_path:
                        v_grid[vy][vx + 1] = (self.Style.green +
                                              self.Style.block +
                                              self.Style.RESET)
                    else:
                        v_grid[vy][vx + 1] = self.Style.space

        start = ((self.entry[0] * 2 + 1), (self.entry[1] * 2 + 1))
        goal = ((self.exite[0] * 2 + 1), (self.exite[1] * 2 + 1))

        if 0 <= start[0] < map_w and 0 <= start[1] < map_h:
            v_grid[start[1]][start[0]] = (self.Style.entry +
                                          self.Style.block + self.Style.RESET)

        if 0 <= goal[0] < map_w and 0 <= goal[1] < map_h:
            v_grid[goal[1]][goal[0]] = (self.Style.gray +
                                        self.Style.block + self.Style.RESET)
        os.system("clear")
        print(f"{self.Style.BOLD}A-Maze-ing 1337{self.Style.RESET}")
        if self.maze.pattern_omitted:
            print(f"{self.Style.red}Error: The size of the maze does not "
                  f"allow the 42 pattern to exist.{self.Style.RESET}")
        for row in v_grid:
            print("".join(row))

    def play_animation(self) -> None:
        """Animate the solving path of the maze."""
        path_list = self.maze.solve(self.entry, self.exite)
        if not path_list:
            return
        self.maze.solution_cells = set()
        os.system("clear")
        for cell in path_list:
            self.maze.solution_cells.add(cell)
            self.render()
            time.sleep(0.05)

    def validat_maze(self) -> None:
        """Validate entry and exit positions."""
        if (not (0 <= self.entry[0] < self.width) or
                not (0 <= self.entry[1] < self.height)):
            raise ValueError("your entry is not valid")

        if (not (0 <= self.exite[0] < self.width) or
                not (0 <= self.exite[1] < self.height)):
            raise ValueError("your exite is not valid")

        if self.maze.is_in_pattern(self.entry[0], self.entry[1]):
            raise ValueError("you entered invalide config"
                             "(your entry/exit is in 42_pattern)")
        if self.maze.is_in_pattern(self.exite[0], self.exite[1]):
            raise ValueError("you entered invalide config"
                             "(your entry/exit is in 42_pattern)")

    def loop(self, config: Dict[str, Any]) -> None:
        """Main interactive loop for maze control."""
        os.system("clear")
        self.validat_maze()

        while True:
            self.render()
            self.maze.solve(config['ENTRY'], config['EXIT'])
            self.maze.export_to_file(config['OUTPUT_FILE'], config['ENTRY'],
                                     config['EXIT'])
            print("enter 'r' to recreate")
            print("enter 's' to solve maze")
            print("enter 'c' to change wall color")
            print("enter 'q' to quit")
            try:
                choice = input("Choice: ").strip().lower()
                if choice == 'q':
                    break
                elif choice == 'r':
                    self.maze = MazeGenerator(self.width,
                                              self.height, self.perfect,
                                              self.seed)
                    self.maze.run(0, 0)
                    self.show_path = False
                    os.system("clear")
                elif choice == 's':
                    if not self.show_path:
                        self.show_path = True
                        self.play_animation()
                    else:
                        self.show_path = False
                        self.maze.solution_cells = set()
                        os.system("clear")
                elif choice == 'c':
                    self.color_idx = ((self.color_idx + 1) %
                                      len(self.wall_colors))
            except (EOFError, KeyboardInterrupt):
                break
