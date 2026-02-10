from typing import Tuple, List
import random
from collections import deque

north = 1  # 0001
east = 2   # 0010
south = 4  # 0100
west = 8   # 1000


class Cell:
    def __init__(self) -> None:
        self.walls: int = north | east | south | west
        self. visited: bool = False

    def has_wall(self, wall: int) -> bool:
        return bool(wall & self.walls)

    def open_wall(self, wall: int) -> None:
        self.walls &= ~wall

    def close_wall(self, wall: int) -> None:
        self.walls |= wall


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.entry = (0, 0)
        self.exit = (self.width - 1, self.height - 1)
        self.solution_cells = set()
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def in_bounds(self, x: int, y: int) -> bool:
        if x >= 0 and x < self.width:
            if y >= 0 and y < self.height:
                return True
        return False

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int, int]]:
        l: list = []
        if self.in_bounds(x+1, y):
            l.append((east, x+1, y))
        if self.in_bounds(x-1, y):
            l.append((west, x-1, y))
        if self.in_bounds(x, y+1):
            l.append((south, x, y+1))
        if self.in_bounds(x, y-1):
            l.append((north, x, y-1))
        return l

    def open_passage(self, x: int, y: int, direction: int) -> None:
        if direction == north:
            if self.in_bounds(x, y-1):
                self.grid[y-1][x].open_wall(south)
                self.grid[y][x].open_wall(north)
        elif direction == south:
            if self.in_bounds(x, y+1):
                self.grid[y+1][x].open_wall(north)
                self.grid[y][x].open_wall(south)
        elif direction == west:
            if self.in_bounds(x-1, y):
                self.grid[y][x-1].open_wall(east)
                self.grid[y][x].open_wall(west)
        else:
            if self.in_bounds(x+1, y):
                self.grid[y][x+1].open_wall(west)
                self.grid[y][x].open_wall(east)

    def generate(self) -> None:
        self._dfs(0, 0)

    def _dfs(self, x: int, y: int) -> None:
        current = self.get_cell(x, y)
        current.visited = True
        neighbors = self.get_neighbors(x, y)
        random.shuffle(neighbors)
        for direction, nx, ny in neighbors:
            neighbor_cell = self.get_cell(nx, ny)
            if not neighbor_cell.visited:
                self.open_passage(x, y, direction)
                self._dfs(nx, ny)

    def display_ascii(self) -> None:
        for x in range(self.width):
            cell = self.grid[0][x]
            print("+---" if cell.has_wall(north) else "+   ", end="")
        print("+")
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                print("|" if cell.has_wall(west) else " ", end="")
                if (x, y) == self.entry:
                    print(" E ", end="")
                elif (x, y) == self.exit:
                    print(" X ", end="")
                elif hasattr(self, "solution_cells") and (x, y) in self.solution_cells:
                    print(" . ", end="")
                else:
                    print("   ", end="")
            last_cell = self.grid[y][self.width - 1]
            print("|" if last_cell.has_wall(east) else " ")
            for x in range(self.width):
                cell = self.grid[y][x]
                print("+---" if cell.has_wall(south) else "+   ", end="")
            print("+")

    def solve(self):
        start = self.entry
        goal = self.exit
        queue = deque()
        queue.append(start)
        visited = set()
        visited.add(start)
        parent = {}
        parent[start] = None

        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            cell = self.get_cell(x, y)
            for direction, nx, ny in self.get_neighbors(x, y):
                if direction == north and cell.has_wall(north):
                    continue
                if direction == south and cell.has_wall(south):
                    continue
                if direction == east and cell.has_wall(east):
                    continue
                if direction == west and cell.has_wall(west):
                    continue
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        if goal not in parent:
            return None

        path = []
        cur = goal
        while cur != start:
            prev = parent[cur]
            px, py = prev
            cx, cy = cur
            if cx == px and cy == py - 1:
                path.append(north)
            elif cx == px and cy == py + 1:
                path.append(south)
            elif cx == px + 1 and cy == py:
                path.append(east)
            elif cx == px - 1 and cy == py:
                path.append(west)
            cur = prev

        path.reverse()
        solution_cells = []
        x, y = start
        solution_cells.append((x, y))
        for move in path:
            if move == north:
                y -= 1
            elif move == south:
                y += 1
            elif move == east:
                x += 1
            elif move == west:
                x -= 1
            solution_cells.append((x, y))
        self.solution_cells = set(solution_cells)
        return path

    def export_hex(self, filename: str) -> None:
        with open(filename, "w") as f:
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    cell = self.grid[y][x]
                    row.append(format(cell.walls, "x"))
                f.write(" ".join(row) + "\n")
