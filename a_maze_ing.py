import sys


def main():
    if (len(sys.argv) != 2):
        print("error: you should give one configuration file")
        sys.exit(1)
    try:
        with open(sys.argv[1], "r") as file:
            content: str = file.read()
            print(content)

    except FileNotFoundError:
        print("Error: file not found")


if __name__ == "__main__":
    main()
