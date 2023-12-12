# Day 12
import pathlib
from dataclasses import dataclass

@dataclass
class Arrangement:
    value: list[str]
    idx: int # currently processed index
    groups: list[int] #

    def previous_value(self) -> str:
        return self.value[self.idx - 1]


def _arrangements_for(raw_line: str) -> int:
    groups_raw, arrangements_raw = raw_line.split(" ")

    arrangements = [int(a) for a in arrangements_raw.split(",")]

    initial_opt = list(groups_raw)
    final_options: list[list[str]] = []
    options: list[list[str]] = [initial_opt]



    while options:
        opt = options.pop()
        if '?' not in opt:
            final_options.append(opt)
            continue

        for idx, el in enumerate(opt):
            if el == '?':
                opt[idx] = '.'
                options.append(list(opt))

                opt[idx] = '#'
                options.append(list(opt))

                break

    valid_opt_count = 0

    for final_opt in final_options:
        final_opt = [e for e in "".join(final_opt).split(".") if e]
        final_opt_arg = [len(e) for e in final_opt]
        if final_opt_arg == arrangements:
            valid_opt_count += 1

    return valid_opt_count


def main():
    data = pathlib.Path("day12_input.txt").read_text()
    lines = data.split("\n")
    arrangements_sum = sum(_arrangements_for(l) for l in lines)
    print(arrangements_sum)


if __name__ == "__main__":
    main()
