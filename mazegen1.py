from typing import List, Dict, Tuple
import random
import sys
import os

sys.setrecursionlimit(100000)
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


class MazeGenerator:
    def __init__(self, width: int, height: int, perfect: bool = True) -> None:
        self.width = width
        self.height = height
        self.perfect = perfect
        self.entree = (0, 0)
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.pattern_42 = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2),
            (2, 3), (2, 4), (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2),
            (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)
        ]

    def get_unvisited_neighbors(
                    self, x: int, y: int) -> List[Tuple[int, int, int]]:
        neighbors: List[Tuple[int, int, int]] = []

        for direction in [north, south, east, west]:
            nx: int = x + Dx[direction]
            ny: int = y + Dy[direction]
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.visited[ny][nx]:
                    neighbors.append((direction, nx, ny))
        return neighbors

    def remove_walls(self, x: int, y: int, direction: int) -> None:
        nx: int = x + Dx[direction]
        ny: int = y + Dy[direction]
        self.grid[y][x] ^= direction
        self.grid[ny][nx] ^= Opposite[direction]

    def prottect_pattern(self):
        center_x = (self.width // 2) - 3
        center_y = (self.height // 2) - 2

        for dx, dy in self.pattern_42:
            x = center_x + dx
            y = center_y + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.visited[y][x] = True

    def generate(self, x: int, y: int) -> None:
        self.visited[y][x] = True

        while True:
            neighors = self.get_unvisited_neighbors(x, y)

            if not neighors:
                return
            direction, nx, ny = random.choice(neighors)
            self.remove_walls(x, y, direction)
            self.generate(nx, ny)

    def add_cycles(self, density: float = 0.1) -> None:
        for y in range(self.height):
            for x in range(self.width):
                directions = [north, south, east, west]
                random.shuffle(directions)
                for direction in directions:
                    nx, ny = x + Dx[direction], y + Dy[direction]
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.grid[y][x] & direction:
                            if random.random() < density:
                                self.remove_walls(x, y, direction)
                                break

    def run(self, start_x: int, start_y: int) -> None:
        self.prottect_pattern()
        self.generate(start_x, start_y)
        if not self.perfect:
            self.add_cycles()


class MazeVisualizer():

    class Style:
        RESET = "\033[0m"
        BOLD = "\033[1m"
        # Colors
        white = "\033[97m"    # Walls
        entry = "\033[95m"  # Entry
        red = "\033[91m"      # Exit
        gray = "\033[90m"     # 42 Pattern
        green = "\033[92m"    # Path Solution

        # Characters
        block = "██"
        space = "  "

    def __init__(self, width: int, height: int, perfect: bool = True) -> None:
        self.width = width
        self.height = height
        self.perfect = perfect
        self.maze = MazeGenerator(width, height, perfect)
        self.maze.run(0, 0)
        self.pattern_42 = [
                    (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2),
                    (2, 3), (2, 4), (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2),
                    (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)
                ]

    def draw_pattern_42(self, grid: List[List[str]], map_w: int, map_h: int) -> None:
        if map_w < 15 or map_h < 10:
            print("warning maze too small for 42 pattern")
            return
        center_x = (map_w // 2) - 3
        center_y = (map_h // 2) - 2

        for dx, dy in self.pattern_42:
            x = center_x + dx
            y = center_y + dy

            if 0 <= x < map_w and 0 <= y < map_h:
                grid[y][x] = (self.Style.green +
                              self.Style.block + self.Style.RESET)

    def render(self) -> None:
        os.system("clear")
        map_h: int = self.height * 2 + 1
        map_w: int = self.width * 2 + 1
        v_grid = [[self.Style.block for _ in range(map_w)] for _ in range(map_h)]

        for y in range(self.height):
            for x in range(self.width):
                vx = x * 2 + 1
                vy = y * 2 + 1
                if self.maze.grid[y][x] != 15:
                    v_grid[vy][vx] = self.Style.space

                    if not (self.maze.grid[y][x] & south):
                        v_grid[vy + 1][vx] = self.Style.space
                    if not (self.maze.grid[y][x] & east):
                        v_grid[vy][vx + 1] = self.Style.space
                else:
                    v_grid[vy][vx] =(self.Style.green +
                                     self.Style.block + self.Style.RESET)

        v_grid[1][1] = self.Style.entry + self.Style.block + self.Style.RESET
        v_grid[map_h - 2][map_w - 2] = (self.Style.red +
                                        self.Style.block + self.Style.RESET)
        # self.draw_pattern_42(v_grid, map_w, map_h)

        print(f"{self.Style.BOLD}A-Maze-ing 1337{self.Style.RESET}")
        for row in v_grid:
            print(self.Style.white + "".join(row) + self.Style.RESET)
