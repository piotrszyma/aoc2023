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

UNREACHABLE = Literal['UNREACHABLE']


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

@dataclass(frozen=True)
class PosWithDir:
    pos: Pos
    dir: Dir


class Context:
    def __init__(self, heat_loss_map: dict[Pos, int]):
        self.heat_loss_map = heat_loss_map
        self.start_end_cache: dict[tuple[Pos, Pos], tuple[int | UNREACHABLE, set[Pos], list[PosWithDir]], ] = {}
        self.visited = set[Pos]()

    def next_point(self, p: Pos, dir: Dir) -> Pos | None:
        if dir == ">":
            next_point = p.shifted_left(1)
        elif dir == "<":
            next_point = p.shifted_left(-1)
        elif dir == "^":
            next_point = p.shifted_top(-1)
        elif dir == "v":
            next_point = p.shifted_top(1)
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
        pos_with_dir: list[PosWithDir] = [],
    ) -> tuple[int | UNREACHABLE, set[Pos], list[PosWithDir]]:
        if start == end:
            assert current_dir
            return self.heat_loss_map[end], {start, *visited}, [PosWithDir(pos=end, dir=current_dir), *pos_with_dir]

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

        if current_dir is not None and current_dir_repeats < 3:
            # if did not move 3 times current dir, allow move in current dir
            next_dirs.append(current_dir)

        min_res: int | UNREACHABLE = 'UNREACHABLE'
        min_visited: set[Pos] = set()
        min_pos_with_dir = []
        for next_dir in next_dirs:
            new_start = self.next_point(start, next_dir)
            if new_start is None:
                continue

            if new_start in visited:
                continue

            if new_start == start:
                continue

            new_curr_dir_repeats = (
                current_dir_repeats + 1 if next_dir == current_dir else 1
            )

            path_suffix_min_total_heat_loss, prev_visited, prev_min_pos_with_dir = self.min_total_heat_loss(
                new_start,
                end,
                current_dir=next_dir,
                current_dir_repeats=new_curr_dir_repeats,
                visited={*visited, start},
                pos_with_dir=[*pos_with_dir, PosWithDir(pos=new_start, dir=next_dir)]
            )

            if path_suffix_min_total_heat_loss == 'UNREACHABLE':
                continue

            entered_from_other = current_dir is not None # Do not add heat loss for first.

            res = (self.heat_loss_map[start] if entered_from_other else 0) + path_suffix_min_total_heat_loss

            if min_res == 'UNREACHABLE' or res < min_res:
                min_res = res
                min_visited = prev_visited
                min_pos_with_dir = prev_min_pos_with_dir

        result = min_res
        self.start_end_cache[(start, end)] = (result, min_visited, min_pos_with_dir)
        return result, min_visited, min_pos_with_dir


def least_hit_loss_for_input(data: str) -> int:
    lines = data.split("\n")

    heat_loss_map: dict[Pos, int] = {}

    bottom_right_pos = Pos(top_shift=len(lines) - 1, left_shift=len(lines[0]) - 1)

    for top_shift, line in enumerate(lines):
        for left_shift, heat_loss in enumerate(line):
            heat_loss_map[Pos(top_shift, left_shift)] = int(heat_loss)

    least_hit_loss, visited, pos_with_dir = Context(heat_loss_map).min_total_heat_loss(
        Pos(0, 0),
        bottom_right_pos,
    )

    pos_to_dir = {p.pos: p.dir for p in pos_with_dir}

    # Debug print start
    for top_shift, line in enumerate(lines):
        for left_shift, heat_loss in enumerate(line):
            p = Pos(top_shift, left_shift)
            if p in visited:
                dir = pos_to_dir.get(p)
                print(dir or '?', end='')
            else:
                print('.', end='')
        print()
    # Debug print end

    if least_hit_loss == "UNREACHABLE":
        raise ValueError("Bottom right is unreachable from top left")

    return least_hit_loss


def main():
    data = pathlib.Path("day17_input_test.txt").read_text()

    print(least_hit_loss_for_input(data))


if __name__ == "__main__":
    main()
