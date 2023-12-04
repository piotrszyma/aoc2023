# Day 1

_word_to_digit = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def main():
    with open("day1.input.txt", "r") as f:
        total = 0

        for line in f:
            if not line.strip():
                break

            first: int | None = None
            last: int | None = None

            prefix = ""

            for c in line:
                if first is not None:
                    break

                if c.isdigit():
                    first = int(c)
                else:
                    prefix += c
                    for word in _word_to_digit:
                        if word in prefix:
                            first = _word_to_digit[word]

            suffix = ""

            for c in line[::-1]:
                if last is not None:
                    break

                if c.isdigit():
                    last = int(c)
                else:
                    suffix = c + suffix
                    for word in _word_to_digit:
                        if word in suffix:
                            last = _word_to_digit[word]

            assert first is not None
            assert last is not None

            num = int(str(first) + str(last))
            total += num

            print(f"{line=} {num=}")

        print(total)


if __name__ == "__main__":
    main()
