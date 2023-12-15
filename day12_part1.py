# Day 12
import pathlib
from dataclasses import dataclass


@dataclass
class Arrangement:
    value: list[str]
    idx: int  # currently processed index
    groups: list[int]  #

    def previous_value(self) -> str:
        return self.value[self.idx - 1]


def pattern_groups_size(pattern: list[str]) -> list[int]:
    groups_size = []
    group_size = 0
    for item in pattern:
        if item == ".":
            if group_size > 0:
                groups_size.append(group_size)
                group_size = 0
        elif item == "?":
            break
        else:
            assert item == "#"
            group_size += 1

    if group_size > 0:
        groups_size.append(group_size)
        group_size = []

    return groups_size


def can_be_subgroup(group_size: list[int], potential_supgroup: list[int]) -> bool:
    if len(potential_supgroup) > len(group_size):
        return False

    for idx, _ in enumerate(potential_supgroup[:-1]):
        if potential_supgroup[idx] != group_size[idx]: # todo: last can be smaller
            return False

    return True


def _arrangements_for(raw_line: str) -> int:
    patterns_raw, groups_raw = raw_line.split(" ")

    expected_group_size = [int(a) for a in groups_raw.split(",")]

    initial_pattern = list(patterns_raw)
    final_patterns: list[list[str]] = []
    patterns: list[list[str]] = [initial_pattern]

    while patterns:
        pattern = patterns.pop()

        if not can_be_subgroup(
            group_size=expected_group_size,
            potential_supgroup=pattern_groups_size(pattern),
        ):
            continue

        if "?" not in pattern:
            final_patterns.append(pattern)
            continue

        for idx, el in enumerate(pattern):
            if el == "?":
                pattern[idx] = "."
                patterns.append(list(pattern))

                pattern[idx] = "#"
                patterns.append(list(pattern))

                break

    valid_patterns_count = 0

    for pattern in final_patterns:
        groups_size = pattern_groups_size(pattern)
        if groups_size == expected_group_size:
            valid_patterns_count += 1

    return valid_patterns_count


def main():
    data = pathlib.Path("day12_input.txt").read_text()
    lines = data.split("\n")
    arrangements_sum = sum(_arrangements_for(l) for l in lines)
    print(arrangements_sum)


if __name__ == "__main__":
    main()
