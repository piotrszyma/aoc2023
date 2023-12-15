# Day 12
import functools
import pathlib
from dataclasses import dataclass


@dataclass
class Arrangement:
    value: list[str]
    idx: int  # currently processed index
    groups: list[int]  #

    def previous_value(self) -> str:
        return self.value[self.idx - 1]


def pattern_groups_size(pattern: tuple[str, ...]) -> tuple[int, ...]:
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
            if item != "#":
                ...
            assert item == "#"
            group_size += 1

    if group_size > 0:
        groups_size.append(group_size)
        group_size = []

    return tuple(groups_size)


def can_be_subgroup(group_size: tuple[int, ...], potential_supgroup: tuple[int, ...]) -> bool:
    if len(potential_supgroup) > len(group_size):
        return False

    for idx, _ in enumerate(potential_supgroup[:-1]):
        if potential_supgroup[idx] != group_size[idx]:  # todo: last can be smaller
            return False

    return True


@dataclass
class Pattern:
    value: tuple[str, ...]
    unknown_count: int
    unknown_first_idx: int = 0


_MULTIPLIER = 5


def _arrangements_for(raw_line: str) -> int:
    print('calculating for ', raw_line)

    patterns_raw, groups_raw = raw_line.split(" ")

    # TODO: uncomment for part 2

    patterns_raw = "?".join(patterns_raw for _ in range(_MULTIPLIER))
    groups_raw = ",".join(groups_raw for _ in range(_MULTIPLIER))

    expected_group_size = tuple(int(a) for a in groups_raw.split(","))

    initial_pattern = Pattern(
        value=tuple(patterns_raw), unknown_count=patterns_raw.count("?")
    )
    final_patterns: list[Pattern] = []
    patterns: list[Pattern] = [initial_pattern]

    while patterns:
        pattern = patterns.pop()

        groups_size = pattern_groups_size(pattern.value)
        if not can_be_subgroup(
            group_size=expected_group_size,
            potential_supgroup=groups_size,
        ):
            continue

        assert pattern.unknown_count >= 0
        if pattern.unknown_count == 0:
            final_patterns.append(pattern)
            continue

        for idx, el in enumerate(pattern.value):
            if idx < pattern.unknown_first_idx:
                continue

            if el == "?":
                value = list(pattern.value)
                value[idx] = "."
                patterns.append(
                    Pattern(
                        value=tuple(value),
                        unknown_count=pattern.unknown_count - 1,
                        unknown_first_idx=idx + 1,
                    )
                )

                value[idx] = "#"
                patterns.append(
                    Pattern(
                        value=tuple(value),
                        unknown_count=pattern.unknown_count - 1,
                        unknown_first_idx=idx + 1,
                    )
                )

                break

    valid_patterns_count = 0

    for pattern in final_patterns:
        groups_size = pattern_groups_size(pattern.value)
        if groups_size == expected_group_size:
            valid_patterns_count += 1

    return valid_patterns_count


def main():
    data = pathlib.Path("day12_input_test.txt").read_text()
    lines = data.split("\n")
    arrangements_sum = sum(_arrangements_for(l) for l in lines)
    print(arrangements_sum)


if __name__ == "__main__":
    main()
