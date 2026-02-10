from typing import List, Dict, Any


class Parsing:

    class ConfigSyntaxError(Exception):
        pass

    def __init__(self, content: str) -> None:
        self.content = content
        self.config: Dict[str, Any] = {}

    def spliting_file(self) -> List[str]:
        l: List[str] = self.content.split('\n')
        clean_lines: list[str] = []
        for line in l:
            stripped_line = line.strip()

            if not stripped_line or stripped_line.startswith('#'):
                continue
            clean_lines.append(stripped_line)
        return (clean_lines)

    def parse_lines(self, file: List[str]) -> None:
        for config in file:
            parts: List[str] = config.split('=')
            if (len(parts) != 2):
                raise Parsing.ConfigSyntaxError(
                    "Configuration's syntax is incorrect")
            key: str = parts[0].strip()
            raw_value: str = parts[1].strip()
            try:
                if (key == "WIDTH" or key == "HEIGHT"):
                    val = int(raw_value)
                    if (val <= 0):
                        raise ValueError("give a positive number")
                    self.config[key] = val

                elif (key == "ENTRY" or key == "EXIT"):
                    coords = raw_value.split(',')
                    if (len(coords) != 2):
                        raise ValueError("you need x,y")
                    x = int(coords[0].strip())
                    y = int(coords[1].strip())
                    self.config[key] = (x, y)
                else:
                    self.config[key] = raw_value
            except ValueError as e:
                raise Parsing.ConfigSyntaxError(
                    f"error in value of {key}: {e}")

    def parse(self) -> Dict[str, Any]:
        lines = self.spliting_file()
        self.parse_lines(lines)
        return (self.config)


def main():
    pass


if __name__ == "__main__":
    main()
