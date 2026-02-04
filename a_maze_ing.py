from mazegen.model import Maze


def main():
    maze = Maze(10, 4)
    maze.generate()
    maze.display_ascii()


if __name__ == "__main__":
    main()
