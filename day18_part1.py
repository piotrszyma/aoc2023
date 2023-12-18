# Day 18
from dataclasses import dataclass
import pathlib
from typing import Iterable, Literal

Dir = Literal["U", "D", "L", "R"]


def dir_from_str(dir: str) -> Dir:
    match dir:
        case "U" | "D" | "L" | "R":
            return dir
        case _:
            raise ValueError(f"Unexpected {dir=}")



@dataclass(frozen=True)
class Pos:
    left_shift: int
    top_shift: int

    def around(self) -> set['Pos']:
        return set((
            Pos(left_shift=self.left_shift-1, top_shift=self.top_shift),
            Pos(left_shift=self.left_shift+1, top_shift=self.top_shift),
            Pos(left_shift=self.left_shift, top_shift=self.top_shift+1),
            Pos(left_shift=self.left_shift, top_shift=self.top_shift-1),
        ))

    def __lt__(self, other: 'Pos') -> bool:
        if self.left_shift == other.left_shift:
            return self.top_shift < other.top_shift
        return self.left_shift < other.left_shift

    def shift(self, dir: Dir) -> "Pos":
        match dir:
            case "U":
                return Pos(left_shift=self.left_shift, top_shift=self.top_shift - 1)
            case "D":
                return Pos(left_shift=self.left_shift, top_shift=self.top_shift + 1)
            case "L":
                return Pos(left_shift=self.left_shift - 1, top_shift=self.top_shift)
            case "R":
                return Pos(left_shift=self.left_shift + 1, top_shift=self.top_shift)
            case _:
                raise ValueError(f"Unexpected dir {dir=}")

def pos_range(start: Pos, end: Pos) -> Iterable[Pos]:
    min_left_shift = min(start.left_shift, end.left_shift)
    max_left_shift = max(start.left_shift, end.left_shift)

    min_top_shift = min(start.top_shift, end.top_shift)
    max_top_shift = max(start.top_shift, end.top_shift)

    for left_shift in range(min_left_shift, max_left_shift + 1):
        for top_shift in range(min_top_shift, max_top_shift + 1):
            yield Pos(left_shift=left_shift, top_shift=top_shift)

@dataclass(frozen=True)
class Instruction:
    direction: Dir
    length: int
    color: str

    @staticmethod
    def from_string(v: str) -> "Instruction":
        try:
            raw_dir, raw_length, color = v.split(" ")
        except ValueError as error:
            print(v)
            raise
        return Instruction(
            direction=dir_from_str(raw_dir), length=int(raw_length), color=color
        )


def main():
    data = pathlib.Path("day18_input.txt").read_text()
    lines = data.split("\n")
    instr: list[Instruction] = []
    for line in lines:
        instr.append(Instruction.from_string(line))

    pos = Pos(0, 0)
    holes: set[Pos] = set()
    for i in instr:
        for _ in range(i.length):
            pos = pos.shift(i.direction)
            holes.add(pos)

    top_shift_min = min(h.top_shift for h in holes) - 1
    top_shift_max = max(h.top_shift for h in holes) + 1

    left_shift_min = min(h.left_shift for h in holes) - 1
    left_shift_max = max(h.left_shift for h in holes) + 1

    top_left_pos = Pos(left_shift=left_shift_min, top_shift=top_shift_min)
    bottom_right_pos =Pos(left_shift=left_shift_max, top_shift=top_shift_max)

    to_visit: list[Pos] = [top_left_pos]
    visited: set[Pos] = set()

    while to_visit:
        pos = to_visit.pop()

        if pos in visited:
            continue

        if pos.top_shift < top_shift_min or pos.top_shift > top_shift_max or pos.left_shift < left_shift_min or pos.left_shift > left_shift_max:
            continue

        if pos in holes:
            continue

        visited.add(pos)
        to_visit.extend(pos.around())

    size = 0
    for top_shift in range(top_left_pos.top_shift, bottom_right_pos.top_shift + 1):
        for left_shift in range(top_left_pos.left_shift, bottom_right_pos.left_shift + 1):
            pos = Pos(top_shift=top_shift, left_shift=left_shift)
            if pos in holes:
                size += 1
            elif pos in visited:
                ...
                # print(' ', end='')
            else:
                size += 1
                # print('.',end='')

        # print()

    print(size)




if __name__ == "__main__":
    main()
