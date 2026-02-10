import sys
from mazegen.parsing import Parsing
from mazegen1 import MazeGenerator, MazeVisualizer
# try:
#     import mlx
# except ImportError:
#     print("Warning: MLX library ma kaynach. Ghadi nkhdm bla visual.")
#     mlx = None


def main():
    if (len(sys.argv) != 2):
        print("error: you should give one configuration file")
        sys.exit(1)
    try:
        with open(sys.argv[1], "r") as file:
            content: str = file.read()
            parser = Parsing(content)
            config = parser.parse()
            maze = MazeVisualizer(config["WIDTH"], config["HEIGHT"], config["PERFECT"])
            maze.render()
            # generator = MazeGenerator(config["WIDTH"], config["HEIGHT"], False)
            # start_x, start_y = config["ENTRY"]
            # generator.run(start_x, start_y)
            # generator.print_maze()
            # maze = Maze(10, 4)
            # maze.generate()
            # maze.display_ascii()

            print("\nMaze Généré!")
    except FileNotFoundError:
        print(f"Error: file not found {sys.argv[1]}")
        sys.exit(1)
    except Parsing.ConfigSyntaxError as e:
        print(f"Configuration Syntax Error: '{e}'")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
