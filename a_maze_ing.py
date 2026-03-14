import sys
from mazegen.parsing import Parsing
from mazegen.generator import MazeGenerator
from mazegen.visualiser import MazeVisualizer


def main():
    if (len(sys.argv) != 2):
        print("error: you should give one configuration file")
        sys.exit(1)
    try:
        with open(sys.argv[1], "r") as file:
            content: str = file.read()
            parser = Parsing(content)
            config = parser.parse()
            if "OUTPUT_FILE" not in config:
                raise parser.ConfigSyntaxError("OUTPUT_FILE is missing"
                                               "from configuration")

            if config["PERFECT"].lower() == "false":
                config["PERFECT"] = False
            if config['ENTRY'] == config["EXIT"]:
                raise parser.ConfigSyntaxError("entry = exit")
            maze_vis = MazeVisualizer(config["WIDTH"], config["HEIGHT"],
                                      config["ENTRY"], config["EXIT"],
                                      config.get("PERFECT", True))

            maze_vis.maze.solve(config["ENTRY"], config["EXIT"])

            maze_vis.loop(config)

            print("\nMaze Généré!")
    except FileNotFoundError:
        print(f"Error: file not found {sys.argv[1]}")
        sys.exit(1)
    except Parsing.ConfigSyntaxError as e:
        print(f"Configuration Syntax Error: '{e}'")
        sys.exit(1)
    except MazeGenerator.MazeError as e:
        print("Error:", e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
