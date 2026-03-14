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
    """Generates, solves, and exports a maze grid."""

    class MazeError(Exception):
        """Custom exception for maze generation errors."""
        pass

    def __init__(self, width: int, height: int, perfect: bool = True,
                 seed: int | None = None) -> None:
        """Initialize maze dimensions and internal structures."""
        self.width = width
        self.height = height
        self.perfect = perfect
        self.entree = (0, 0)
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.solution_cells: set[Tuple[int, int]] = set()
        self.ordered_path: List[Tuple[int, int]] = []
        self.pattern_omitted: bool = False
        self.pattern_42 = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2),
            (2, 3), (2, 4), (5, 0), (6, 0), (7, 0), (7, 1), (7, 2), (6, 2),
            (5, 2), (5, 3), (5, 4), (6, 4), (7, 4)
        ]
        if seed is not None:
            random.seed(seed)
        else:
            random.seed()

    def get_unvisited_neighbors(
                    self, x: int, y: int) -> List[Tuple[int, int, int]]:
        """Return all unvisited neighboring cells with directions."""
        neighbors: List[Tuple[int, int, int]] = []

        for direction in [north, south, east, west]:
            nx: int = x + Dx[direction]
            ny: int = y + Dy[direction]
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.visited[ny][nx]:
                    neighbors.append((direction, nx, ny))
        return neighbors

    def remove_walls(self, x: int, y: int, direction: int) -> None:
        """Remove wall between current cell and neighbor."""
        nx: int = x + Dx[direction]
        ny: int = y + Dy[direction]
        if 0 <= nx < self.width and 0 <= ny < self.height:
            self.grid[y][x] ^= direction
            self.grid[ny][nx] ^= Opposite[direction]

    def is_in_pattern(self, x: int, y: int) -> bool:
        """Check if a cell belongs to the protected pattern."""
        if self.grid[y][x] == 15:
            return True
        return False

    def prottect_pattern(self) -> None:
        """Reserve cells to preserve the '42' pattern in the maze."""
        if self.width < 10 or self.height < 6:
            self.pattern_omitted = True
            print("Error: The size of the maze does not "
                  "allow the 42 pattern to exist.", file=sys.stderr)
            return
        center_x = (self.width // 2) - 4
        center_y = (self.height // 2) - 2

        for dx, dy in self.pattern_42:
            x = center_x + dx
            y = center_y + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.visited[y][x] = True

    def generate(self, x: int, y: int) -> None:
        """Generate maze using recursive DFS."""
        self.visited[y][x] = True

        while True:
            neighors = self.get_unvisited_neighbors(x, y)

            if not neighors:
                return
            direction, nx, ny = random.choice(neighors)
            self.remove_walls(x, y, direction)
            self.generate(nx, ny)

    def add_cycles(self, density: float = 0.05) -> None:
        """Add extra openings to create cycles in the maze."""
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

    def solve(self, start: Tuple[int, int] | None = None,
              goal: Tuple[int, int] | None = None) -> List[Tuple[int, int]]:
        """Solve the maze using BFS and return the path."""
        st: Tuple[int, int] = start if start is not None else (0, 0)
        gl: Tuple[int, int] = (goal if goal is not None else
                               (self.width - 1, self.height - 1)
                               )

        if not (0 <= st[0] < self.width and 0 <= st[1] < self.height):
            return []
        if not (0 <= gl[0] < self.width and 0 <= gl[1] < self.height):
            return []

        queue: deque[Tuple[int, int]] = deque([st])
        visited: set[Tuple[int, int]] = {st}
        parent: Dict[Tuple[int, int], Tuple[int, int] | None] = {st: None}

        while queue:
            curr = queue.popleft()
            if curr == gl:
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

        path: List[Tuple[int, int]] = []
        curr_node: Tuple[int, int] | None = gl
        if gl in parent:
            while curr_node is not None:
                path.append(curr_node)
                curr_node = parent[curr_node]
            path.reverse()
        else:
            return []

        self.ordered_path = path
        self.solution_cells = set(path)
        return path

    def run(self, start_x: int, start_y: int) -> None:
        """Generate the maze and optionally add cycles."""
        self.prottect_pattern()
        self.generate(start_x, start_y)
        if not self.perfect:
            self.add_cycles()

    def get_path_string(self) -> str:
        """Convert solution path to N/E/S/W direction string."""
        if not self.ordered_path:
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
        """Export maze grid and solution path to a file."""
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
