# Day 11
from dataclasses import dataclass
import pathlib
from typing import Iterable, TypeVar

_EMPTY_SHIFT = 1


@dataclass(frozen=True)
class Coord:
    col_idx: int
    row_idx: int

    def __hash__(self):
        return hash((self.col_idx, self.row_idx))

T = TypeVar('T')

def pairs(lst: Iterable[T]) -> Iterable[tuple[T, T]]:
    for e1 in lst:
        for e2 in lst:
            yield (e1, e2)

def main():
    data = pathlib.Path("day11_input_test.txt").read_text()

    rows = data.split("\n")

    rows_no = len(rows)
    cols_no = len(rows[0])

    empty_rows = set(row_no for row_no in range(rows_no))
    empty_cols = set(col_no for col_no in range(cols_no))
    galaxy_coords: set[Coord] = set()

    for row_idx, line in enumerate(data.split("\n")):
        for col_idx, c in enumerate(line):
            if c == "#":
                if row_idx in empty_rows:
                    empty_rows.remove(row_idx)

                if col_idx in empty_cols:
                    empty_cols.remove(col_idx)

                galaxy_coords.add(Coord(row_idx=row_idx, col_idx=col_idx))

    galaxy_coords_shifted: set[Coord] = set()
    for coord in galaxy_coords:
        empty_cols_on_left = set(
            col_idx for col_idx in empty_cols if col_idx < coord.col_idx
        )
        empty_rows_above = set(
            row_idx for row_idx in empty_rows if row_idx < coord.row_idx
        )

        galaxy_coords_shifted.add(
            Coord(
                row_idx=coord.row_idx + (len(empty_rows_above) * _EMPTY_SHIFT),
                col_idx=coord.col_idx + (len(empty_cols_on_left) * _EMPTY_SHIFT),
            )
        )

    distances_total: int = 0
    calculated_pairs: set[frozenset[Coord]] = set()

    for c1, c2 in pairs(galaxy_coords_shifted):
        if c1 == c2:
            continue

        if frozenset((c1, c2)) in calculated_pairs:
            continue

        calculated_pairs.add(frozenset((c1, c2)))

        distance = abs(c1.col_idx - c2.col_idx) + abs(c1.row_idx - c2.row_idx)
        distances_total += distance

    print(distances_total)


if __name__ == "__main__":
    main()
