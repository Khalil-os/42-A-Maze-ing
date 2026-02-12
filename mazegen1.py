from typing import List, Dict, Tuple
import random
import sys
import os
from collections import deque
import time

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
        self.solution_cells = set()
        self.pattern_42 = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2),
            (2, 3), (2, 4), (5, 0), (6, 0), (7, 0), (7, 1), (7, 2), (6, 2),
            (5, 2), (5, 3), (5, 4), (6, 4), (7, 4)
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
        if 0 <= nx < self.width and 0 <= ny < self.height:
            self.grid[y][x] ^= direction
            self.grid[ny][nx] ^= Opposite[direction]

    def prottect_pattern(self) -> None:
        if self.width < 10 or self.height < 6:
            return
        center_x = (self.width // 2) - 4
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

    def add_cycles(self, density: float = 0.05) -> None:

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 15:
                    continue
                directions = [north, south, east, west]
                random.shuffle(directions)
                for direction in directions:
                    nx, ny = x + Dx[direction], y + Dy[direction]
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.grid[ny][nx] == 15:
                            continue
                        if self.grid[y][x] & direction:
                            if random.random() < density:
                                self.remove_walls(x, y, direction)
                                break

    def solve(self, start: Tuple[int, int] = None,
              goal: Tuple[int, int] = None) -> List[Tuple[int, int]]:

        if start is None:
            start = (0, 0)
        if goal is None:
            goal = (self.width - 1, self.height - 1)

        start = tuple(start)
        goal = tuple(goal)

        if not (0 <= start[0] < self.width and 0 <= start[1] < self.height):
            return []
        if not (0 <= goal[0] < self.width and 0 <= goal[1] < self.height):
            return []

        # 2. Bda l-BFS
        queue = deque([start])
        visited = {start}
        parent = {start: None}

        while queue:
            curr = queue.popleft()
            if curr == goal:
                break

            x, y = curr
            cell_val = self.grid[y][x]

            if cell_val == 15:
                continue

            for direction, dx, dy in [(north, 0, -1), (south, 0, 1), (east, 1, 0), (west, -1, 0)]:
                if not (cell_val & direction):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = curr
                        queue.append((nx, ny))

        path = []
        curr = goal
        if goal in parent:
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
        else:
            return []

        self.ordered_path = path
        self.solution_cells = set(path)
        return path

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

    def __init__(self, width: int, height: int, entry,
                 exite, perfect: bool = True) -> None:

        self.width = width
        self.height = height
        self.perfect = perfect
        self.maze = MazeGenerator(width, height, perfect)
        self.maze.run(0, 0)
        self.show_path = False
        self.entry = entry if entry else (0, 0)
        self.exite = exite if exite else (width - 1, height - 1)

    def render(self) -> None:
        print("\033[H", end="")
        map_h: int = self.height * 2 + 1
        map_w: int = self.width * 2 + 1
        v_grid = [[self.Style.block for _ in range(map_w)] for _ in range(map_h)]
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
                                         ((x, y+1) in self.maze.solution_cells))

                    if is_path and neighboor_in_path:
                        v_grid[vy + 1][vx] = (self.Style.green +
                                              self.Style.block +
                                              self.Style.RESET)
                    else:
                        v_grid[vy + 1][vx] = self.Style.space

                if not (self.maze.grid[y][x] & east):
                    neighboor_in_path = (should_draw_path and
                                         ((x+1, y) in self.maze.solution_cells))
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
            v_grid[goal[1]][goal[0]] = (self.Style.red +
                                        self.Style.block + self.Style.RESET)
        os.system("clear")
        print(f"{self.Style.BOLD}A-Maze-ing 1337{self.Style.RESET}")
        for row in v_grid:
            print(self.Style.white + "".join(row) + self.Style.RESET)

    def play_animation(self):

        path_list = self.maze.solve(self.entry, self.exite)
        if not path_list:
            return
        self.maze.solution_cells = set()
        os.system("clear")
        for cell in path_list:
            self.maze.solution_cells.add(cell)
            self.render()
            time.sleep(0.05)

    def loop(self):
        os.system("clear")
        while True:
            self.render()
            print("enter 'r' to recreate")
            print("enter 's' to solve maze")
            print("enter 'q' to quit")
            try:
                choice = input("Choice: ").strip().lower()
                if choice == 'q':
                    break
                elif choice == 'r':
                    self.maze = MazeGenerator(self.width,
                                              self.height, self.perfect)
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
            except (EOFError, KeyboardInterrupt):
                break
