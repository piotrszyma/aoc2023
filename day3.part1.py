# Day 3

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Point:
    left_shift: int
    top_shift: int


@dataclass(frozen=True)
class EngineNumber:
    start: Point
    end: Point
    value: int

    def adjacent_points(self) -> Iterable[Point]:
        assert self.start.top_shift == self.end.top_shift, "EngineNumber must be on a vertical line"
        top_shift = self.start.top_shift

        yield Point(left_shift=self.start.left_shift - 1, top_shift=top_shift)
        yield Point(left_shift=self.end.left_shift + 1, top_shift=top_shift)

        for left_shift in range(self.start.left_shift - 1, self.end.left_shift + 2):
            yield Point(left_shift=left_shift, top_shift=top_shift-1)
            yield Point(left_shift=left_shift, top_shift=top_shift+1)


@dataclass(frozen=True)
class Symbol:
    position: Point
    value: str


def main():
    with open("day3.input.txt", "r") as f:
        engine_nums: list[EngineNumber] = []
        symbols: list[Symbol] = []

        symbol_pos_to_symbol_value: dict[Point, str] = {}

        for top_shift, line in enumerate(f):
            line = line.strip()
            if line == "":
                continue

            current_num = ""
            current_num_start: Point | None = None

            left_shift = 0

            for left_shift, char in enumerate(line + "."): # Add extra '.' so line never ends with number.
                if char.isdigit():
                    if current_num == "":  # Start of a number.
                        current_num = char
                        current_num_start = Point(left_shift, top_shift)
                    else:
                        current_num += char
                else: # Not a digit.
                    if current_num != "": # Clear number (if set).
                        assert current_num_start
                        engine_nums.append(
                            EngineNumber(
                                start=current_num_start,
                                end=Point(left_shift - 1, top_shift),
                                value=int(current_num),
                            )
                        )
                        current_num = ""
                        current_num_start = None

                    if char != ".":
                        symbol_pos = Point(left_shift, top_shift)
                        symbols.append(
                            Symbol(position=symbol_pos, value=char)
                        )

                        symbol_pos_to_symbol_value[symbol_pos] = char

        part_numbers: list[EngineNumber] = []
        for engine_num in engine_nums:
            for adj_point in engine_num.adjacent_points():
                if adj_point in symbol_pos_to_symbol_value:
                    part_numbers.append(engine_num)
                    break

        sum_of_part_nums = sum(p.value for p in part_numbers)
        print(sum_of_part_nums)



if __name__ == "__main__":
    main()
