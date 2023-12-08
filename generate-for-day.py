import argparse
import pathlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    args = parser.parse_args()
    day: int = args.day

    template = f"""# Day {day}
import pathlib

def main():
    data = pathlib.Path("day{day}_input_test.txt").read_text()

if __name__ == "__main__":
    main()
"""

    py_day1 = pathlib.Path(f"day{day}_part1.py")
    py_day1.write_text(template)

    py_day2 = pathlib.Path(f"day{day}_part2.py")
    py_day2.write_text(template)

    txt_input_test = pathlib.Path(f"day{day}_input_test.txt")
    txt_input_test.touch()

    txt_input = pathlib.Path(f"day{day}_input.txt")
    txt_input.touch()


if __name__ == "__main__":
    main()
