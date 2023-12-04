# Day 2

from dataclasses import dataclass
import re


RE_COLOR_COUNTS = re.compile(r"(?P<count>\d+) (?P<color>\w+)")
RE_GAME_ID = re.compile(r"Game (?P<game_id>\d+)")


@dataclass
class Subset:
    red: int = 0
    green: int = 0
    blue: int = 0


def main():
    with open("day2.input.txt", "r") as f:
        game_idx_sum = 0

        for line in f:
            if not line.strip():
                continue

            game, line_subsets = line.strip().split(": ")
            _, game_idx = game.split(" ")

            subsets = line_subsets.split("; ")

            is_possible = True

            for subset_raw in subsets:
                subset = Subset()

                for match in RE_COLOR_COUNTS.finditer(subset_raw):
                    count = int(match.group("count"))
                    color_raw = match.group("color")
                    match color_raw:
                        case "red":
                            subset.red = count
                        case "blue":
                            subset.blue = count
                        case "green":
                            subset.green = count

                # There are only 12 red cubes, 13 green cubes, and 14 blue cubes.
                if subset.red > 12 or subset.green > 13 or subset.blue > 14:
                    is_possible = False
                    break

            if is_possible:
                game_idx_sum += int(game_idx)

        print(f"{game_idx_sum=}")


if __name__ == "__main__":
    main()
