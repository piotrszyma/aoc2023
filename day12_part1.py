# Day 12
import functools
import pathlib
from dataclasses import dataclass
import re
from typing import Callable, Iterable, Iterator
from time import perf_counter
from contextlib import contextmanager


@contextmanager
def measure_exec_time():
    start = perf_counter()
    yield lambda: perf_counter() - start
    print(f"Time: {perf_counter() - start:.3f} seconds")


@dataclass
class Record:
    value: str
    groups: tuple[int, ...]

    @staticmethod
    def from_line(l: str, multiplier=1) -> "Record":
        value_raw, groups_raw = l.split(" ")
        groups = tuple(map(int, groups_raw.split(","))) * multiplier
        value = "?".join(value_raw for _ in range(multiplier))
        return Record(value=value, groups=groups)


@functools.lru_cache()
def arrangements_count(
    values: str, group_sizes: tuple[int, ...], previous_was_hash=False
) -> int:
    if values == "":
        no_more_group_sizes = len(group_sizes) == 0

        # TODO: there must be more elegant way to handle this case
        one_group_size_of_size_zero = len(group_sizes) == 1 and group_sizes[0] == 0

        if no_more_group_sizes or one_group_size_of_size_zero:
            return 1
        else:
            return 0

    if values[0] == ".":
        if previous_was_hash:  # end of group
            if len(group_sizes) == 0:  # no more groups expected
                return 0
            elif group_sizes[0] == 0:  #
                return arrangements_count(
                    values[1:], group_sizes[1:], previous_was_hash=False
                )
            else:
                return 0
        else:
            return arrangements_count(values[1:], group_sizes, previous_was_hash=False)
    elif values[0] == "#":
        if len(group_sizes) == 0:
            return 0
        elif group_sizes[0] > 0:
            group_sizes = (group_sizes[0] - 1, *group_sizes[1:])
            return arrangements_count(values[1:], group_sizes, previous_was_hash=True)
        else:
            assert group_sizes[0] == 0
            return 0
    elif values[0] == "?":
        values = '.' + values[1:]
        count_with_dot = arrangements_count(
            values, group_sizes, previous_was_hash=previous_was_hash
        )

        values = '#' + values[1:]
        count_with_hash = arrangements_count(
            values, group_sizes, previous_was_hash=previous_was_hash
        )

        return count_with_dot + count_with_hash
    else:
        raise ValueError(f"Unexpected {values=}")


def main():
    data = pathlib.Path("day12_input.txt").read_text()
    lines = data.split("\n")

    total_count = 0
    multiplier = 1

    for idx, line in enumerate(lines):
        record = Record.from_line(line, multiplier=multiplier)

        print()
        print(f"{idx}.")
        print(line)
        with measure_exec_time():
            line_count = arrangements_count(record.value, record.groups)
        print(line_count)
        print()

        total_count += line_count

    print(total_count)


if __name__ == "__main__":
    main()
