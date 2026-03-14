from typing import List, Dict, Tuple
import random
from collections import deque
import sys


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
    class MazeError(Exception):
        pass

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

    def is_in_pattern(self, x: int, y: int) -> bool:

        if self.grid[y][x] == 15:
            return True
        return False

    def prottect_pattern(self) -> None:
        if self.width < 10 or self.height < 6:
            raise self.MazeError("the size of the maze does not allow "
                                 "the 42 pattern to exist")
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

            for direction, dx, dy in [(north, 0, -1), (south, 0, 1),
                                      (east, 1, 0), (west, -1, 0)]:
                if not (cell_val & direction):
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.width and 0 <= ny < self.height and
                            (nx, ny) not in visited):
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

    def get_path_string(self) -> str:
        """Converts the coordinate path to string of N, E, S, W directions."""
        if not hasattr(self, 'ordered_path') or not self.ordered_path:
            return ""

        path_str = ""
        for i in range(len(self.ordered_path) - 1):
            cx, cy = self.ordered_path[i]
            nx, ny = self.ordered_path[i+1]

            if ny < cy:
                path_str += "N"
            elif ny > cy:
                path_str += "S"
            elif nx > cx:
                path_str += "E"
            elif nx < cx:
                path_str += "W"

        return path_str

    def export_to_file(self, filename: str, entry: Tuple[int, int],
                       exit_coord: tuple[int, int]) -> None:
        """Writes the maze and its solution to the specified output file."""
        path_str = self.get_path_string()

        try:
            with open(filename, 'w') as f:
                for row in self.grid:
                    line = "".join(f"{cell:X}" for cell in row)
                    f.write(line + "\n")

                f.write("\n")

                f.write(f"{entry[0]},{entry[1]}\n")
                f.write(f"{exit_coord[0]},{exit_coord[1]}\n")
                f.write(path_str + "\n")
        except IOError as e:
            print(f"Error writing to file {filename}: {e}")
