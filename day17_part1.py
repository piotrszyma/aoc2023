# Day 17
from dataclasses import dataclass
import functools
import pathlib
from typing import Literal

# constraints
# - at most three blocks in one direction
# - turn left / right
# - no reverse direction

# START: top left
# FINISH: bottom right


@dataclass(frozen=True)
class Pos:
    top_shift: int
    left_shift: int

    def __lt__(self, other: "Pos") -> bool:
        return self.top_shift < other.top_shift and self.left_shift < other.left_shift

    def shifted_top(self, shift: int) -> "Pos":
        return Pos(top_shift=self.top_shift + shift, left_shift=self.left_shift)

    def shifted_left(self, shift: int) -> "Pos":
        return Pos(top_shift=self.top_shift, left_shift=self.left_shift + shift)


Dir = Literal[">", "^", "<", "v"]


class Context:
    def __init__(self, heat_loss_map: dict[Pos, int]):
        self.heat_loss_map = heat_loss_map
        self.start_end_cache: dict[tuple[Pos, Pos], int] = {}
        self.visited = set[Pos]()

    def next_point(self, p: Pos, dir: Dir) -> Pos | None:
        if dir == ">":
            next_point = p.shifted_left(1)
        elif dir == "<":
            next_point = p.shifted_left(-1)
        elif dir == "^":
            next_point = p.shifted_top(1)
        elif dir == "v":
            next_point = p.shifted_top(-1)
        else:
            raise ValueError(f"Unexpected direction {dir}")

        if next_point not in self.heat_loss_map:
            return None

        return next_point

    def min_total_heat_loss(
        self,
        start: Pos,
        end: Pos,
        current_dir: Dir | None = None,  # None for start
        current_dir_repeats=0,
        visited: set[Pos] = set(),
    ) -> int:
        print(start, end)
        cached_min = self.start_end_cache.get((start, end))
        if cached_min is not None:
            return cached_min

        next_dirs: list[Dir]
        if current_dir == ">" or current_dir == "<":
            next_dirs = ["^", "v"]
        elif current_dir == "v" or current_dir == "^":
            next_dirs = ["<", ">"]
        elif current_dir is None:
            next_dirs = [">", "v"]
        else:
            raise ValueError("Unexpected current dir")

        if current_dir_repeats < 3 and current_dir is not None:
            next_dirs.append(
                current_dir
            )  # if did not move 3 times current dir, allow move

        opts: list[int] = []
        for next_dir in next_dirs:
            new_start = self.next_point(start, next_dir)
            if new_start is None:
                continue

            if new_start in visited:
                continue

            new_curr_dir_repeats = (
                current_dir_repeats + 1 if next_dir == current_dir else 1
            )

            opts.append(
                self.heat_loss_map[start]
                + self.min_total_heat_loss(
                    new_start,
                    end,
                    current_dir=next_dir,
                    current_dir_repeats=new_curr_dir_repeats,
                    visited={*visited, start}
                )
            )

        result = min(opts)
        self.start_end_cache[(start, end)] = result
        return result
        # if source_dir is None: # Start.
        #     return min(
        #         self.heat_loss_map[] + self.min_total_heat_loss()
        #     )


def main():
    data = pathlib.Path("day17_input_test.txt").read_text()

    lines = data.split("\n")

    heat_loss_map: dict[Pos, int] = {}

    bottom_right_pos = Pos(top_shift=len(lines), left_shift=len(lines[0]))

    for top_shift, line in enumerate(lines):
        for left_shift, heat_loss in enumerate(line):
            heat_loss_map[Pos(top_shift, left_shift)] = int(heat_loss)

    least_hit_loss = Context(heat_loss_map).min_total_heat_loss(
        Pos(0, 0),
        bottom_right_pos,
    )

    print(least_hit_loss)


if __name__ == "__main__":
    main()
