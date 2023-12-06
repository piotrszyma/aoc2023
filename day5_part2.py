# Day 5

from dataclasses import dataclass
import pathlib
from typing import Iterable, NamedTuple, TypeVar

def is_empty(range: range) -> bool:
    return len(range) == 0


def difference(r1: range, r2: range) -> list[range]:
    # nothing in common from left
    if r2.stop <= r1.start:
        return [r1]

    # nothing in common from right
    if r2.start >= r1.stop:
        return [r1]

    # left overlap (not fully)
    if r2.start <= r1.start and r2.stop < r1.stop:
        return [range(r2.stop, r1.stop)]

    # right overlap (not fully)
    if r1.start < r2.start and r2.stop >= r1.stop:
        return [range(r1.start, r2.start)]

    # r1 is smaller or at most equal r2
    if r1.start >= r2.start and r1.stop <= r2.stop:
        return []

    # r2 cuts r1 into two
    if r1.start < r2.start and r1.stop > r2.stop:
        return [range(r1.start, r2.start), range(r2.stop, r1.stop)]


    # # -- r1 --
    # #          - r2 -
    # if r1.stop <= r2.start:
    #     return [r1]

    # #    -- r1 --
    # #          - r2 -
    # if r1.start <= r2.start and r1.stop > r2.start and r1.stop < r2.stop:
    #     return [range(r1.start, r2.start)]

    # #         -- r1 --
    # #          - r2 -
    # #           -- r1 --
    # #          - r2 -
    # if r1.start > r2.start and r2.stop > r1.start and r1.stop > r2.stop:
    #     return [range(r2.stop + 1, r1.stop)]

    # #                   -- r1 --
    # #          - r2 -
    # if r1.start >= r2.stop:
    #     return [r1]

    raise RuntimeError(f"Unexpected ranges {r1=}, {r2=} for difference")


def intersection(r1: range, r2: range) -> range:
    return range(max(r1[0], r2[0]), min(r1[-1], r2[-1]) + 1)


@dataclass
class ItemMapping:
    dest_start: int
    source_start: int
    size: int

    @property
    def range_(self) -> range:
        return range(self.source_start, self.source_start + self.size)

    @property
    def shift(self) -> int:
        return self.dest_start - self.source_start

    @staticmethod
    def from_raw_value(value_raw: str) -> "ItemMapping":
        dest_start, source_start, size = value_raw.split(" ")
        return ItemMapping(
            dest_start=int(dest_start),
            source_start=int(source_start),
            size=int(size),
        )

    def apply(self, value: int) -> int | None:
        if value in self.range_:
            return value + self.shift
        else:
            return None

    def apply_range(self, r: range) -> tuple[range | None, list[range]]:
        """Returns pair - applied chunk (or None if nothing) and not applied list."""
        common_range = intersection(r, self.range_)
        if is_empty(common_range):
            return (None, [r])

        other_ranges = difference(r, common_range)

        common_range_shifted = range(common_range.start + self.shift, common_range.stop + self.shift)
        return (common_range_shifted, other_ranges)


class ItemKey(NamedTuple):
    source: str
    target: str


def apply(value: int, mappings: list[ItemMapping]) -> int:
    for mapping in mappings:
        new_value = mapping.apply(value)
        if new_value is not None:  # return if there is a match
            return new_value
    return value  # otherwise fallback to same value


def apply_range(r: range, mappings: list[ItemMapping]) -> list[range]:
    # seeds: 79 14 55 13
    # seed-to-soil map:
    # 50 98 2
    # 52 50 48
    for mapping in mappings:
        applied_ranges, other_ranges = mapping.apply_range(r)
        if applied_ranges is not None:
            # assert len(other_ranges) == 0
            return [applied_ranges, *other_ranges]

    return [r]


T = TypeVar("T")


def pairs(iterable: Iterable[T]) -> Iterable[tuple[T, T]]:
    pair: list[T] = []
    for item in iterable:
        if len(pair) == 2:
            yield (pair[0], pair[1])
            pair = []

        pair.append(item)

    if len(pair) == 2:
        yield (pair[0], pair[1])


def main():
    data = pathlib.Path("day5.input.txt").read_text()
    sections_raw = data.split("\n\n")
    seeds_raw = sections_raw[0]
    mappings_raw = sections_raw[1:]

    seeds_ranges = [
        range(start, start + size)
        for (start, size) in pairs(
            int(s) for s in seeds_raw.replace("seeds: ", "").split(" ")
        )
    ]
    mappings: dict[ItemKey, list[ItemMapping]] = {}
    item_source_to_target: dict[str, str] = {}

    for mapping_raw in mappings_raw:
        item_key_raw, values_raw = mapping_raw.split(" map:")
        source, target = item_key_raw.split("-to-")
        values_raw = values_raw.strip()
        values = values_raw.split("\n")

        item_key = ItemKey(source=source, target=target)
        item_source_to_target[source] = target

        item_mappings: list[ItemMapping] = []

        for value_raw in values:
            item_mappings.append(ItemMapping.from_raw_value(value_raw))

        mappings[item_key] = item_mappings

    current = "seed"
    values = seeds_ranges

    while current != "location":
        new_current = item_source_to_target[current]
        item_key = ItemKey(source=current, target=new_current)
        item_mappings = mappings[item_key]

        new_values = []
        for v in values:
            for new_range in apply_range(v, item_mappings):
                new_values.append(new_range)

        values = new_values
        current = new_current

    lowest_location = min(r.start for r in values)
    print(lowest_location)

import traceback

def assert_equal(left: T, right: T):
    if left != right:
        try:
            raise ValueError(f"left is not right = {(left, right)}")
        except ValueError as error:
            traceback.print_stack()
            print(error)


if __name__ == "__main__":
    main()
