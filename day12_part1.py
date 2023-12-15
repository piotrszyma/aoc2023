# Day 12
import functools
import pathlib
from dataclasses import dataclass
import re


@dataclass
class Record:
    value: str
    groups: tuple[int, ...]

    @staticmethod
    def from_line(l: str) -> "Record":
        value, groups_raw = l.split(" ")
        groups = tuple(map(int, groups_raw.split(",")))
        return Record(value=value, groups=groups)


# def arrangements_count_internal(
#         values: list[str],
#         groups: tuple[int, ...]
# ) -> int:


def find_unknown_idx(value: str) -> int:
    if "?" not in value:
        assert "?" in value

    idx = len(value) // 2 - 1
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


def trim_value_groups(
    value_groups: ValueGroups, group_sizes: GroupSizes
) -> tuple[ValueGroups, GroupSizes]:
    for value_group, group_size in zip(value_groups[::], group_sizes[::]):
        if len(value_group) == group_size:
            value_groups = value_groups[1:]
            group_sizes = group_sizes[1:]
        else:
            break

    for value_group, group_size in zip(value_groups[::-1], group_sizes[::-1]):
        if len(value_group) == group_size:
            value_groups = value_groups[:-1]
            group_sizes = group_sizes[:-1]
        else:
            break

    return (value_groups, group_sizes)


def are_valid(value_groups: ValueGroups, group_sizes: GroupSizes) -> bool:
    if not value_groups and group_sizes:  # No more values but still value groups.
        return False

    for value_group, group_size in zip(value_groups[::], group_sizes[::]):
        if len(value_group) != group_size:
            if "?" not in value_group:
                return False
            else:
                break

    for value_group, group_size in zip(value_groups[::-1], group_sizes[::-1]):
        if len(value_group) != group_size:
            if "?" not in value_group:
                return False
            else:
                break

    return True


@functools.lru_cache()
def arrangements_count(values: str, group_sizes: tuple[int, ...]) -> int:
    value_groups: ValueGroups = tuple(tuple(g) for g in re.split(r"\.+", values) if g)

    value_groups, group_sizes = trim_value_groups(value_groups, group_sizes)

    if not are_valid(value_groups, group_sizes):
        return 0

    if not value_groups and not group_sizes: # all trimmed (groups matching)
        return 1

    # ??? 1,1

    values = ".".join("".join(g) for g in value_groups)

    unknown_idx = find_unknown_idx(values)

    values_lst_1 = list(values)
    values_lst_1[unknown_idx] = "#"
    values_lst_1 = "".join(values_lst_1)

    arrangements_1 = arrangements_count(values_lst_1, group_sizes)

    values_lst_2 = list(values)
    values_lst_2[unknown_idx] = "."
    values_lst_2 = "".join(values_lst_2)

    arrangements_2 = arrangements_count(values_lst_2, group_sizes)

    total_count = arrangements_1 + arrangements_2

    print(values, group_sizes, total_count)

    return total_count


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
