# Day 10
from dataclasses import dataclass
import pathlib
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
        ".|.",
        ".|.",
        ".|.",
    ),
    "-": (
        "...",
        "---",
        "...",
    ),
    "L": (
        ".|.",
        ".L-",
        "...",
    ),
    "J": (
        ".|.",
        "-J.",
        "...",
    ),
    "7": (
        "...",
        "-7.",
        ".|.",
    ),
    "F": (
        "...",
        ".F-",
        ".|.",
    ),
    ".": (
        "...",
        "...",
        "...",
    ),
    "S": (
        ".|.",
        "-S-",
        ".|.",
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
    data = pathlib.Path("day10_input_test2.txt").read_text()

    rows_raw = data.split("\n")
    rows_raw_mapped = []
    for row in rows_raw:
        row_mapped = []
        for c in row:
            row_mapped.append(_MAPPING[c])

        rows_raw_mapped.append(row_mapped)

    rows_raw_mapped = [_MAPPING[c] for row in rows_raw for c in row]

    rows_raw_mapped = []
    for row_raw_mapped in rows_raw_mapped:
        for idx in range(3):
            rows_raw_mapped.append(''.join(r[idx] for r in row_raw_mapped))

    position_to_pipe = dict[Position, Pipe]()

    start_pipe: Pipe | None = None

    for top_shift, row_raw in enumerate(rows_raw_mapped):
        for left_shift, p in enumerate(row_raw):
            position = Position(left_shift=left_shift, top_shift=top_shift)
            pipe = Pipe(
                symbol=p,
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

    # Find bounding box covering all pipe elements.
    left_top_min_pos = Position(top_shift=0, left_shift=0)
    right_bottom_max_pos = Position(
        top_shift=max(p.position.top_shift for p in visited_pipes),
        left_shift=max(p.position.left_shift for p in visited_pipes),
    )

    # Get all positions on bounding box that are not pipeline.
    positions_to_check: set[Position] = {
        *[
            Position(top_shift=0, left_shift=left_shift)
            for left_shift in range(right_bottom_max_pos.left_shift + 1)
        ],
        *[
            Position(top_shift=right_bottom_max_pos.top_shift, left_shift=left_shift)
            for left_shift in range(right_bottom_max_pos.left_shift + 1)
        ],
        *[
            Position(top_shift=top_shift, left_shift=0)
            for top_shift in range(right_bottom_max_pos.top_shift + 1)
        ],
        *[
            Position(top_shift=top_shift, left_shift=right_bottom_max_pos.left_shift)
            for top_shift in range(right_bottom_max_pos.top_shift + 1)
        ],
    }

    positions_to_check_list = list(positions_to_check)
    positions_outside = set[Position]()

    visited_pipe_pos = {p.position for p in visited_pipes}

    def is_pipe(pos: Position) -> bool:
        return pos in visited_pipe_pos

    def is_outside_bounding_box(pos: Position) -> bool:
        return (
            pos.left_shift < 0
            or pos.top_shift < 0
            or pos.left_shift > right_bottom_max_pos.left_shift
            or pos.top_shift > right_bottom_max_pos.top_shift
        )

    while positions_to_check_list:
        position = positions_to_check_list.pop()
        if is_pipe(position):
            continue

        if is_outside_bounding_box(position):
            continue

        positions_to_check_list.append(*position.all_neighbours())

        positions_outside.add(position)

    # TODO(pszyma): calc all 3x3 dots only
    ...


if __name__ == "__main__":
    main()
