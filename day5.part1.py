# Day 5

from dataclasses import dataclass
import pathlib
from typing import NamedTuple

@dataclass
class ItemMapping:
    dest_start: int
    source_start: int
    size: int

    @property
    def range(self) -> range:
        return range(self.source_start, self.source_start + self.size)

    @property
    def shift(self) -> int:
        return self.dest_start - self.source_start

    @staticmethod
    def from_raw_value(value_raw: str) -> 'ItemMapping':
        dest_start, source_start, size = value_raw.split(' ')
        return ItemMapping(
            dest_start=int(dest_start),
            source_start=int(source_start),
            size=int(size),
        )

    def apply(self, value: int) -> int | None:
        if value in self.range:
            return value + self.shift
        else:
            return None




class ItemKey(NamedTuple):
    source: str
    target: str


def apply(value: int, mappings: list[ItemMapping]) -> int:
    for mapping in mappings:
        new_value = mapping.apply(value)
        if new_value is not None: # return if there is a match
            return new_value
    return value # otherwise fallback to same value


def main():
    data = pathlib.Path("day5.input.txt").read_text()
    sections_raw = data.split("\n\n")
    seeds_raw = sections_raw[0]
    mappings_raw = sections_raw[1:]

    seeds = [int(s) for s in seeds_raw.replace("seeds: ", "").split(" ")]
    mappings: dict[ItemKey, list[ItemMapping]] = {}
    item_source_to_target: dict[str, str] = {}

    for mapping_raw in mappings_raw:
        item_key_raw, values_raw = mapping_raw.split(" map:")
        source, target = item_key_raw.split("-to-")
        values_raw = values_raw.strip()
        values = values_raw.split('\n')

        item_key = ItemKey(source=source, target=target)
        item_source_to_target[source] = target

        item_mappings: list[ItemMapping] = []

        for value_raw in values:
            item_mappings.append(ItemMapping.from_raw_value(value_raw))

        mappings[item_key] = item_mappings

    current = 'seed'
    values = seeds

    while current != "location":
        new_current = item_source_to_target[current]
        item_key = ItemKey(source=current, target=new_current)
        item_mappings = mappings[item_key]

        new_values = [apply(v, item_mappings) for v in values]

        values = new_values
        current = new_current

    lowest_location = min(values)
    print(lowest_location)



if __name__ == "__main__":
    # Tests.
    mapping1 = ItemMapping(dest_start=50, source_start=98, size=2)
    assert list(mapping1.range) == [98, 99]

    mapping2 = ItemMapping(dest_start=52, source_start=50, size=48)
    assert mapping2.apply(79) == 81

    main()

