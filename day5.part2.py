# Day 5

from dataclasses import dataclass
import pathlib
from typing import Iterable, NamedTuple, TypeVar


def difference(r1: range, r2: range) -> list[range]:
    # -- r1 --
    #          - r2 -
    if r1.stop <= r2.start:
        return [r1]

    #    -- r1 --
    #          - r2 -
    if r1.start < r2.start and r1.stop > r2.start and r1.stop < r2.stop:
        return [range(r1.start, r2.start)]

    #         -- r1 --
    #          - r2 -
    if r1.start < r2.start and r1.stop > r2.stop:
        return [range(r1.start, r2.start), range(r2.stop, r1.stop)]

    #           -- r1 --
    #          - r2 -
    if r1.start > r2.start and r2.stop > r1.start and r1.stop > r2.stop:
        return [range(r2.stop + 1, r1.stop)]

    #                   -- r1 --
    #          - r2 -
    if r1.start >= r2.stop:
        return [r1]

    raise RuntimeError(f"Unexpected ranges {r1=}, {r2=}")


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
        raise NotImplementedError


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
    # TODO(pszyma): create apply that maps ranges.
    ...


T = TypeVar("T")


def pairs(iterable: Iterable[T]) -> Iterable[tuple[T, T]]:
    pair: list[T] = []
    for item in iterable:
        if len(pair) == 2:
            yield (pair[0], pair[1])
            pair = []

        pair.append(item)


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
    # Tests.
    mapping1 = ItemMapping(dest_start=50, source_start=98, size=2)
    assert list(mapping1.range_) == [98, 99]

    mapping2 = ItemMapping(dest_start=52, source_start=50, size=48)
    assert mapping2.apply(79) == 81

    # right intersect
    assert intersection(range(0, 5), range(1, 6)) == range(1, 5)
    # all intersect
    assert intersection(range(0, 5), range(1, 4)) == range(1, 4)
    # left intersect
    assert intersection(range(-5, 6), range(0, 5)) == range(0, 5)
    # no intersect
    assert intersection(range(0, 5), range(6, 10)) == range(0, 0)
    # -- r1 --
    #          - r2 -


    # assert_equal(
    #     difference(range(0, 10), range(10, 15)), [range(0, 10)]
    # )

    #    -- r1 --
    #          - r2 -

    assert_equal(
        difference(range(0, 10), range(5, 15)), [range(0, 5)]
    )

    #         -- r1 --
    #          - r2 -

    assert_equal(
        difference(range(0, 10), range(1, 5)), [range(0, 1), range(5, 10)]
    )

    #           -- r1 --
    #          - r2 -

    assert_equal(
        difference(range(5, 10), range(0, 5)), [range(5, 10)]
    )

    #                   -- r1 --
    #          - r2 -

    # main()
