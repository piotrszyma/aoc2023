# Day 10
from dataclasses import dataclass
import pathlib
import sys
from typing import Iterable, Literal

_START_SYMBOL_VALUE = "S"


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


_MAPPING: dict[str, tuple[str, str, str]] = {
    "|": (
        ".X.",
        ".X.",
        ".X.",
    ),
    "-": (
        "...",
        "XXX",
        "...",
    ),
    "L": (
        ".X.",
        ".XX",
        "...",
    ),
    "J": (
        ".X.",
        "XX.",
        "...",
    ),
    "7": (
        "...",
        "XX.",
        ".X.",
    ),
    "F": (
        "...",
        ".XX",
        ".X.",
    ),
    ".": (
        "...",
        "...",
        "...",
    ),
    "S": (
        ".X.",
        "XXX",
        ".X.",
    ),
}


@dataclass
class Position:
    top_shift: int
    left_shift: int

    def left(self) -> "Position":
        return Position(top_shift=self.top_shift, left_shift=self.left_shift - 1)

    def right(self) -> "Position":
        return Position(top_shift=self.top_shift, left_shift=self.left_shift + 1)

    def above(self) -> "Position":
        return Position(top_shift=self.top_shift - 1, left_shift=self.left_shift)

    def below(self) -> "Position":
        return Position(top_shift=self.top_shift + 1, left_shift=self.left_shift)

    def all_neighbours(self) -> Iterable["Position"]:
        for top_shift in range(self.top_shift - 1, self.top_shift + 1 + 1):
            for left_shift in range(self.left_shift - 1, self.left_shift + 1 + 1):
                yield Position(top_shift=top_shift, left_shift=left_shift)

    def __hash__(self):
        return hash((self.top_shift, self.left_shift))

    def __lt__(self, other: "Position"):
        return (self.top_shift, self.left_shift) < (other.top_shift, other.left_shift)


Direction = Literal["up", "right", "down", "left"]


@dataclass
class Symbol:
    value: str


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


@dataclass
class Pipe:
    symbol: str
    position: Position

    def __hash__(self):
        return hash((self.symbol, self.position))

    def is_start(self) -> bool:
        return self.symbol == _START_SYMBOL_VALUE

    def directions(self) -> set[Direction]:
        match self.symbol:
            case "|":
                return {"down", "up"}
            case "-":
                return {"left", "right"}
            case "L":
                return {"up", "right"}
            case "J":
                return {"up", "left"}
            case "7":
                return {"down", "left"}
            case "F":
                return {"down", "right"}
            case "S":
                return {"up", "down", "left", "right"}
            case ".":
                return set()

        raise ValueError(f"Cannot get directions for pipe symbol {self.symbol}")

    def possible_next(self, all_pipes: dict[Position, "Pipe"]) -> Iterable["Pipe"]:
        left_pipe = all_pipes.get(self.position.left())
        if (
            left_pipe  # there is pipe on left
            and "right"
            in left_pipe.directions()  # that pipe on left can join with this
            and "left" in self.directions()  # this pipe can join with pipe on left
        ):
            yield left_pipe

        right_pipe = all_pipes.get(self.position.right())
        if (
            right_pipe
            and "left" in right_pipe.directions()
            and "right" in self.directions()
        ):
            yield right_pipe

        above_pipe = all_pipes.get(self.position.above())
        if (
            above_pipe
            and "down" in above_pipe.directions()
            and "up" in self.directions()
        ):
            yield above_pipe

        below_pipe = all_pipes.get(self.position.below())
        if (
            below_pipe
            and "up" in below_pipe.directions()
            and "down" in self.directions()
        ):
            yield below_pipe


def main():
    data = pathlib.Path("day10_input.txt").read_text()

    rows_raw = data.split("\n")

    position_to_pipe = dict[Position, Pipe]()

    start_pipe: Pipe | None = None

    for top_shift, row_raw in enumerate(rows_raw):
        for left_shift, symbol in enumerate(row_raw):
            position = Position(left_shift=left_shift, top_shift=top_shift)
            pipe = Pipe(
                symbol=symbol,
                position=position,
            )

            if pipe.is_start():
                start_pipe = pipe

            position_to_pipe[position] = pipe

    assert start_pipe is not None, "start pipe not found"
    visited_pipes: set[Pipe] = {start_pipe}
    pipeline: list[Pipe] = [start_pipe]

    while True:
        current_pipe = pipeline[-1]

        next_pipes = current_pipe.possible_next(all_pipes=position_to_pipe)
        nonvisited_next_pipes = [
            pipe for pipe in next_pipes if pipe not in visited_pipes
        ]

        if len(nonvisited_next_pipes) == 0:
            break

        next_pipe_to_visit = nonvisited_next_pipes[0]
        pipeline.append(next_pipe_to_visit)
        visited_pipes.add(next_pipe_to_visit)


    # ==== PART 2 ====

    pipeline_positions: set[Position] = set(p.position for p in pipeline)

    pipeline_x3: list[list[str]] = []

    for top_shift, row_raw in enumerate(rows_raw):
        rows_x3 = [[], [], []]
        for left_shift, symbol in enumerate(row_raw):
            p = Position(left_shift=left_shift, top_shift=top_shift)
            if p not in pipeline_positions:
                mapped = _MAPPING['.'] # nothing here
            else:
                mapped = _MAPPING[symbol]

            for idx in range(3):
                rows_x3[idx].extend(mapped[idx])

        pipeline_x3.extend(rows_x3)

    to_visit = [Position(0, 0)]
    visited = set[Position]()

    while to_visit:
        el = to_visit.pop()
        if el in visited:
            continue
        try:
            val = pipeline_x3[el.top_shift][el.left_shift]
        except IndexError:
            continue

        if val == 'X':
            continue

        pipeline_x3[el.top_shift][el.left_shift] = 'X'

        for el in el.all_neighbours():
            to_visit.append(el)

    total_3x3_dots = 0
    # Window every 3x3.
    for top_shift in range(0, len(pipeline_x3), 3):
        for left_shift in range(0, len(pipeline_x3[0]), 3):
            # Check if every item in window is dot.
            dots_count = 0
            for top_idx in range(top_shift, top_shift + 3):
                for left_idx in range(left_shift, left_shift + 3):
                    if pipeline_x3[top_idx][left_idx] == '.':
                        dots_count += 1

            if dots_count == 9:
                total_3x3_dots += 1

    print(total_3x3_dots)


if __name__ == "__main__":
    main()
