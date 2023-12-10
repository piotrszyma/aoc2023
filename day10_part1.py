# Day 10
from dataclasses import dataclass
import pathlib

_START_SYMBOL = "S"


@dataclass
class Position:
    top_shift: int
    left_shift: int


@dataclass
class Pipe:
    symbol: str
    position: Position

    def is_start(self) -> bool:
        return self.symbol == _START_SYMBOL


def main():
    data = pathlib.Path("day10_input_test.txt").read_text()

    rows_raw = data.split("\n")

    rows: list[list[Pipe]] = []

    start_pipe: Pipe | None = None

    for top_shift, row_raw in enumerate(rows_raw):
        row: list[Pipe] = []
        for left_shift, p in enumerate(row_raw):
            pipe = Pipe(
                symbol=p,
                position=Position(left_shift=left_shift, top_shift=top_shift),
            )

            if pipe.is_start():
                start_pipe = pipe

            row.append(pipe)

        rows.append(row)

    assert start_pipe is not None, "start pipe not found"

    ...


if __name__ == "__main__":
    main()
