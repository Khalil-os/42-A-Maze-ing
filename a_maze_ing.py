from mazegen.model import Maze


def main():
    maze = Maze(10, 10)
    maze.generate()
    maze.solve()
    maze.display_ascii()
    maze.export_hex("output_maze.txt")


if __name__ == "__main__":
    main()
