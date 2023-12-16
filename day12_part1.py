# Day 12
import functools
import pathlib
from dataclasses import dataclass
import re
from typing import Iterable

_MULTIPLER = 1

@dataclass
class Record:
    value: str
    groups: tuple[int, ...]

    @staticmethod
    def from_line(l: str) -> "Record":
        value_raw, groups_raw = l.split(" ")
        groups = tuple(map(int, groups_raw.split(","))) * _MULTIPLER
        value = "?".join(value_raw for _ in range(_MULTIPLER))
        return Record(value=value, groups=groups)


# def arrangements_count_internal(
#         values: list[str],
#         groups: tuple[int, ...]
# ) -> int:


def find_unknown_idx(value: str) -> int:
    if "?" not in value:
        assert "?" in value

    idx = len(value) // 2
    left_idx = idx
    right_idx = idx + 1
    while True:
        if left_idx >= 0 and value[left_idx] == "?":
            return left_idx

        if right_idx < len(value) and value[right_idx] == "?":
            return right_idx

        left_idx -= 1
        right_idx += 1


Values = tuple[str, ...]
GroupSizes = tuple[int, ...]
ValueGroups = tuple[Values, ...]


@functools.lru_cache
def trim_value_groups(
    value_groups: ValueGroups, group_sizes: GroupSizes
) -> tuple[ValueGroups, GroupSizes]:
    for value_group, group_size in zip(value_groups[::], group_sizes[::]):
        if len(value_group) == group_size and "?" not in value_group:
            value_groups = value_groups[1:]
            group_sizes = group_sizes[1:]
        else:
            break

    for value_group, group_size in zip(value_groups[::-1], group_sizes[::-1]):
        if len(value_group) == group_size and "?" not in value_group:
            value_groups = value_groups[:-1]
            group_sizes = group_sizes[:-1]
        else:
            break

    return (value_groups, group_sizes)


@functools.lru_cache
def are_valid(value_groups: ValueGroups, group_sizes: GroupSizes) -> bool:
    if value_groups and not group_sizes:
        for value_group in value_groups:
            if "#" in value_group:
                return False

    if not value_groups and group_sizes:  # No more values but still value groups.
        return False

    for value_group, group_size in zip(value_groups[::], group_sizes[::]):
        if "?" in value_group:
            break

        if len(value_group) != group_size:
            assert "?" not in value_group
            return False

    for value_group, group_size in zip(value_groups[::-1], group_sizes[::-1]):
        if "?" in value_group:
            break

        if len(value_group) != group_size:
            assert "?" not in value_group
            return False

    return True

def replace_at_idx(val: str, idx: int, new_value: str) -> str:
    table = list(val)
    table[idx] = new_value
    return  "".join(table)


@functools.lru_cache
def opts_with_question_at(idx: int, initial_value: str) -> tuple[str, str]:
    tmpl = list(initial_value)
    tmpl[idx] = "#"
    opts = []
    opts.append("".join(tmpl))

    tmpl[idx] = "."
    opts.append("".join(tmpl))
    return (opts[0], opts[1])


def get_potential_group_splits(
    value_groups: tuple[int, ...],
) -> Iterable[tuple[tuple[int, ...], tuple[int, ...]]]:
    for split_idx in range(len(value_groups) + 1):
        left_groups = value_groups[:split_idx]
        right_groups = value_groups[split_idx:]
        yield (left_groups, right_groups)


@functools.lru_cache()
def arrangements_count(values: str, group_sizes: tuple[int, ...]) -> int:
    value_groups: ValueGroups = tuple(tuple(g) for g in re.split(r"\.+", values) if g)

    value_groups, group_sizes = trim_value_groups(value_groups, group_sizes)

    if not are_valid(value_groups, group_sizes):
        return 0

    if not value_groups and not group_sizes:  # all trimmed (groups matching)
        return 1

    # TODO: try to split after every group_size

    # ??? 1,1

    values = ".".join("".join(g) for g in value_groups)

    unknown_idx = find_unknown_idx(values)

    #
    count_with_split = 0
    left_values, right_values = values[:unknown_idx], values[unknown_idx + 1 :]
    for (left_group_sizes, right_group_sizes) in get_potential_group_splits(group_sizes):
        left_opts = arrangements_count(left_values, left_group_sizes)
        right_opts = arrangements_count(right_values, right_group_sizes)
        count_with_split += left_opts * right_opts

    new_with_hash = replace_at_idx(values, unknown_idx, '#')
    count_with_hash = arrangements_count(new_with_hash, group_sizes)

    count_total = count_with_split + count_with_hash

    # print(values, group_sizes, count_total)

    return count_total


# ?##
#


def main():
    data = pathlib.Path("day12_input_test.txt").read_text()
    lines = data.split("\n")

    total_count = 0
    for line in lines:
        record = Record.from_line(line)
        line_count = arrangements_count(record.value, record.groups)
        print(line, line_count)
        total_count += line_count

    print(total_count)


if __name__ == "__main__":
    main()
