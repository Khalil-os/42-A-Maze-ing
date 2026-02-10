import time
import os

# 1. Lwan (ANSI Codes)
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# 2. Maze Sghir (1 = Hayt, 0 = Triq)
# Hna sta3mlna Grid ssimple ghir l chra7
maze_map = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]


def draw():
    # Ms7 l-ecran
    os.system('clear')

    print("Mital d ASCII Rendering:\n")

    # Rsem star b star
    for row in maze_map:
        line = ""
        for cell in row:
            if cell == 1:
                # Rsem hayt hmer (#)
                line += RED + "# " + RESET
            else:
                # Rsem triq khdra (.)
                line += GREEN + ". " + RESET
        print(line)


print("Ghanbda rsm mn hna 3 d twayni...")
time.sleep(1)
draw()
print("\nChfti? Hada howa ASCII Rendering!")
