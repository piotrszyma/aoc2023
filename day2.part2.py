# Day 2

import re


RE_COLOR_COUNTS = re.compile(r"(?P<count>\d+) (?P<color>\w+)")


def main():
    with open("day2.input.txt", "r") as f:
        powers_sum = 0

        for line in f:
            if not line.strip():
                continue

            _, line_subsets = line.strip().split(": ")

            subsets = line_subsets.split("; ")

            min_blue = 0
            min_red = 0
            min_green = 0

            for subset_raw in subsets:
                for match in RE_COLOR_COUNTS.finditer(subset_raw):
                    count = int(match.group("count"))
                    color_raw = match.group("color")
                    match color_raw:
                        case "red":
                            min_red = max(count, min_red)
                        case "blue":
                            min_blue = max(count, min_blue)
                        case "green":
                            min_green = max(count, min_green)

            power = min_red * min_green * min_blue

            powers_sum += power

        print(f"{powers_sum=}")


if __name__ == "__main__":
    main()
