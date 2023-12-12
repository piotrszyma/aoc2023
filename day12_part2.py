# Day 12
import pathlib
from dataclasses import dataclass


@dataclass
class Arrangement:
    items_to_process: list[str]
    items_processed: list[str]
    current_item: str | None  # non indicates that arrangement is final and nothing else needed
    groups_to_match: list[int]
    current_group_len: int

    def __str__(self):
        all_items = (
            "".join(self.items_processed)
            + ("|" + self.current_item + "|" if self.current_item else "")
            + "".join(self.items_to_process)
        )
        return f"{all_items}, ci={self.current_item}, gtm={self.groups_to_match} gl={self.current_group_len}"

    def all_consumed(self) -> bool:
        return self.current_item is None

    def all_groups_matched(self) -> bool:
        return len(self.groups_to_match) == 0

    def has_accumulated_group(self) -> bool:
        return self.current_group_len > 0

    def accumulated_group_matches_expected(self) -> bool:
        return self.current_group_len == self.groups_to_match[0]

    def next_item(self) -> str | None:
        for item in self.items_to_process:
            return item
        return None

    def next_items_processed(self) -> list[str]:
        assert self.current_item is not None
        return [*self.items_processed, self.current_item]

    def process(self) -> list["Arrangement"]:
        if self.current_item != "?" and len(self.items_to_process) == 0:
            if self.current_item == "#":
                if (
                    len(self.groups_to_match) == 1
                    and self.groups_to_match[0] == self.current_group_len + 1 # +1 for current item
                ):
                    return [
                        Arrangement(
                            items_to_process=[],
                            items_processed=self.next_items_processed(),
                            current_item=self.next_item(),
                            groups_to_match=[],
                            current_group_len=0,
                        )
                    ]
                else:
                    return []
            elif self.current_item == ".":
                if (len(self.groups_to_match) == 0 and self.current_group_len == 0) or (
                    len(self.groups_to_match) == 1
                    and self.groups_to_match[0] == self.current_group_len
                ):
                    return [
                        Arrangement(
                            items_to_process=[],
                            items_processed=self.next_items_processed(),
                            current_item=self.next_item(),
                            groups_to_match=[],
                            current_group_len=0,
                        )
                    ]
                else:
                    return []
            else:
                raise ValueError(f"unexpected current item = {self.current_item}")

        if self.current_item == ".":
            if self.has_accumulated_group():
                if len(self.groups_to_match) == 0:
                    return []
                if self.current_group_len == self.groups_to_match[0]:
                    # consume current item and matching group
                    return [
                        Arrangement(
                            items_to_process=self.items_to_process[1:],
                            items_processed=self.next_items_processed(),
                            current_item=self.next_item(),
                            groups_to_match=self.groups_to_match[1:],
                            current_group_len=0,
                        )
                    ]
                else:
                    # Accumulated group must end but does not match expected group.
                    return []
            else:  # no accumulated groups
                assert self.current_group_len == 0
                return [
                    Arrangement(
                        items_to_process=self.items_to_process[1:],
                        items_processed=self.next_items_processed(),
                        current_item=self.next_item(),
                        groups_to_match=self.groups_to_match,  # does not consume any groups to match
                        current_group_len=self.current_group_len,  # should be 0
                    )
                ]
        elif self.current_item == "#":
            if self.has_accumulated_group():
                self.current_group_len += 1

                if len(self.groups_to_match) == 0:
                    return []

                expected_group_len = self.groups_to_match[0]
                if expected_group_len < self.current_group_len:
                    return []

                return [
                    Arrangement(
                        items_to_process=self.items_to_process[1:],
                        items_processed=self.next_items_processed(),
                        current_item=self.next_item(),
                        groups_to_match=self.groups_to_match,
                        current_group_len=self.current_group_len,
                    )
                ]
            else:  # no accumulated groups
                assert self.current_group_len == 0
                return [
                    Arrangement(
                        items_to_process=self.items_to_process[1:],
                        items_processed=self.next_items_processed(),
                        current_item=self.next_item(),
                        groups_to_match=self.groups_to_match,
                        current_group_len=1,  # a new group.
                    )
                ]
        elif self.current_item == "?":
            return [
                Arrangement(
                    items_to_process=self.items_to_process,
                    items_processed=self.items_processed,
                    current_item=".",
                    groups_to_match=self.groups_to_match,
                    current_group_len=self.current_group_len,
                ),
                Arrangement(
                    items_to_process=self.items_to_process,
                    items_processed=self.items_processed,
                    current_item="#",
                    groups_to_match=self.groups_to_match,
                    current_group_len=self.current_group_len,
                ),
            ]

        raise ValueError("unexpected state")


def _arrangements_for(raw_line: str) -> int:
    groups_raw, arrangements_raw = raw_line.split(" ")

    groups = [int(a) for a in arrangements_raw.split(",")]

    initial_opt = list(groups_raw)
    all_items = len(initial_opt)
    arrangements_to_process = [
        Arrangement(
            items_to_process=initial_opt[1:],
            items_processed=[],
            current_item=initial_opt[0],
            groups_to_match=groups,
            current_group_len=1 if initial_opt[0] == "#" else 0,
        )
    ]
    arrangements_final = []

    while arrangements_to_process:
        arrangement = arrangements_to_process.pop()

        if arrangement.all_consumed():
            if arrangement.all_groups_matched():
                arrangements_final.append(arrangement)

            continue

        # print("arrangement\t\t", str(arrangement))
        next_arrangements = arrangement.process()
        # print("next_arrangements\t", [str(s) for s in next_arrangements])

        arrangements_to_process.extend(next_arrangements)

    # print("arrangements_final", [str(a) for a in arrangements_final])

    return len(arrangements_final)


def main():
    data = pathlib.Path("day12_input.txt").read_text()
    lines = data.split("\n")

    count_all = 0
    for line in lines:
        count = _arrangements_for(line)
        print(count, "\t", line)
        count_all += count

    print(count_all)


if __name__ == "__main__":
    main()
