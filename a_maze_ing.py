import sys
from mazegen.parsing import Parsing
from mazegen1 import MazeGenerator, MazeVisualizer


def main():
    if (len(sys.argv) != 2):
        print("error: you should give one configuration file")
        sys.exit(1)
    try:
        with open(sys.argv[1], "r") as file:
            content: str = file.read()
            parser = Parsing(content)
            config = parser.parse()
            if config["PERFECT"] == "False":
                config["PERFECT"] = False
            maze = MazeVisualizer(config["WIDTH"], config["HEIGHT"],
                                  config["ENTRY"], config["EXIT"],
                                  config["PERFECT"])
            maze.loop()

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
